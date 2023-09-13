import cv2
import PoseDetector as pd
import AngleManager as af


class OpencvManager:
    def __init__(self):
        detector=pd.PoseDetector()
        AngleManager=af.AngleManager()

    def doctorManage(self,file_name):
        cap = cv2.VideoCapture(file_name)

        teacherAngle= {"LelbowAngle":0,"LshoulderAngle":0,"RelbowAngle":0,"RshoulderAngle":0
            ,"Lhip":0,"Rhip":0,"Lknee":0,"Rknee":0}

        frameCount=cap.get(cv2.CAP_PROP_FRAME_COUNT)
        while True:
            success, img = cap.read()

            Curframe = cap.get(cv2.CAP_PROP_POS_FRAMES)
            if Curframe >= frameCount / 3 and Curframe <= frameCount - frameCount / 3:  # 현재 프레임 수를 확인 후, 지정된 프레임 이상일 시 동영상에서 스켈렙톤 뽑아내기
                img = self.detector.findPose(img)
                lmList = self.detector.findPosition(img)
                self.AngleManager.GetAngle(lmList, teacherAngle)
                # 의사용, 환자의 경우 실시간으로 비교가 일어나야하므로 필요없음.
                self.AngleManager.GetAverageAngle(lmList, teacherAngle)

            if img is None:
                break

        for i,value in teacherAngle.items():
            teacherAngle[i]=round(value/(frameCount/3),2)
        self.AngleManager.TransferJsonFile(file_name)

    def patientManage(self,file_name):
        cap = cv2.VideoCapture(file_name)

        Angle= {"LelbowAngle":0,"LshoulderAngle":0,"RelbowAngle":0,"RshoulderAngle":0
            ,"Lhip":0,"Rhip":0,"Lknee":0,"Rknee":0}

        frameCount=cap.get(cv2.CAP_PROP_FRAME_COUNT)
        while True:
            success, img = cap.read()

            Curframe = cap.get(cv2.CAP_PROP_POS_FRAMES)
            if Curframe >= frameCount / 3 and Curframe <= frameCount - frameCount / 3:  # 현재 프레임 수를 확인 후, 지정된 프레임 이상일 시 동영상에서 스켈렙톤 뽑아내기
                img = self.detector.findPose(img)
                lmList,patient = self.detector.findPosition(img)
                self.AngleManager.GetAngle(lmList, Angle)
                print(Angle) #환자 주요 사이각 출력

            if img is None:
                break
