import jwt, datetime

from rest_framework.exceptions import AuthenticationFailed

import json
from .encrypt_utils import AESCipher
from back.my_settings import ReturnKey
from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import *
# import OpencvManager as om


class RegisterView(APIView):
    def post(self, request):
        returnKey = ReturnKey()
        key = returnKey.aesKey()
        aes = AESCipher(key)

        body = json.loads(request.body.decode('utf-8'))

        if body["type"] == "patient":
            user = Patient()
            user.name = body["name"]
            user.id = body["id"]
            user.password = aes.encrypt(body["password"])
            user.email = body["email"]

        elif body["type"] == "doctor":
            user = Doctor()
            user.name = body["name"]
            user.id = body["id"]
            user.password = aes.encrypt(body["password"])
            user.email = body["email"]
            user.doctornum = body["doctornum"]
            user.hospitalname = body["hospitalname"]

        else:
            raise serializers.ValidationError("잘못된 type을 입력하였습니다.")

        user.save()

        response = Response()
        response.data = {
            'message': 'success'
        }

        return response


class OverlabId(APIView):
    def post(self, request):
        body = json.loads(request.body.decode('utf-8'))
        input_id = body["id"]
        user_type = body["type"]

        if user_type == "patient":
            user = Patient.objects.filter(id=input_id).first()
        elif body["type"] == "doctor":
            user = Doctor.objects.filter(id=input_id).first()
        else:
            raise serializers.ValidationError("잘못된 type을 입력하였습니다.")

        # 사용자가 이미 존재하는 경우
        if user is not None:
            raise AuthenticationFailed("ID already exists!")

        response = Response()
        response.data = {
            'message': 'success'
        }
        return response


class LoginView(APIView):
    def post(self, request):
        returnKey = ReturnKey()
        key = returnKey.aesKey()
        aes = AESCipher(key)

        body = json.loads(request.body.decode('utf-8'))
        input_id = body["id"]
        password = body["password"]
        user_type = body["type"]

        if user_type == "patient":
            user = Patient.objects.filter(id=input_id).first()
        elif user_type == "doctor":
            user = Doctor.objects.filter(id=input_id).first()

            # 관리자 (Doctor 테이블의 가장 첫 데이터로 가정)
            if user.uid == Doctor.objects.first().uid:
                user_type = 'admin'
            else:
                if user.state != "approval":
                    raise AuthenticationFailed("User not allowed!")
        else:
            raise serializers.ValidationError("잘못된 type을 입력하였습니다.")

        # 사용자가 없는 경우
        if user is None:
            raise AuthenticationFailed("User not found!")

        # 패스워드가 잘못된 경우
        if password != aes.decrypt(user.password):
            raise AuthenticationFailed("Incorrect password!")

        # 입력한 비번이랑 같으면 로그인 성공(토큰과 같이 보냄)
        payload = {
            'type': user_type,
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256')
        response = Response()
        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            'jwt': token
        }

        return response


class UserView(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed("Unauthenticated!")

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Unauthenticated!")

        if payload['type'] == 'patient':
            user = Patient.objects.filter(id=payload['id']).first()

            data = {
                "uid": user.uid,
                "name": user.name,
                "id": user.id,
                "email": user.email,
                "type": payload['type']
            }

        elif (payload['type'] == 'doctor') or (payload['type'] == 'admin'):
            user = Doctor.objects.filter(id=payload['id']).first()

            data = {
                "_id": user.uid,
                "name": user.name,
                "id": user.id,
                "email": user.email,
                "doctornum": user.doctornum,
                "hospitalname": user.hospitalname,
                "type": payload['type']
            }

        else:
            raise serializers.ValidationError("잘못된 type을 입력하였습니다.")

        return Response(data)


class LogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'success'
        }

        return response


class UserDrop(APIView):
    def post(self, request):
        returnKey = ReturnKey()
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed("Unauthenticated!")

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Unauthenticated!")

        key = returnKey.aesKey()
        aes = AESCipher(key)

        body = json.loads(request.body.decode('utf-8'))
        password = body["password"]

        if payload["type"] == "patient":
            user = Patient.objects.filter(id=payload['id']).first()
        elif payload["type"] == "doctor":
            user = Doctor.objects.filter(id=payload['id']).first()
        else:
            raise serializers.ValidationError("잘못된 type을 입력하였습니다.")

        # 사용자가 없는 경우
        if user is None:
            raise AuthenticationFailed("User not found!")

        # 패스워드가 잘못된 경우
        if password != aes.decrypt(user.password):
            raise AuthenticationFailed("Incorrect password!")

        user.delete()

        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'success'
        }

        return response


class PasswordModify(APIView):
    def post(self, request):
        returnKey = ReturnKey()
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed("Unauthenticated!")

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Unauthenticated!")

        key = returnKey.aesKey()
        aes = AESCipher(key)

        body = json.loads(request.body.decode('utf-8'))
        current_password = body["current_password"]
        new_password = body["new_password"]

        if payload["type"] == "patient":
            user = Patient.objects.filter(id=payload['id']).first()
        elif payload["type"] == "doctor":
            user = Doctor.objects.filter(id=payload['id']).first()
        else:
            raise serializers.ValidationError("잘못된 type을 입력하였습니다.")

        # 사용자가 없는 경우
        if user is None:
            raise AuthenticationFailed("User not found!")

        # 패스워드가 잘못된 경우
        if current_password != aes.decrypt(user.password):
            raise AuthenticationFailed("Incorrect password!")

        user.password = aes.encrypt(new_password)
        user.save()

        response = Response()
        response.data = {
            'message': 'success'
        }

        return response






