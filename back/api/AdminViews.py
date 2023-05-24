from django.db.models import Count
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import *
from . import serializers
import json


class ApproveRejectDoctor(APIView):
    def post(self, request):
        body = json.loads(request.body.decode('utf-8'))
        doctor = Doctor.objects.filter(id=body["id"]).first()

        doctor_type = body["type"]

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
    def get(self, request):
        data_list = []

        video_list = Correctpic.objects.all().values('doctorid', 'exercisetype').annotate(Count('uid'))
        for video in video_list:
            doctor = Doctor.objects.filter(uid=video['doctorid']).first()
            data = {
                "doctor_name": doctor.name,
                "doctor_hospitalName": doctor.hospitalname,
                "exercise_type": video['exercisetype'],
                "video_num": video['uid__count']
            }
            data_list.append(data)

        return Response({'data': data_list})
