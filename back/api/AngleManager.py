import math
import json
import numpy as np

class AngleManager():

    def GetJointAngle(self,CenterPos,jointPos1, jointPos2) :

        theta1=math.atan2((jointPos1[2]-CenterPos[2]), (jointPos1[1]-CenterPos[1]))
        theta2=math.atan2((jointPos2[2]-CenterPos[2]), (jointPos2[1]-CenterPos[1]))

        degree= abs(theta2-theta1)*180/math.pi

        return round(degree,3)

    #dictionary로 바꾸자.
    def GetAverageAngle(self,joints1,AngleSum): #두 영상으로 비교 예정...

        Angle={"LelbowAngle":[14,16,12],"LshoulderAngle":[12,14,24],"RelbowAngle":[13,11,15],"RshoulderAngle":[11,13,23]
            ,"Lhip":[24,23,26],"Rhip":[23,24,25],"Lknee":[25,23,27],"Rknee":[26,24,28]}
        i=0
        for key,value in Angle.items():
            center,left,right=value
            AngleSum[key]+= self.GetJointAngle(joints1[center],joints1[left],joints1[right])
            i+=1

    def GetAverageJoint(self,lmList,poselist):
        # 각도 구하는 공식 다시 생각하기...

        for i in range(len(lmList)):

            id,x,y=lmList[i]

            if id in poselist :
                xx,yy=poselist[id]
                poselist[id]=[xx+x,yy+y]

#벡터 1로 정규화
## 12번을 기준으로 벡터 1로 만들어 정규화 해볼 예정

## 1. 기준벡터(의사의 좌표값)을 벡터 1로 정규화한다.
## 2. 의사의 크기/크기 1을 나눈 n배수를 구한다.
## 3. 환자의 x,y값을 벡터 1값을 가지는 x,y좌표로 바꾼다. (x/dist,y/dist)
## 4. 의사의 n배수를 곱하면, 두 크기가 같아진다?
## ** 의사를 환자한테 맞춘다. 환자 영상을 볼 수 있기 때문 ?

#######
# 12 - 14 | 14 - 16
# 11 - 13 | 13 - 15
# 12 - 24 | 11 - 23
# 24 - 26 | 26 - 28
# 23 - 25 | 25 - 27
#######
    def adjustStd(self,patient, doctor):

        thresh=[[12,14],[14,16],[11,13],[13,15],[12,24],[11,23],[24,26],[26,28],[23,25],[25,27],[28,32],[28,30],[27,29],[27,31]]
        #thresh의 리스트 idx번에 해당하는 x,y좌표 리스트를 numpy화
        #patient Standard 의 줄인말로, 환자 기준치를 의미한다.

        for idx in range(len(thresh)) :
            patiStd1 = np.array(patient[thresh[idx][0]])
            patiStd2 = np.array(patient[thresh[idx][1]])
            patiDist=np.linalg.norm(patiStd1-patiStd2) # 두 좌표간의 길이을 측정하는 함수

            doctStd1 = np.array(doctor[thresh[idx][0]])
            doctStd2 = np.array(doctor[thresh[idx][1]])
            doctDist=np.linalg.norm(doctStd1-doctStd2)

            newDoct2=doctStd1+((doctStd2-doctStd1)/doctDist)*patiDist
            doctor[thresh[idx][1]]=newDoct2 #새로운 값으로 초기화
        return doctor

