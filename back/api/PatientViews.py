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
        for patientpic in patientpic_list:
            if type_dict.get(patientpic.correctpicid.exercisetype) is None:
                type_dict[patientpic.correctpicid.exercisetype] = 1
            else:
                type_dict[patientpic.correctpicid.exercisetype] += 1

        i=1
        data_list = []
        for type in list(type_dict.keys()):
            comment_list, score_list = [], []
            uid, score = 0, 0
            flag = False

            correctpic = Correctpic.objects.filter(exercisetype=type)
            for pic in correctpic:
                patientpic = Patientpic.objects.filter(correctpicid=pic.uid, patientid=patient).last()
                # 아직 코스를 다 수행하지 않은 경우
                if patientpic is None:
                    flag=True
                    break
                
                score_list.append(patientpic.score)

                comment = Doctorcomment.objects.filter(pictureid=patientpic).first()
                comment_list.append(comment)

                uid = pic.doctorid.uid

            if flag:
                text = "아직 코스를 수행하지 않음"
            else:
                text = '내원 불필요'
                for c in comment_list:
                    if c is None:
                        text = '아직 평가되지 않음'
                    elif c.text == '내원 필요':
                        text = '내원 필요'

                score = sum(score_list) / type_dict[type]

            doctor = Doctor.objects.filter(uid=uid).first()
            data = {
                "_id": i,
                "trainTitle": type.split('-')[0],
                "trainNum": type_dict[type],
                "doctorName": doctor.name,
                "hospitalName": doctor.hospitalname,
                "score": score,
                "counselResult": text
            }
            data_list.append(data)
            i += 1

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
