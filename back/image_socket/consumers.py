from io import BytesIO

from channels.generic.websocket import WebsocketConsumer
import json
import base64
from PIL import Image

import os

from django.conf import settings
from django.http import JsonResponse

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "back.settings")

import django
django.setup()


class Consumers(WebsocketConsumer):
    # websocket에 연결되면 호출되는 메소드
    def connect(self):
        print("웹소켓에 연결되었습니다.")

        # websocket 연결
        self.accept() 

        # 소켓에 연결되었음을 프론트에 알림
        self.send(text_data=json.dumps({
            'type': 'connection established',
            'message': 'You are now connected!'
        }))

    # websocket 연결이 해제되면 호출되는 메소드
    def disconnect(self, close_code):
        print("해제되었습니다.")

    # websocket으로 메시지 받으면 호출되는 메소드
    def receive(self, text_data=None, bytes_data=None):
        print("메시지를 받았습니다.")

        # 이미지 받기
        byte_img = BytesIO(bytes_data)
        img_file = Image.open(byte_img)
        print(img_file)

        # 영상으로부터 사물 인식 결과를 프론트에 전송



        self.send(text_data=json.dumps({
            'type': 'received value',
            'message': "received!"
        }))
