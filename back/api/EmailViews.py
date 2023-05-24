from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed

from .models import *
import json
import smtplib
from email.mime.text import MIMEText
from random import seed, randrange

from . import serializers
from back.my_settings import ReturnKey
from time import time


code_dic = {}


class EmailView(APIView):
    def post(self, request):
        body = json.loads(request.body.decode('utf-8'))
        recvEmail = body['email']

        if body["type"] == "patient":
            if Patient.objects.filter(email=recvEmail):
                raise AuthenticationFailed("이미 가입된 이메일입니다.")
        elif body["type"] == "doctor":
            if Doctor.objects.filter(email=recvEmail):
                raise AuthenticationFailed("이미 가입된 이메일입니다.")
        else:
            raise serializers.ValidationError("잘못된 type을 입력하였습니다.")


        returnKey = ReturnKey()
        # 호스트 이메일 환경설정
        sendEmail = returnKey.EMAIL_HOST_USER
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
                  <br>Motion Doctor<br/><br/>
          </h1>

          <br>
          <pre >
            안녕하세요, Motion Doctor 관리자입니다.
            Motion Doctor의 가입을 위해서 고객님의 인증번호를 인증하셔야 합니다.
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

        msg['Subject'] = "[Motion Doctor] 이메일 인증"
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