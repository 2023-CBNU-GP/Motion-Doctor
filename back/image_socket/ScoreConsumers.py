import json
from channels.generic.websocket import WebsocketConsumer
import cv2

import sys
sys.path.append("..")
from api.AngleManager import *
from api.PoseDetector import *


# 환자 모션 영상을 프론트에서 보내면 이것이 media 폴더에 저장됨.
# media 폴더에 있는 영상을 인공지능 모델에 연결시켜서 결과값을 리턴해야하는데
# 이때 프론트에서 새롭게 연결한 웹소켓으로 결과값을 전송하는 것
# 이 결과값을 전송하기 위한 Consumer
class ScoreConsumers(WebsocketConsumer):
    # websocket에 연결되면 호출되는 메소드
    def connect(self):
        print("웹소켓에 연결되었습니다.")

        # websocket 연결
        self.accept()

        # 여기에 파이썬 모델로 영상을 전송하여 결과 score를 저장
        file_name = "media/doctor/13/JKZHFLNUPS.mp4" # 소켓으로 전달된 환자 파일
        cap = cv2.VideoCapture(file_name)
        pTime = 0
        detector = PoseDetector()

        frameCount = cap.get(cv2.CAP_PROP_FRAME_COUNT)
        patientAngle = {"LelbowAngle": 0, "LshoulderAngle": 0, "RelbowAngle": 0, "RshoulderAngle": 0
            , "Lhip": 0, "Rhip": 0, "Lknee": 0, "Rknee": 0}
        scoreAngle = {"LelbowAngle": 0, "LshoulderAngle": 0, "RelbowAngle": 0, "RshoulderAngle": 0
            , "Lhip": 0, "Rhip": 0, "Lknee": 0, "Rknee": 0}
        angleManager = AngleManager()

        teacherAngle = angleManager.GetAvgAngle("media/doctor/13/","JKZHFLNUPS.mp4") #의사 파일명

        poselist = {11: [0, 0], 12: [0, 0], 13: [0, 0], 14: [0, 0], 15: [0, 0], 16: [0, 0], 23: [0, 0], 24: [0, 0],
                    25: [0, 0], 26: [0, 0], 27: [0, 0], 28: [0, 0]}

        similarity = 0.0
        while True:
            success, img = cap.read()

            Curframe = cap.get(cv2.CAP_PROP_POS_FRAMES)

            if Curframe >= frameCount / 3 and Curframe <= frameCount - frameCount / 3:  # 현재 프레임 수를 확인 후, 지정된 프레임 이상일 시 동영상에서 스켈렙톤 뽑아내기
                img = detector.findPose(img)
                lmList = detector.findPosition(img)

                # 사이각 구하기 공식
                angleManager.GetAngle(lmList, patientAngle)
                angleManager.GetAverageAngle(lmList, patientAngle)
                angleManager.ComparePose(teacherAngle, patientAngle, scoreAngle)
                # cos유사도
                angleManager.GetAverageJoint(lmList, poselist)
                similarity = angleManager.GetSimiarityCos(teacherAngle, poselist)

            if img is None:
                break

        print(scoreAngle)
        print(similarity)

        score = 0

        # 결과값을 프론트에 알림
        self.send(text_data=json.dumps({
            'type': 'connection established',
            'message': score
        }))

    # websocket 연결이 해제되면 호출되는 메소드
    def disconnect(self, close_code):
        print("해제되었습니다.")
