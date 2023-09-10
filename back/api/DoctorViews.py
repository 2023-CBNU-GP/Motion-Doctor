from rest_framework.exceptions import AuthenticationFailed
from rest_framework.views import APIView
import jwt
from rest_framework.response import Response

from .models import *
import json


# 의사가 comment를 부여하기 위한 api
class DoctorComment(APIView):
    def post(self, request):
        token = request.COOKIES.get('jwt')
        body = json.loads(request.body.decode('utf-8'))

        if not token:
            raise AuthenticationFailed("Unauthenticated!")

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Unauthenticated!")

        doctor = Doctor.objects.filter(id=payload["id"]).first()

        comment = Doctorcomment()
        comment.text = body["text"]
        comment.doctorid = doctor

        # 환자 영상 링크 전체를 보내줄 때
        comment.pictureid = Patientpic.objects.filter(picturefilename=body['video']).first()

        # 재활코스 타입과 이름으로 보내줄 때
        #correctpic = Correctpic.objects.filter(exercisetype=body['type'], exercisename=body['name']).first()
        #patientpic_list = Patientpic.objects.filter(correctpicid=correctpic)

        #for patientpic in patientpic_list:
        #    file_name = str(patientpic.picturefilename).split('/')[2].split('-')[2]
        #    if file_name[:10] == body['idx']:
        #        comment.pictureid = patientpic
        #        break

        comment.save()

        response = Response()
        response.data = {
            'message': 'success'
        }

        return response


# 특정 의사가 본인의 재활 코스를 수강한 환자 목록 리턴하는 api
class ManagePatientList(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed("Unauthenticated!")

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Unauthenticated!")

        doctor = Doctor.objects.filter(id=payload["id"]).first()

        manage_list = Manage.objects.filter(doctorid=doctor)

        i = 1
        data_list = []
        for manage in manage_list:
            patient = Patient.objects.filter(uid=manage.patientid.uid).first()
            patientpic_list = Patientpic.objects.filter(patientid=manage.patientid)

            type_dict = {}
            for patientpic in patientpic_list:
                correctpic = Correctpic.objects.filter(uid=patientpic.correctpicid.uid).first()

                if type_dict.get(correctpic.exercisetype) is None:
                    type_dict[correctpic.exercisetype] = 1
                else:
                    type_dict[correctpic.exercisetype] += 1

            type_list = list(type_dict.keys())

            k=0
            for j in range(len(type_dict)):
                isCounseled = True
                for _ in range(type_dict[type_list[j]]):
                    comment = Doctorcomment.objects.filter(pictureid=patientpic_list[k].uid).first()
                    if comment is None:
                        isCounseled = False
                    k+=1

                data = {
                    "_id": i,
                    "uid": patient.uid,
                    "patientName": patient.name,
                    "trainCourse": type_list[j].split('-')[0],
                    "isCounseled": isCounseled
                }
                data_list.append(data)
                i += 1

        return Response({'data': data_list})


# 특정 의사가 특정 환자의 재활 테스트 영상 보기 위한 정보
class PatientTestList(APIView):
    def post(self, request, uid):
        token = request.COOKIES.get('jwt')
        body = json.loads(request.body.decode('utf-8'))

        if not token:
            raise AuthenticationFailed("Unauthenticated!")

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Unauthenticated!")

        patient = Patient.objects.filter(uid=uid).first()
        correctpic_list = Correctpic.objects.filter(exercisetype=body["type"])

        i=0
        data_list=[]
        for correctpic in correctpic_list:
            videoList, scoreList = [], []
            name, type = '', ''
            patientpic = Patientpic.objects.filter(correctpicid=correctpic.uid, patientid=patient.uid)

            if not patientpic.exists():
                break

            for pic in patientpic:
                videoList.append(str(pic.picturefilename))
                scoreList.append(pic.score)

            type = correctpic.exercisetype
            name=correctpic.exercisename

            data = {
                "_id": i+1,
                "patientName": patient.name,
                "trainTitle": type.split('-')[0],
                "trainName": name,
                "videoList": videoList,
                "scoreList": scoreList
            }
            data_list.append(data)
            i+=1

        return Response({'data': data_list})


# 특정 의사가 본인이 올린 전체 영상 확인하는 API
class DoctorVideo(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed("Unauthenticated!")

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Unauthenticated!")

        doctor = Doctor.objects.filter(id=payload["id"]).first()
        video_list = Correctpic.objects.filter(doctorid=doctor.uid)

        type_dict = {}
        name_list = []
        for video in video_list:
            if type_dict.get(video.exercisetype) is None:
                type_dict[video.exercisetype] = 1
            else:
                type_dict[video.exercisetype] += 1

            name_list.append(video.exercisename)

        type_list = list(type_dict.keys())

        data_list = []
        j=0
        for i in range(len(type_dict)):
            num = []
            for _ in range(type_dict[type_list[i]]):
                num.append(name_list[j])
                j += 1

            data = {
                "_id": i+1,
                "type": type_list[i],
                "name": num,
                "num": type_dict[type_list[i]]
            }
            data_list.append(data)

        return Response({'data': data_list})
