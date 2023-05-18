from channels.generic.websocket import WebsocketConsumer
import json


class Consumers(WebsocketConsumer):
    # websocket에 연결되면 호출되는 메소드
    def connect(self):
        print("웹소켓에 연결되었습니다.")

        self.accept()  # websocket 연결

        self.send(text_data=json.dumps({
            'type': 'connection_established',
            'message': 'You are now connected!'
        }))

    def disconnect(self, close_code):
        print("해제되었습니다.")

    def receive(self, text_data=None, bytes_data=None):
        # 영상 받기
        print("메시지를 받았습니다.")

        # 영상으로부터 사물 인식 및 각도 측정 결과를 프론트에 전송
        self.send(text_data=json.dumps({
            'type': 'current_state',
            'message': 'message'
        }))
