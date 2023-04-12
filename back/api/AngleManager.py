import math
import json

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

        return AngleSum

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


    def TransferJsonFile(self,fileName,avgAngleList=None):
        #file 경로 지정
        file_path="DoctorAngle.json"
        #json파일이 없을시 예외발생, json파일 생성 후, 처음 들어온 데이터 저장. 이후 부터는 try문을 통해 예외발생 안함.
        try:

            with open(file_path) as json_file:
                json_data=json.load(json_file)

                dic=self.StoreAvgAngle(fileName,avgAngleList)

                json_data.update(dic)
                print(json_data)

                with open(file_path,'w') as make_file :
                    json.dump(json_data,make_file,indent='\t')

        except :
            dic=self.StoreAvgAngle(fileName,avgAngleList)

            with open(file_path,'w') as make_file :
                json.dump(dic,make_file,indent='\t')

    def StoreAvgAngle(self,fileName,avgAngleList):
        dic={}
        dic[fileName]={
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
