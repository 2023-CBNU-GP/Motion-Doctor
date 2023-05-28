from rest_framework.exceptions import AuthenticationFailed
from rest_framework.views import APIView
import jwt
from rest_framework.response import Response

from .models import *
import json


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


# 특정 의사가 특정 환자의 재활 테스트 영상 보기 위한 정보
class PatientTest(APIView):
    def post(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed("Unauthenticated!")

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Unauthenticated!")

        # 이부분을 어떻게 구현할지 희진이와 대화 필요.
