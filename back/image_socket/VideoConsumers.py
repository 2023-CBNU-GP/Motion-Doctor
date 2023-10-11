import base64
import json
import os

from channels.generic.websocket import AsyncWebsocketConsumer
from api.models import *

import tempfile
from django.core.files import File
import cv2

import subprocess
from api.AngleManager import *
from api.PoseDetector import *


# 환자 모션 웹캠 저장 및 점수 반환 consumer
class VideoConsumers(AsyncWebsocketConsumer):

    async def save_mp4(self, file_name_patient,file_name_doctor):

        fps = 30  # 원하는 프레임 속도
        cap = cv2.VideoCapture(file_name_patient)
        cap.set(cv2.CAP_PROP_FPS, fps)
        detector = PoseDetector()
        # 의사 파일 가져오는 코드
        cap1 = cv2.VideoCapture(file_name_doctor)
        cap1.set(cv2.CAP_PROP_FPS, fps)
        detector1 = PoseDetector()  # 의사용
        angleManager = AngleManager()
        # mp4확장자 선택을 위함
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        # 앞 string 파일 이름
        width = int(cap.get(3))
        height = int(cap.get(4))
        new_file_patient=file_name_patient[:-4]+"1.mp4" #동영상 저장 파일 이름
        out=cv2.VideoWriter(new_file_patient,fourcc, fps, (width, height)) #동영상 저장 파일 이름

        while True:
            success, target_image = cap.read()
            success1,doctor_image=cap1.read()

            if target_image is None or doctor_image is None:
                break

            target_image = detector.findPose(target_image)
            lmList, patient = detector.findPosition(target_image)

            doctor_image = detector1.findPose(doctor_image)
            _, doctor = detector1.findPosition(doctor_image)
            if not doctor or not patient:
                continue

            angleManager.adjustStd(patient, doctor)
            angleManager.transPos(patient[0][0] - doctor[0][0], patient[0][1] - doctor[0][1], doctor)
            detector1.drawPose(target_image, out, doctor, 100)
            success3=out.write(target_image) #동영상 저장하는 부분
            print(success3)
        out.release()
        return new_file_patient # True일 때 실행 하도록

    async def save_video(self, patient_id, exercise_name, exercise_type, video_data):
        # Base64 디코딩하여 바이너리 데이터로 변환
        binary_data = base64.b64decode(video_data)

        # 임시파일 저장 (webm으로 저장 -> mp4로 수동 변환하면 안 깨짐)
        temp_path = tempfile.gettempdir()
        file_name = '/video.webm'
        with open(temp_path + file_name, 'wb') as wfile:
            wfile.write(binary_data)

        video_webm = temp_path + "/video.webm"
        video2_mp4 = temp_path + "/video.mp4"

        subprocess.run(f"ffmpeg -i {video_webm} {video2_mp4}", shell=True)
        print("파일이 변환되었습니다.")

        score = 0
        correctPic = Correctpic.objects.filter(exercisename=exercise_name, exercisetype=exercise_type).first()
        patient = Patient.objects.filter(id=patient_id).first()

        patientpic = Patientpic.objects.filter(correctpicid=correctPic, patientid=patient).first()
        if patientpic is None:
            # 새로운 Patientpic 객체 생성 및 저장 (여기서 webm 파일을 mp4로 변환해야함)
            with open(temp_path + "/video.mp4", "rb") as file:
                form = Patientpic()

                file_obj = File(file)
                form.picturefilename = file_obj
                form.score = score
                form.correctpicid = correctPic
                form.patientid = patient

                form.save()

        else:
            with open(temp_path + "/video.mp4", "rb") as file:
                file_obj = File(file)
                patientpic.picturefilename = file_obj
                patientpic.save()

        os.remove('/tmp/video.webm')
        os.remove('/tmp/video.mp4')

        doctor_uid = Doctor.objects.filter(uid=correctPic.doctorid.uid).first()
        if Manage.objects.filter(patientid=patient, doctorid=doctor_uid).first() is None:
            manage_form = Manage()
            manage_form.doctorid = doctor_uid
            manage_form.patientid = patient
            manage_form.save()

        patientpic = Patientpic.objects.filter(correctpicid=correctPic, patientid=patient).first()
        print("파일이 생성되었습니다." + str(patientpic.picturefilename))

        # 환자 모션 영상을 프론트에서 보내면 이것이 media 폴더에 저장됨.
        # media 폴더에 있는 영상을 평가시스템에 넘겨서 점수 계산
        print("work")

        # correctpic = Correctpic.objects.filter(exercisetype=exercise_type, exercisename=exercise_name).first()

        # 여기에 파이썬 모델로 영상을 전송하여 결과 score를 저장
        file_name_patient = "media/" + str(patientpic.picturefilename)  # 소켓으로 전달된 환자 파일
        print(file_name_patient)
        cap = cv2.VideoCapture(file_name_patient)
        detector = PoseDetector()
        fps = 30  # 원하는 프레임 속도
        cap.set(cv2.CAP_PROP_FPS, fps)
        patientAngle = {"LelbowAngle": 0, "LshoulderAngle": 0, "RelbowAngle": 0, "RshoulderAngle": 0
            , "Lhip": 0, "Rhip": 0, "Lknee": 0, "Rknee": 0}
        scoreAngle = {"LelbowAngle": 0, "LshoulderAngle": 0, "RelbowAngle": 0, "RshoulderAngle": 0
            , "Lhip": 0, "Rhip": 0, "Lknee": 0, "Rknee": 0}
        angleManager = AngleManager()

        doctor_video_list = str(correctPic.picturefilename).split('/')
        file_name_doctor="media/" + doctor_video_list[0] + "/" + doctor_video_list[1]
        teacherAngle = angleManager.GetAvgAngle(file_name_doctor,doctor_video_list[2])  # 의사 파일명

        similarity = 0.0

        poselist = {11: [0, 0], 12: [0, 0], 13: [0, 0], 14: [0, 0], 15: [0, 0], 16: [0, 0], 23: [0, 0], 24: [0, 0],
                    25: [0, 0], 26: [0, 0], 27: [0, 0], 28: [0, 0]}

        while True:
            success, target_image = cap.read()

            if target_image is None:
                break
            target_image = detector.findPose(target_image)
            lmList, patient = detector.findPosition(target_image)

            if not patient:
                continue

            # 사이각 구하기 공식
            angleManager.GetAngle(lmList, patientAngle)
            angleManager.GetAverageAngle(lmList, patientAngle)
            angleManager.ComparePose(teacherAngle, patientAngle, scoreAngle)
            # cos유사도
            angleManager.GetAverageJoint(lmList, poselist)
            similarity = angleManager.GetSimiarityCos(teacherAngle, poselist)

        print(scoreAngle)
        print(similarity)
        cap.release()
        cv2.destroyAllWindows()

        # 스켈레톤이 입혀진 새로운 동영상 저장
        new_file_patient=await self.save_mp4(file_name_patient,file_name_doctor+"/"+doctor_video_list[2])

        with open(new_file_patient, "rb") as file:
            file_obj = File(file)
            patientpic.picturefilename = file_obj

            score = round((sum(scoreAngle.values()) / 8 + similarity * 100) / 2, 0)
            print(score)
            patientpic.score = score
            patientpic.save()

        print("스켈레톤이 적용된 파일이 생성되었습니다." + str(patientpic.picturefilename))

        await self.send(text_data=json.dumps({
            'type': 'return value',
            'message': score
        }))

    async def connect(self):
        # 웹소켓 연결이 이루어질 때 실행되는 메서드
        # 연결을 받고 처리할 준비를 할 수 있습니다.
        print("웹소켓에 연결되었습니다.")

        # websocket 연결
        await self.accept()

        # 소켓에 연결되었음을 프론트에 알림
        await self.send(text_data=json.dumps({
            'message': "socket connected"
        }))

    async def disconnect(self, close_code):
        # 웹소켓 연결이 종료될 때 실행되는 메서드
        print("해제됩니다.")
        if close_code == 1000:
            await self.close()

    async def receive(self, text_data=None, bytes_data=None):
        # 웹소켓으로부터 메시지를 수신받을 때 실행되는 메서드
        # 수신한 데이터를 처리하고 응답을 보낼 수 있습니다.
        data = json.loads(text_data)
        patient_id = data['patient_id']
        exercise_name = data['exercise_name']
        exercise_type = data['exercise_type']
        video_data = data['video_data']

        video_data = video_data[23:]

        # 비디오 저장 & 점수계산
        await self.save_video(patient_id, exercise_name, exercise_type, video_data)

        # 응답을 보낼 때는 send() 메서드를 사용합니다.
        await self.send(text_data='Video saved successfully.')

        # 소켓 종료
        await self.disconnect(1000)
