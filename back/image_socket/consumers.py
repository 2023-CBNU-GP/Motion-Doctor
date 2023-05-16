from channels.generic.websocket import WebsocketConsumer
import json


class Consumers(WebsocketConsumer):
    # websocket에 연결되면 호출되는 메소드
    def connect(self):
        self.accept()  # websocket 연결

        self.send(text_data=json.dumps({
            'type': 'connection_established',
            'message': 'You are now connected!'
        }))

    def disconnect(self, close_code):
        pass

    def receive(self, text_data=None, bytes_data=None):
        # 영상 받기
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        self.send(text_data=json.dumps({
            'message': message
        }))

        # 영상으로부터 사물 인식 및 각도 측정 결과를 프론트에 전송
        # self.send(text_data=json.dumps({
        #     'type': 'current_state',
        #     'message': 'message'
        # }))
