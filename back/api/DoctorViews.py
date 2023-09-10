from rest_framework.exceptions import AuthenticationFailed
from rest_framework.views import APIView
import jwt
from rest_framework.response import Response

from .models import *
import json
from django.db.models import Avg

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

        correctpic = Correctpic.objects.filter(exercisetype=body['type'], exercisename=body['name']).first()
        patientpic_list = Patientpic.objects.filter(correctpicid=correctpic)

        for patientpic in patientpic_list:
            file_name = str(patientpic.picturefilename).split('/')[2].split('-')[2]
            if file_name[:10] == body['idx']:
                comment.pictureid = patientpic
                break
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

        # 여기도 DB 수정 필요
        # PatientPic에 exerciseType 추가하는 것이 좋아보임.
        # 원래 같은 Type은 하나로 표시되어야하는데, 일단 다 표시되도록 하였음.
        for manage in manage_list:
            patient = Patient.objects.filter(uid=manage.patientid.uid).first()
            patientpic_list = Patientpic.objects.filter(patientid=manage.patientid)
            for patientpic in patientpic_list:
                correctpic = Correctpic.objects.filter(uid=patientpic.correctpicid.uid).first()
                type = correctpic.exercisetype
                comment = Doctorcomment.objects.filter(pictureid=patientpic.uid).first()
                if comment is None:
                    isCounseled = False
                else:
                    isCounseled = True

                data = {
                    "_id": i,
                    "patientName": patient.name,
                    "trainCourse": type.split('-')[0],
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
                "trainList": name,
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
        for video in video_list:
            if type_dict.get(video.exercisetype) is None:
                type_dict[video.exercisetype] = 1
            else:
                type_dict[video.exercisetype] += 1

        type_list = list(type_dict.keys())

        data_list = []
        for i in range(len(type_dict)):
            data = {
                "_id": i+1,
                "type": type_list[i].split('-')[0],
                "num": type_dict[type_list[i]]
            }
            data_list.append(data)

        return Response({'data': data_list})
