import base64
import json
import os

from channels.generic.websocket import AsyncWebsocketConsumer
from django.conf import settings
from api.models import *

import tempfile
from django.core.files import File
from moviepy.editor import VideoFileClip
import cv2

from pydub import AudioSegment
from pydub.utils import make_chunks
import subprocess


# 환자 모션 웹캠 저장 및 점수 반환 consumer
class VideoConsumers(AsyncWebsocketConsumer):
    async def save_video(self, patient_id, exercise_name, exercise_type, video_data):
        # Base64 디코딩하여 바이너리 데이터로 변환
        binary_data = base64.b64decode(video_data)

        # 임시파일 저장 (webm으로 저장 -> mp4로 수동 변환하면 안 깨짐)
        temp_path = tempfile.gettempdir()
        file_name = '/video.webm'
        with open(temp_path + file_name, 'wb') as wfile:
            wfile.write(binary_data)

        video_webm = temp_path + "/video.webm"
        video2_mp4 = temp_path + "/video.mp4"
        subprocess.run(f"ffmpeg -i {video_webm} {video2_mp4}", shell=True)

        score = 0
        correctPic = Correctpic.objects.filter(exercisename=exercise_name, exercisetype=exercise_type).first()
        patient = Patient.objects.filter(id=patient_id).first()

        # 새로운 Patientpic 객체 생성 및 저장 (여기서 webm 파일을 mp4로 변환해야함)
        with open(temp_path + "/video.mp4", "rb") as file:
            form = Patientpic()

            file_obj = File(file)
            form.picturefilename = file_obj
            form.score = score
            form.correctpicid = correctPic
            form.patientid = patient

            form.save()

        # 환자가 영상을 찍으면 해당 의사와 매칭
        if Manage.objects.filter(doctorid=correctPic.doctorid, patientid=patient).first() is None:
            manage_form = Manage()
            manage_form.doctorid = correctPic.doctorid
            manage_form.patientid = patient
            manage_form.save()

    async def connect(self):
        # 웹소켓 연결이 이루어질 때 실행되는 메서드
        # 연결을 받고 처리할 준비를 할 수 있습니다.
        print("웹소켓에 연결되었습니다.")

        # websocket 연결
        await self.accept()

        # 소켓에 연결되었음을 프론트에 알림
        await self.send(text_data=json.dumps({
            'message': "socket connected"
        }))

    async def disconnect(self, close_code):
        # 웹소켓 연결이 종료될 때 실행되는 메서드
        print("해제됩니다.")
        if close_code == 1000:
            await self.close()

    async def receive(self, text_data=None, bytes_data=None):
        # 웹소켓으로부터 메시지를 수신받을 때 실행되는 메서드
        # 수신한 데이터를 처리하고 응답을 보낼 수 있습니다.
        data = json.loads(text_data)
        patient_id = data['patient_id']
        exercise_name = data['exercise_name']
        exercise_type = data['exercise_type']
        video_data = data['video_data']

        video_data = video_data[23:]

        # 비디오 저장
        await self.save_video(patient_id, exercise_name, exercise_type, video_data)

        # 응답을 보낼 때는 send() 메서드를 사용합니다.
        await self.send(text_data='Video saved successfully.')
