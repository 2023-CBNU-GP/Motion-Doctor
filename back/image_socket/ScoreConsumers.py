import json
from channels.generic.websocket import WebsocketConsumer


# 환자 모션 영상을 프론트에서 보내면 이것이 media 폴더에 저장됨.
# media 폴더에 있는 영상을 인공지능 모델에 연결시켜서 결과값을 리턴해야하는데
# 이때 프론트에서 새롭게 연결한 웹소켓으로 결과값을 전송하는 것
# 이 결과값을 전송하기 위한 Consumer
class ScoreConsumers(WebsocketConsumer):
    # websocket에 연결되면 호출되는 메소드
    def connect(self):
        print("웹소켓에 연결되었습니다.")

        # websocket 연결
        self.accept()

        # 여기에 파이썬 모델로 영상을 전송하여 결과 score를 저장
        score = 0

        # 결과값을 프론트에 알림
        self.send(text_data=json.dumps({
            'type': 'connection established',
            'message': score
        }))

    # websocket 연결이 해제되면 호출되는 메소드
    def disconnect(self, close_code):
        print("해제되었습니다.")