#의사 Pose 좌표를 평행이동한다.
    def transPos(self,thresX,thresY,doctor):

        for idx in range(len(doctor)):
            doctor[idx][0]+=thresX
            doctor[idx][1]+=thresY

        return doctor
    # cos 유사도는 각 벡터 사이의 유사도를 확인함...
    # teacher의 x,y좌표와 환자의 x,y좌표에 대해 우사도를 해야하나..?
    def GetSimiarityCos(self, TeacherJoint, PatientJoint):
        poselist = [11, 12, 13, 14, 15, 16, 23, 24, 25, 26, 27, 28]

        for i in range(len(PatientJoint)):
            dot_product = np.dot(TeacherJoint[str(poselist[i])], PatientJoint[poselist[i]])
            l2_norm = (np.sqrt(sum(np.square(TeacherJoint[str(poselist[i])]))) * np.sqrt(
                sum(np.square(PatientJoint[poselist[i]]))))
            similarity = dot_product / l2_norm

        return similarity

    def GetAngle(self,joints,AngleList):

        Angle={"LelbowAngle":[14,16,12],"LshoulderAngle":[12,14,24],"RelbowAngle":[13,11,15],"RshoulderAngle":[11,13,23]
            ,"Lhip":[24,23,26],"Rhip":[23,24,25],"Lknee":[25,23,27],"Rknee":[26,24,28]}

        i=0
        for key,value in Angle.items():
            center,left,right=value
            AngleList[key]= self.GetJointAngle(joints[center],joints[left],joints[right])
            i+=1

        return AngleList

    def ComparePose(self,TeacherAngle,PatientAngle,scoreAngle):

        for key,value in scoreAngle.items():
            angle=abs(TeacherAngle[key]-PatientAngle[key])
            if angle <= 10 :
                 scoreAngle[key]=100
            elif angle <= 20 :
                scoreAngle[key]=90
            elif angle <= 30 :
                scoreAngle[key]=80
            elif angle <= 40 :
                scoreAngle[key]=70
            else:
                scoreAngle[key]=60

        return scoreAngle


    def TransferJsonFile(self,folderName,fileName,avgJointList=None,avgAngleList=None):
        #file 경로 지정
        file_path=folderName+"/DoctorAngle.json"
        #json파일이 없을시 예외발생, json파일 생성 후, 처음 들어온 데이터 저장. 이후 부터는 try문을 통해 예외발생 안함.
        try:

            with open(file_path) as json_file:
                json_data=json.load(json_file)

                dic=self.StoreAvgAngle(fileName,avgJointList,avgAngleList)

                json_data.update(dic)
                print(json_data)

                with open(file_path,'w') as make_file :
                    json.dump(json_data,make_file,indent='\t')

        except :
            dic=self.StoreAvgAngle(fileName,avgJointList,avgAngleList)

            with open(file_path,'w') as make_file :
                json.dump(dic,make_file,indent='\t')
#poselist={11:[0,0],12:[0,0],13:[0,0],14:[0,0],15:[0,0],16:[0,0],23:[0,0],24:[0,0],25:[0,0],26:[0,0],27:[0,0],28:[0,0]}
    def StoreAvgAngle(self,fileName,avgJointList,avgAngleList):
        dic={}
        dic[fileName]={'11':avgJointList[11],'12':avgJointList[12],'13':avgJointList[13],'14':avgJointList[14],'15':avgJointList[15],'16':avgJointList[16],'23':avgJointList[23],'24':avgJointList[24],'25':avgJointList[25],
                       '26':avgJointList[26],'27':avgJointList[27],'28':avgJointList[28],
                    'LelbowAngle':avgAngleList['LelbowAngle'],'LshoulderAngle':avgAngleList['LshoulderAngle'],
                    'RelbowAngle':avgAngleList['RelbowAngle'],'RshoulderAngle':avgAngleList['RshoulderAngle'],
                    'Lhip':avgAngleList['Lhip'],'Rhip':avgAngleList['Rhip'],
                    'Lknee':avgAngleList['Lknee'],'Rknee':avgAngleList['Rknee']
        }

        return dic

    def GetAvgAngle(self,filePath,fileName):

        #json파일이 없을시 예외발생, json파일 생성 후, 처음 들어온 데이터 저장. 이후 부터는 try문을 통해 예외발생 안함.
        with open(filePath+"/DoctorAngle.json") as json_file:
            json_data=json.load(json_file)

        return json_data[fileName]
