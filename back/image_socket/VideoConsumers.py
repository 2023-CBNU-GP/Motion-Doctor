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
    async def find(self, cap):
        return cap.read()

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
                print("파일이 생성되었습니다.")

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

        # 환자 모션 영상을 프론트에서 보내면 이것이 media 폴더에 저장됨.
        # media 폴더에 있는 영상을 인공지능 모델에 연결시켜서 결과값을 리턴해야하는데
        # 이때 프론트에서 새롭게 연결한 웹소켓으로 결과값을 전송하는 것
        print("work")

        correctpic = Correctpic.objects.filter(exercisetype=exercise_type, exercisename=exercise_name).first()
        patientpic = Patientpic.objects.filter(correctpicid=correctpic).first()
        # while True:
        #     patientpic = Patientpic.objects.filter(correctpicid=correctpic).first()
        #     print(patientpic)
        #     if patientpic is not None:
        #         print("탈출합니다.")
        #         break

        # 여기에 파이썬 모델로 영상을 전송하여 결과 score를 저장
        file_name_patient = "media/" + str(patientpic.picturefilename)  # 소켓으로 전달된 환자 파일
        # file_name_patient ="madia/patient/3/jiu3159-팔들어올리기-PAUROZPQME.mp4"
        print(file_name_patient)
        cap = cv2.VideoCapture(file_name_patient)
        pTime = 0
        detector = PoseDetector()

        frameCount = cap.get(cv2.CAP_PROP_FRAME_COUNT)

        patientAngle = {"LelbowAngle": 0, "LshoulderAngle": 0, "RelbowAngle": 0, "RshoulderAngle": 0
            , "Lhip": 0, "Rhip": 0, "Lknee": 0, "Rknee": 0}
        scoreAngle = {"LelbowAngle": 0, "LshoulderAngle": 0, "RelbowAngle": 0, "RshoulderAngle": 0
            , "Lhip": 0, "Rhip": 0, "Lknee": 0, "Rknee": 0}
        angleManager = AngleManager()

        doctor_video_list = str(correctpic.picturefilename).split('/')
        teacherAngle = angleManager.GetAvgAngle("media/" + doctor_video_list[0] + "/" + doctor_video_list[1],
                                                doctor_video_list[2])  # 의사 파일명

        # 의사 파일 가져오는 코드
        file_name_doctor = "media/" + str(correctpic.picturefilename)  # 소켓으로 전달된 환자 파일
        cap1 = cv2.VideoCapture(file_name_doctor)
        detector1 = PoseDetector()  # 의사용
        similarity = 0.0

        poselist = {11: [0, 0], 12: [0, 0], 13: [0, 0], 14: [0, 0], 15: [0, 0], 16: [0, 0], 23: [0, 0], 24: [0, 0],
                    25: [0, 0], 26: [0, 0], 27: [0, 0], 28: [0, 0]}
        ##저장용
        w = round(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        h = round(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        fps = cap.get(cv2.CAP_PROP_FPS)
        print("환자 ", fps)
        fps1 = cap1.get(cv2.CAP_PROP_FPS)
        print("의사 ", fps1)

        # mp4확장자 선택을 위함
        fourcc = cv2.VideoWriter_fourcc(*'DIVX')
        # 앞 string 파일 이름
        out=cv2.VideoWriter(file_name_patient,fourcc, 30, (w, h))

        while True:
            success, target_image = await self.find(cap)
            _, skeleton_image = await self.find(cap1)

            if target_image is None:
                break

            if skeleton_image is None:
                break

            target_image = detector.findPose(target_image)
            skeleton_image = detector1.findPose(skeleton_image)

            lmList, patient = detector.findPosition(target_image)
            _, doctor = detector1.findPosition(skeleton_image)

            if not doctor or not patient:
                continue

            angleManager.adjustStd(patient, doctor)
            angleManager.transPos(patient[0][0] - doctor[0][0], patient[0][1] - doctor[0][1], doctor)
            target_image = detector1.drawPose(target_image, doctor, 100)
            out.write(target_image) #data저장용
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
        out.release()
        cap1.release()
        cv2.destroyAllWindows()
        score = round((sum(scoreAngle.values()) / 8 + similarity * 100) / 2, 0)
        print(score)
        patientpic.score = score
        patientpic.save()

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

        # 비디오 저장
        await self.save_video(patient_id, exercise_name, exercise_type, video_data)

        # 응답을 보낼 때는 send() 메서드를 사용합니다.
        await self.send(text_data='Video saved successfully.')

        await self.disconnect(1000)
