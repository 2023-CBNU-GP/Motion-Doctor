from django.db.models import Count
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import *
from . import serializers
import json


# 관리자가 의사를 승인할 것인지 안 할 것인지 선택하는 api
class ApproveRejectDoctor(APIView):
    def post(self, request):
        body = json.loads(request.body.decode('utf-8'))
        doctor = Doctor.objects.filter(id=body["id"]).first()

        doctor_type = body["type"]

        # ready도 가능하게 바꾸기. . .
        if doctor_type == "approval":
            doctor.state = "approval"
        elif doctor_type == "rejection":
            doctor.state = "rejection"
        else:
            raise serializers.ValidationError('승인여부 type이 잘못 입력되었습니다.')

        doctor.save()

        response = Response()
        response.data = {
            'message': 'success'
        }

        return response


# 의사 정보 리턴해주는 api
class ListDoctor(APIView):
    def get(self, request):
        data_list = []

        user_list = Doctor.objects.all()
        user_list = user_list[1:]
        for user in user_list:
            if user.state == "approval":
                state = True
            else:
                state = False

            data = {
                "_id": user.uid,
                "name": user.name,
                "id": user.id,
                "email": user.email,
                "doctornum": user.doctornum,
                "hospitalname": user.hospitalname,
                "state": state
            }
            data_list.append(data)

        return Response({"data": data_list})


class ListDoctorVideo(APIView):
    # 전체 의사에 대해 올린 동영상 정보 리턴해주는 api
    def get(self, request):
        data_list = []

        video_list = Correctpic.objects.all().values('doctorid', 'exercisetype').annotate(Count('uid'))
        for video in video_list:
            doctor = Doctor.objects.filter(uid=video['doctorid']).first()
            data = {
                "doctor_name": doctor.name,
                "doctor_hospitalName": doctor.hospitalname,
                "video_num": video['uid__count'],
                "type": video['exercisetype'].split('-')[0],
                "typeIdx": video['exercisetype'].split('-')[1]
            }
            data_list.append(data)

        return Response({'data': data_list})

    # 특정 의사가 올린 동영상 리턴 api
    def post(self, request):
        body = json.loads(request.body.decode('utf-8'))
        exercise_type = body["type"]

        video_list = Correctpic.objects.filter(exercisetype=exercise_type).values()
        doctor = Doctor.objects.filter(uid=video_list[0]['doctorid_id']).first()

        data = {
            "doctor_name": doctor.name,
            "doctor_hospitalName": doctor.hospitalname,
            "courseName": video_list[0]['exercisetype'].split('-')[0],
            "trainList": [video_list[0]['exercisename'], video_list[1]['exercisename']],
            "filePathList": [video_list[0]['picturefilename'], video_list[1]['picturefilename']]
        }

        return Response({'data': data})


# 특정 의사가 관리하는 환자의 수를 리턴하는 API
class DoctorPatientNum(APIView):
    def post(self, request):
        body = json.loads(request.body.decode('utf-8'))
        doctor = Doctor.objects.filter(id=body["id"]).first()

        manage_list = Manage.objects.filter(doctorid=doctor)

        data = {
            "_id": 1,
            "name": doctor.name,
            "patientNum": len(manage_list),
        }

        return Response({"data": data})
