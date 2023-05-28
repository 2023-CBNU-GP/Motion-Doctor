from rest_framework.exceptions import AuthenticationFailed
from rest_framework.views import APIView
import jwt
from rest_framework.response import Response

from .models import *
import json


# 의사가 comment를 부여하기 위한 api
# DB 수정!
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

        # 여기서 pictureId는 patientPic을 가리키도록 되어 있는데
        # 하나의 exerciseType(큰 운동)에 여러 개의 exerciseName이 있고, 각 exerciseName마다 patientPic이 존재.
        # 따라서 DB에 논리적인 오류가 있는 듯함. 일단은 여러 개의 exerciseName마다 comment를 만들었다. 나중에 수정예정.
        correctpic_list = Correctpic.objects.filter(exercisetype=body['type'])
        for correctpic in correctpic_list:
            comment = Doctorcomment()
            comment.text = body["text"]
            comment.doctorid = doctor
            comment.pictureid = Patientpic.objects.filter(correctpicid=correctpic).first()
            comment.save()

        response = Response()
        response.data = {
            'message': 'success'
        }

        return response


# 특정 의사가 본인의 재활 코스를 수강한 환자 목록 리턴하는 api
# DB 수정!
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


# 특정 환자가(자신이) 테스트한 재활 코스 전체 목록 확인하는 api
class DoctorPatientList(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed("Unauthenticated!")

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Unauthenticated!")

        patient = Patient.objects.filter(id=payload["id"]).first()

        patientpic_list = Patientpic.objects.filter(patientid=patient)
        type_dict = {}
        type_list = []
        for patientpic in patientpic_list:
            correctpic = Correctpic.objects.filter(uid=patientpic.correctpicid.uid).first()
            if type_dict.get(correctpic.exercisetype) is None:
                type_dict[correctpic.exercisetype] = 1
                type_list.append(True)
            else:
                type_dict[correctpic.exercisetype] += 1
                type_list.append(False)

        data_list = []
        i,j=1,0
        for patientpic in patientpic_list:
            if type_list[j]:
                correctpic = Correctpic.objects.filter(uid=patientpic.correctpicid.uid).first()
                doctor = Doctor.objects.filter(uid=correctpic.doctorid.uid).first()
                comment = Doctorcomment.objects.filter(pictureid=patientpic.uid).first()
                if comment is None:
                    text = None
                else:
                    text = comment.text
                data = {
                    "_id": i,
                    "trainTitle": correctpic.exercisetype.split('-')[0],
                    "trainNum": type_dict[correctpic.exercisetype],
                    "doctorName": doctor.name,
                    "hospitalName": doctor.hospitalname,
                    "counselResult": text
                }
                data_list.append(data)
                i += 1
                j += 1
            else:
                j += 1

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

        name, videoList, scoreList = [], [], []
        type=''
        for correctpic in correctpic_list:
            patientpic = Patientpic.objects.filter(correctpicid=correctpic.uid).first()
            type = correctpic.exercisetype
            name.append(correctpic.exercisename)
            videoList.append(str(patientpic.picturefilename))
            scoreList.append(patientpic.score)

        data = {
            "_id": 1,
            "patientName": patient.name,
            "trainTitle": type.split('-')[0],
            "trainList": name,
            "videoList": videoList,
            "scoreList": scoreList
        }

        return Response({'data': data})
