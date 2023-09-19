import base64
import shutil

import cv2
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed

from .models import *
import random
import string

import jwt
from . import serializers
import json

from .AngleManager import *
from .PoseDetector import *

import tempfile
import subprocess
from os import path
import time


# 의사가 파일 업로드하는 API 입니다!
class FileUpload(APIView):
    def post(self, request):
        # 현재 로그인되어있는 doctor 정보 받아오기
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed("Unauthenticated!")

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Unauthenticated!")

        doctor = Doctor.objects.filter(id=payload['id']).first()
        # CVmanager=om.OpencvManager()

        # 동영상 저장하는 부분
        file_data = request.FILES.getlist('file_path')
        name_data = request.POST.getlist('name')
        type_data = request.POST.getlist('tag')

        if int(request.POST.get('num')) != len(file_data):
            raise serializers.ValidationError("업로드할 파일 개수가 맞지 않습니다.")

        n = 10    # 문자의 개수(문자열의 크기)
        rand_str = ""  # 문자열
        for i in range(n):
            rand_str += str(random.choice(string.ascii_uppercase))

        for i in range(int(request.POST.get('num'))):
            form = Correctpic()
            form.picturefilename = file_data[i]
            form.exercisename = name_data[i]
            form.exercisetype = type_data[i] + '-' + rand_str
            form.doctorid = doctor
            form.save()

            # 동영상 정보 json으로 저장하는 부분
            while True:
                cap = cv2.VideoCapture('media/' + str(form.picturefilename))
                if cap.isOpened():
                    print("생성되었습니다.")
                    break
            pTime = 0
            detector = PoseDetector()
            angleManager = AngleManager()

            frameCount = cap.get(cv2.CAP_PROP_FRAME_COUNT)
            DoctorAngle = {"LelbowAngle": 0, "LshoulderAngle": 0, "RelbowAngle": 0, "RshoulderAngle": 0,
                           "Lhip": 0, "Rhip": 0, "Lknee": 0, "Rknee": 0}

            poselist = {11: [0, 0], 12: [0, 0], 13: [0, 0], 14: [0, 0], 15: [0, 0], 16: [0, 0], 23: [0, 0], 24: [0, 0],
                        25: [0, 0], 26: [0, 0], 27: [0, 0], 28: [0, 0]}

            while True:
                success, img = cap.read()

                Curframe = cap.get(cv2.CAP_PROP_POS_FRAMES)

                if Curframe >= frameCount / 3 and Curframe <= frameCount - frameCount / 3:  # 현재 프레임 수를 확인 후, 지정된 프레임 이상일 시 동영상에서 스켈렙톤 뽑아내기
                    img = detector.findPose(img)
                    lmList,_ = detector.findPosition(img)
                    # 사이각 구하기 공식
                    angleManager.GetAngle(lmList, DoctorAngle)
                    angleManager.GetAverageAngle(lmList, DoctorAngle)
                    # cos유사도
                    angleManager.GetAverageJoint(lmList, poselist)

                if img is None:
                    break

            for id, value in poselist.items():
                x = value[0]
                y = value[1]

                poselist[id] = [round(x / (frameCount / 3) % 360, 2), round(y / (frameCount / 3) % 360, 2)]

            name_list = str(form.picturefilename).split('/')
            angleManager.TransferJsonFile('media/'+name_list[0]+"/"+name_list[1], name_list[2], poselist, DoctorAngle)

        response = Response()
        response.data = {
            'message': 'success'
        }

        return response


# 의사가 올린 파일 삭제하는 api
class FileDelete(APIView):
    def post(self, request):
        body = json.loads(request.body.decode('utf-8'))
        data = Correctpic.objects.filter(exercisetype=body['type'], exercisename=body['name']).first()

        if Patientpic.objects.filter(correctpicid=data.uid).first() is not None:
            raise AuthenticationFailed("파일을 삭제할 수 없습니다.")

        data.delete()

        response = Response()
        response.data = {
            'message': 'success'
        }

        return response


# 환자 모션 웹캠 저장 및 점수 반환 API -> websocket으로 전환
# class PatientEvaluation(APIView):
#     def post(self, request):
#         # 현재 로그인되어있는 patient 정보 받아오기
#         token = request.COOKIES.get('jwt')
#
#         if not token:
#             raise AuthenticationFailed("Unauthenticated!")
#
#         try:
#             payload = jwt.decode(token, 'secret', algorithms=['HS256'])
#         except jwt.ExpiredSignatureError:
#             raise AuthenticationFailed("Unauthenticated!")
#
#         patient = Patient.objects.filter(id=payload['id']).first()
#
#         file_data = request.FILES.get('file_path')
#         name_data = request.POST.get('name')
#         type_data = request.POST.get('type')
#
#         webm_path = default_storage.save('media/video.webm', file_data)
#         video_mp4 = "video.mp4"
#         subprocess.run(f"ffmpeg -i {path} {video_mp4}", shell=True)
#
#         score = 0
#         correctPic = Correctpic.objects.filter(exercisename=name_data, exercisetype=type_data).first()
#         patientpic = Patientpic.objects.filter(correctpicid=correctPic, patientid=patient).first()
#         if patientpic is None:
#             # 새로운 Patientpic 객체 생성 및 저장 (여기서 webm 파일을 mp4로 변환해야함)
#             with open("media/video.mp4", "rb") as file:
#                 form = Patientpic()
#
#                 file_obj = File(file)
#                 form.picturefilename = file_obj
#                 form.score = score
#                 form.correctpicid = correctPic
#                 form.patientid = patient
#
#                 form.save()
#                 print("파일이 생성되었습니다.")
#
#         else:
#             with open("media/video.mp4", "rb") as file:
#                 file_obj = File(file)
#                 patientpic.picturefilename = file_obj
#                 patientpic.save()
#
#         os.remove("video.webm")
#         os.remove("media/video.mp4")
#
#         # 환자가 영상을 찍으면 해당 의사와 매칭
#         if Manage.objects.filter(doctorid=correctPic.doctorid, patientid=patient).first() is None:
#             manage_form = Manage()
#             manage_form.doctorid = correctPic.doctorid
#             manage_form.patientid = patient
#             manage_form.save()
#
#         response = Response()
#         response.data = {
#             'message': 'success',
#             'score': 0
#         }
#
#         return response
