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


# 물체 인식을 위해 10s에 한 번씩 프론트에서 이미지를 보내면
# 물체가 있는지 없는지를 판단해서 리턴하는 consumer
class ImageConsumers(WebsocketConsumer):
    # websocket에 연결되면 호출되는 메소드
    def connect(self):
        print("웹소켓에 연결되었습니다.")

        # websocket 연결
        self.accept() 

        # 소켓에 연결되었음을 프론트에 알림
        self.send(text_data=json.dumps({
            'message': "socket connected"
        }))

    # websocket 연결이 해제되면 호출되는 메소드
    def disconnect(self, close_code):
        print("해제되었습니다.")

        # 결과값을 프론트에 알림
        self.send(text_data=json.dumps({
            'message': "socket disconnected"
        }))

    # websocket으로 메시지 받으면 호출되는 메소드
    def receive(self, text_data=None, bytes_data=None):
        print("메시지를 받았습니다.")

        # 이미지 받기
        byte_img = BytesIO(bytes_data)
        img_file = Image.open(byte_img)
        print(img_file)

        # 영상으로부터 사물 인식 결과를 프론트에 전송
        # 여기에 img_file 모델로 넘겨서 true or false 리턴하게 해주면 됨!
        result = True

        self.send(text_data=json.dumps({
            'type': 'received value',
            'message': result
        }))
