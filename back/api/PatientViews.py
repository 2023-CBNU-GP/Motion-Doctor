from rest_framework.exceptions import AuthenticationFailed
from rest_framework.views import APIView
from rest_framework.response import Response

import jwt
from .models import *
import json


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

        # 환자 영상 모두 가져오기
        patientpic_list = Patientpic.objects.filter(patientid=patient)

        type_dict = {}
        comment_list = []
        score_list = []
        doctor_list = []
        for patientpic in patientpic_list:
            correctpic = Correctpic.objects.filter(uid=patientpic.correctpicid.uid).first()
            doctor = Doctor.objects.filter(uid=correctpic.doctorid.uid).first()
            if type_dict.get(correctpic.exercisetype) is None:
                type_dict[correctpic.exercisetype] = 1
            else:
                type_dict[correctpic.exercisetype] += 1

            comment = Doctorcomment.objects.filter(pictureid=patientpic.uid).first()
            score = patientpic.score

            comment_list.append(comment)
            score_list.append(score)
            doctor_list.append(doctor)

        keys = list(type_dict.keys())
        values = list(type_dict.values())

        data_list = []
        i,j=0,0
        for num in values:
            text = '내원 불필요'
            system_score=0
            for _ in range(num):
                if comment_list[j] == '내원 필요':
                    text = '내원 필요'
                if comment_list[j] is None:
                    text = '아직 평가되지 않음'

                system_score+=score_list[j]

                j+=1

            data = {
                "_id": i+1,
                "trainTitle": keys[i].split('-')[0],
                "trainNum": num,
                "doctorName": doctor_list[i].name,
                "hospitalName": doctor_list[i].hospitalname,
                "score": system_score/num,
                "counselResult": text
            }
            data_list.append(data)

            i+=1

        return Response({'data': data_list})


# 환자가 자신이 등록한 비디오 삭제하는 API - 구현해야함
class RemoveVideo(APIView):
    def post(self, request):
        token = request.COOKIES.get('jwt')
        body = json.loads(request.body.decode('utf-8'))

        if not token:
            raise AuthenticationFailed("Unauthenticated!")

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Unauthenticated!")

        patient = Patient.objects.filter(id=payload["id"]).first()
        correctpic = Correctpic.objects.filter(exercisetype=body['type']).first()

        video = Patientpic.objects.filter(patientid=patient, correctpicid=correctpic).first()

        # 사용자가 없는 경우
        if video is None:
            raise FileNotFoundError("삭제하려고 하는 파일이 존재하지 않습니다.")

        video.delete()

        response = Response()
        response.data = {
            'message': 'success'
        }

        return response
