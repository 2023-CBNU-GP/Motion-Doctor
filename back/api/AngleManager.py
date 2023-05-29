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



    #cos 유사도는 각 벡터 사이의 유사도를 확인함...
    #teacher의 x,y좌표와 환자의 x,y좌표에 대해 우사도를 해야하나..?
    def GetSimiarityCos(self,TeacherJoint,PatientJoint):

        for i in range(len(TeacherJoint)) :
            dot_product=np.dot(TeacherJoint[i],PatientJoint[i])

            l2_norm =(np.sqrt(sum(np.square(TeacherJoint[i])))*np.sqrt(sum(np.square(PatientJoint[i]))))
            similarity = dot_product/l2_norm

            print(similarity)

    def GetAngle(self,joints,AngleList):

        Angle={"LelbowAngle":[14,16,12],"LshoulderAngle":[12,14,24],"RelbowAngle":[13,11,15],"RshoulderAngle":[11,13,23]
            ,"Lhip":[24,23,26],"Rhip":[23,24,25],"Lknee":[25,23,27],"Rknee":[26,24,28]}

        i=0
        for key,value in Angle.items():
            center,left,right=value
            AngleList[key]= self.GetJointAngle(joints[center],joints[left],joints[right])
            i+=1

        return AngleList

    def ComparePose(self,TeacherAngle,PatientAngle) :
        scoreAngle={}

        for key,value in TeacherAngle.items():
            angle=abs(float(value)-PatientAngle[key])
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

        print(scoreAngle)
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

    def GetAvgAngle(self,fileName):
        file_path="DoctorAngle.json"
        #json파일이 없을시 예외발생, json파일 생성 후, 처음 들어온 데이터 저장. 이후 부터는 try문을 통해 예외발생 안함.
        with open(file_path) as json_file:
            json_data=json.load(json_file)

        return json_data[fileName]
