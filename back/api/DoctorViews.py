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

        patientpic = Patientpic.objects.filter(picturefilename=body['video']).first()
        comment = Doctorcomment.objects.filter(pictureid=patientpic).first()

        if comment is None:
            doctor_comment = Doctorcomment()
            doctor_comment.text = body["text"]
            doctor_comment.doctorid = doctor

            # 환자 영상 링크 전체를 보내줄 때
            doctor_comment.pictureid = patientpic
            doctor_comment.save()
        else:
            comment.text = body['text']
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
            patientpic_list = Patientpic.objects.filter(patientid=patient)

            type_dict = {}
            for patientpic in patientpic_list:
                if type_dict.get(patientpic.correctpicid.exercisetype) is None:
                    type_dict[patientpic.correctpicid.exercisetype] = 1
                else:
                    type_dict[patientpic.correctpicid.exercisetype] += 1

            for type in list(type_dict.keys()):
                isCounseled, flag = True, False
                comment_list = []

                correctpic = Correctpic.objects.filter(exercisetype=type)
                for pic in correctpic:
                    patientpic = Patientpic.objects.filter(correctpicid=pic, patientid=patient).last()

                    # 아직 코스를 다 수행하지 않은 경우
                    if patientpic is None:
                        flag = True
                        break

                    comment = Doctorcomment.objects.filter(pictureid=patientpic).first()
                    comment_list.append(comment)

                if flag:
                    continue
                else:
                    for c in comment_list:
                        if c is None:
                            isCounseled = False

                    data = {
                        "_id": i,
                        "uid": patient.uid,
                        "patientName": patient.name,
                        "trainCourse": type.split('-')[0],
                        "idx": type.split('-')[1],
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

        videoList, scoreList, nameList, commentList = [], [], [], []
        for correctpic in correctpic_list:
            patientpic = Patientpic.objects.filter(correctpicid=correctpic, patientid=patient).last()

            videoList.append(str(patientpic.picturefilename))
            scoreList.append(patientpic.score)
            nameList.append(correctpic.exercisename)

            comment = Doctorcomment.objects.filter(pictureid=patientpic.uid).first()
            if comment is None:
                commentList.append(None)
            else:
                commentList.append(comment.text)

        data = {
            "patientName": patient.name,
            "trainTitle": body["type"].split('-')[0],
            "trainName": nameList,
            "videoList": videoList,
            "scoreList": scoreList,
            "commentList": commentList
        }

        return Response({'data': data})


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
        video_list = Correctpic.objects.filter(doctorid=doctor)

        type_dict = {}
        for video in video_list:
            if type_dict.get(video.exercisetype) is None:
                type_dict[video.exercisetype] = 1
            else:
                type_dict[video.exercisetype] += 1

        i = 1
        data_list = []
        for type in list(type_dict.keys()):
            exercise = []

            correctpic = Correctpic.objects.filter(doctorid=doctor, exercisetype=type)
            for pic in correctpic:
                exercise_info = {
                    "name": pic.exercisename,
                    "video_name": str(pic.picturefilename)
                }
                exercise.append(exercise_info)

            data = {
                "_id": i,
                "type": type.split('-')[0],
                "num": type_dict[type],
                "idx": type.split('-')[1],
                "video_info": exercise
            }
            data_list.append(data)
            i += 1

        return Response({'data': data_list})


# 의사가 환자 승인하는 API
class ApprovePatient(APIView):
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
        patient = Patient.objects.filter(id=body["id"]).first()
        isApprove = body["type"]

        # 의사와 환자 매칭
        if isApprove == "approval":
            manage_form = Manage()
            manage_form.doctorid = doctor
            manage_form.patientid = patient
            manage_form.save()

        # 환자와 의사 연결 해제
        elif isApprove == "rejection":
            manage_form = Manage.objects.filter(doctorid=doctor, patientid=patient).first()
            if manage_form is None:
                raise ValueError("승인되어있지 않은 환자 id 입니다.")
            manage_form.delete()

        else:
            raise ValueError('승인여부 type이 잘못 입력되었습니다.')

        response = Response()
        response.data = {
            'message': 'success'
        }

        return response


# 의사가 전체 환자 목록을 확인하는 api (환자 승인하는 페이지)
class TotalPatientList(APIView):
    def get(self, request):
        data_list = []

        user_list = Patient.objects.all()
        for user in user_list:
            data = {
                "_id": user.uid,
                "name": user.name,
                "id": user.id,
                "email": user.email,
            }
            data_list.append(data)

        return Response({"data": data_list})
