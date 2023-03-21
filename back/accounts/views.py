import smtplib
from email.mime.text import MIMEText
from random import seed, randrange

import jwt, datetime
from time import time
from rest_framework.exceptions import AuthenticationFailed

from .models import *
import json
from .encrypt_utils import AESCipher
from back.my_settings import ReturnKey
from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import UserSerializer


class RegisterView(APIView):
    def post(self, request):
        returnKey = ReturnKey()
        key = returnKey.aesKey()
        aes = AESCipher(key)

        user = Patient()
        body = json.loads(request.body.decode('utf-8'))
        user.name = body["name"]
        user.id = body["id"]
        user.password = aes.encrypt(body["password"])
        user.email = body["email"]
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

        user = Patient.objects.filter(id=input_id).first()

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

        user = Patient.objects.filter(id=input_id).first()

        # 사용자가 없는 경우
        if user is None:
            raise AuthenticationFailed("User not found!")

        # 패스워드가 잘못된 경우
        if password != aes.decrypt(user.password):
            raise AuthenticationFailed("Incorrect password!")

        # 입력한 비번이랑 같으면 로그인 성공(토큰과 같이 보냄)
        payload = {
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

        user = Patient.objects.filter(id=payload['id']).first()
        serializer = UserSerializer(user)

        return Response(serializer.data)


class LogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'success'
        }

        return response


code_dic = {}


class EmailView(APIView):
    def post(self, request):
        returnKey = ReturnKey()
        # 호스트 이메일 환경설정
        sendEmail = returnKey.EMAIL_HOST_USER
        body = json.loads(request.body.decode('utf-8'))
        recvEmail = body['email']
        password = returnKey.EMAIL_HOST_PASSWORD
        smtpName = returnKey.EMAIL_HOST
        smtpPort = returnKey.EMAIL_PORT

        # 인증번호 난수 4자리 생성
        seed(time())
        value = randrange(1000, 10000, 1)

        code_dic[recvEmail] = value

        html = """\
        <html>
          <head>
            <style>
              h1{{
                background-color: #f9e796;
                text-align: center;
                color: black;
              }}
              body {{
                background-color: white;
              }}

              p {{
                font-family: verdana;
                font-size: 20px;
              }}
              pre {{
                text-align: center;
              }}

              table{{
                text-align: center;
                opacity: 0.8;
              }}

            </style>
          </head>
          <body align="center">

          <h1 align="center">
                  <br>PF PROGRAM<br/><br/>
          </h1>

          <br>
          <pre >
            안녕하세요, PF PROGRAM 관리자입니다.
            PR FROGAM의 가입을 위해서 고객님의 인증번호를 인증하셔야 합니다.
            가입을 원하신다면 계정 본인 확인을 위한 아래의 인증 번호를 입력칸에 넣어주시길 바랍니다.<br/>
          </pre><br/><br/>
            <table cellpadding="0" cellspacing="0" width="400" height="100">
              <td bgcolor="#e3e1db">
                  인증번호 : {code}
              </td>
            </table>
          </body>
        </html>

        """.format(code=value)

        msg = MIMEText(html, "html")

        msg['Subject'] = "[PF_Program] 이메일 인증"
        msg['From'] = sendEmail
        msg['To'] = recvEmail

        s = smtplib.SMTP(smtpName, smtpPort)  # 메일 서버 연결
        s.starttls()  # TLS 보안 처리
        s.login(sendEmail, password)  # 로그인
        s.sendmail(sendEmail, recvEmail, msg.as_string())  # 메일 전송, 문자열로 변환하여 보냅니다.
        s.close()  # smtp 서버 연결을 종료합니다.

        response = Response()
        response.data = {
            'message': 'success'
        }

        return response


class EmailCodeView(APIView):
    def post(self, request):
        body = json.loads(request.body.decode('utf-8'))
        email = body['email']
        code = body['code']

        store_code = code_dic.get(email)

        # 이메일이 없는 경우
        if store_code is None:
            raise AuthenticationFailed("Email not found!")

        # 잘못된 코드를 입력한 경우
        if code != store_code:
            raise AuthenticationFailed("Incorrect certification code")

        del code_dic[email]

        response = Response()
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

        user = Patient.objects.filter(id=payload['id']).first()

        key = returnKey.aesKey()
        aes = AESCipher(key)

        body = json.loads(request.body.decode('utf-8'))
        password = body["password"]

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

        user = Patient.objects.filter(id=payload['id']).first()

        key = returnKey.aesKey()
        aes = AESCipher(key)

        body = json.loads(request.body.decode('utf-8'))
        current_password = body["current_password"]
        new_password = body["new_password"]

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
