import json
from channels.generic.websocket import AsyncWebsocketConsumer
import cv2

import sys
sys.path.append("..")
from api.AngleManager import *
from api.PoseDetector import *
from api.models import *


# 환자 모션 영상을 프론트에서 보내면 이것이 media 폴더에 저장됨.
# media 폴더에 있는 영상을 인공지능 모델에 연결시켜서 결과값을 리턴해야하는데
# 이때 프론트에서 새롭게 연결한 웹소켓으로 결과값을 전송하는 것
# 이 결과값을 전송하기 위한 Consumer
class ScoreConsumers(AsyncWebsocketConsumer):
    # websocket에 연결되면 호출되는 메소드
    async def connect(self):
        print("웹소켓에 연결되었습니다.")

        # websocket 연결
        await self.accept()

        # 소켓에 연결되었음을 프론트에 알림
        await self.send(text_data=json.dumps({
            'message': "socket connected"
        }))

    # websocket 연결이 해제되면 호출되는 메소드
    async def disconnect(self, close_code):
        print("해제됩니다.")
        if close_code == 1000:
            await self.close()

    async def receive(self, text_data=None, bytes_data=None):
        if text_data:
            await self.handle_text_data(text_data)
            # 결과값을 프론트에 알림

    async def handle_text_data(self, text_data):
        print("work")
        body = json.loads(text_data)
        correctpic = Correctpic.objects.filter(exercisetype=body['type']).first()

        while True:
            patientpic = Patientpic.objects.filter(correctpicid=correctpic.uid).last()
            print(patientpic)
            if patientpic is not None:
                print("탈출합니다.")
                break

        # 여기에 파이썬 모델로 영상을 전송하여 결과 score를 저장
        file_name_patient = "media/" + str(patientpic.picturefilename)  # 소켓으로 전달된 환자 파일
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
        teacherAngle = angleManager.GetAvgAngle("media/"+doctor_video_list[0]+"/"+doctor_video_list[1], doctor_video_list[2])  # 의사 파일명

        # 의사 파일 가져오는 코드
        file_name_doctor = "media/" + str(correctpic.picturefilename)  # 소켓으로 전달된 환자 파일
        cap1 = cv2.VideoCapture(file_name_doctor)
        detector1 = PoseDetector()  # 의사용
        similarity = 0.0

        poselist = {11: [0, 0], 12: [0, 0], 13: [0, 0], 14: [0, 0], 15: [0, 0], 16: [0, 0], 23: [0, 0], 24: [0, 0],
                    25: [0, 0], 26: [0, 0], 27: [0, 0], 28: [0, 0]}

        while True:
            success, img = cap.read()
            _,doctorFrame = cap1.read()

            if img is None:
                break

            if doctorFrame is None:
                break

            Curframe = cap.get(cv2.CAP_PROP_POS_FRAMES)
            #두 이미지의 크기 정규화 : 의사의 이미지 -> 환자의 이미지 크기로 키우거나 줄임.
            skeleton_image = cv2.resize(doctorFrame, (img.shape[1], img.shape[0]))

            if Curframe >= frameCount / 3 and Curframe <= frameCount - frameCount / 3:  # 현재 프레임 수를 확인 후, 지정된 프레임 이상일 시 동영상에서 스켈렙톤 뽑아내기
                img = detector.findPose(img)
                doctorFrame = detector1.findPose(doctorFrame)

                lmList,patient = detector.findPosition(img)
                _, doctor = detector1.findPosition(doctorFrame)

                angleManager.adjustStd(patient,doctor)
                # 사이각 구하기 공식
                angleManager.GetAngle(lmList, patientAngle)
                angleManager.GetAverageAngle(lmList, patientAngle)
                angleManager.ComparePose(teacherAngle, patientAngle, scoreAngle)
                # cos유사도
                angleManager.GetAverageJoint(lmList, poselist)
                similarity = angleManager.GetSimiarityCos(teacherAngle, poselist)

        print(scoreAngle)
        print(similarity)

        score = round((sum(scoreAngle.values())/8 + similarity*100)/2, 0)
        print(score)
        patientpic.score=score
        patientpic.save()

        await self.send(text_data=json.dumps({
                        'type': 'return value',
                        'message': score
                        }))