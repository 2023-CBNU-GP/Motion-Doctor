from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed

from .models import *
import random
import string

import jwt
from . import serializers
import json


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
            # CVmanager.doctorManage(file_data[i])
            form = Correctpic()
            form.picturefilename = file_data[i]
            form.exercisename = name_data[i]
            form.exercisetype = type_data[i] + '-' + rand_str
            form.doctorid = doctor
            form.save()

        # 동영상 정보 json으로 저장하는 거 여기에 넣어주세용



        response = Response()
        response.data = {
            'message': 'success'
        }

        return response


class FileDelete(APIView):
    def post(self, request):
        body = json.loads(request.body.decode('utf-8'))
        data = Correctpic.objects.filter(exercisename=body['name']).first()
        data.delete()

        response = Response()
        response.data = {
            'message': 'success'
        }

        return response


# 환자 모션 웹캠 저장 및 점수 반환 API
class PatientEvaluation(APIView):
    def post(self, request):
        # 현재 로그인되어있는 patient 정보 받아오기
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed("Unauthenticated!")

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Unauthenticated!")

        patient = Patient.objects.filter(id=payload['id']).first()

        form = Patientpic()
        form.picturefilename = request.FILES.get('file_path')

        # 여기가 모델로 파일을 넘겨서 점수 반환하는 부분입니다.
        # CVmanager=om.OpencvManager()
        # CVmanager.patientManage(form.picturefilename)
        # request.FILES.get('file_path')를 모델로 넘겨서 점수 반환해서 아래 score 변수에 저장해주세욤
        score = 0

        form.score = score
        form.correctpicid = Correctpic.objects.filter(exercisename=request.POST.get('name'), exercisetype=request.POST.get('type')).first()
        form.patientid = patient
        form.save()

        response = Response()
        response.data = {
            'message': 'success',
            'score': score
        }

        return response
