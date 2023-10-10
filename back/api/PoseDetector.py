import mediapipe as mp
import cv2

class PoseDetector() :

    def __init__(self, mode=False, model_complexity=1, smooth_landmarks=True,
                 upper=False, smooth=True, detectionCon=0.5, trackCon=0.5):

        self.mode = mode
        self.smooth = smooth
        self.upper=upper
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.model_complexity=model_complexity
        self.smooth_landmarks=smooth_landmarks

        self.mpDraw = mp.solutions.drawing_utils
        self.mpPose = mp.solutions.pose
        self.pose = self.mpPose.Pose(self.mode, self.model_complexity, self.smooth_landmarks,
                                     self.upper, self.smooth, self.detectionCon, self.trackCon)

    def findPose(self,img,draw=True):
        imgRGB = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        self.results = self.pose.process(imgRGB)

        return img
    
        #좌표를 그리는 함수인데, 하나만 가져가면 된다. 아래 하나는 임시 시험용 ... 색을 다르게하기 위함
    def drawPose(self,img,out,pose,color,draw=True):
        thresh=[[12,14],[14,16],[11,13],[13,15],[12,24],[11,23],[24,26],[26,28],[23,25],[25,27],[28,32],[28,30],[27,29],[27,31]]
        imgRGB = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        self.results = self.pose.process(imgRGB)

        for id, landmark in enumerate(pose) :
            cx,cy = landmark[0],landmark[1] #해당 지점에 대한 x,y좌표를 찾아냄.
            cv2.circle(img,(int(cx),int(cy)),5,(0,0,color),thickness=-1,lineType=cv2.LINE_8) #그려지는 원형이 작아짐.

        for idx in range(len(thresh)) :
            #print(landmark)
            cv2.line(img,list(map(int, pose[thresh[idx][0]])),list(map(int, pose[thresh[idx][1]])),(0,0,color),8)

        return img
    

    def findPosition(self,img,draw=True):
        lmList=[]
        PoseList=[]
        if self.results.pose_landmarks:
            for id, landmark in enumerate(self.results.pose_landmarks.landmark) :
                h,w,c=img.shape
                cx,cy = int(landmark.x*w),int(landmark.y*h)
                lmList.append([id, cx, cy])
                PoseList.append([cx,cy])

        return lmList,PoseList

