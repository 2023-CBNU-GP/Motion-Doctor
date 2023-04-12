import mediapipe as mp
import cv2

class PoseDetector() :

    def __init__(self, mode=False,upper=False,
                 smooth=True,detectionCon=0.5, trackCon=0.5):

        self.mode = mode
        self.smooth = smooth
        self.upper=upper
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpDraw = mp.solutions.drawing_utils
        self.mpPose = mp.solutions.pose
        self.pose = self.mpPose.Pose(self.mode, self.upper,
                                     self.smooth,self.detectionCon, self.trackCon)

    def findPose(self,img,draw=True):
        imgRGB = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        self.results = self.pose.process(imgRGB)
        #print(results.pose_landmarks)
        if self.results.pose_landmarks :
            if draw:
                self.mpDraw.draw_landmarks(img,self.results.pose_landmarks,
                                            self.mpPose.POSE_CONNECTIONS)

        return img

    def findPosition(self,img,draw=True):
        lmList=[]
        if self.results.pose_landmarks:
            for id, landmark in enumerate(self.results.pose_landmarks.landmark) :
                h,w,c=img.shape
                cx,cy = int(landmark.x*w),int(landmark.y*h)
                lmList.append([id, cx, cy])

                if draw :
                    cv2.circle(img,(cx,cy),5,(255,0,0),cv2.FILLED) #그려지는 원형이 작아짐.

        return lmList

