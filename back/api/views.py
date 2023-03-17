from django.core.files.storage import default_storage

# Create your views here.
# from django.http import HttpResponse
# import sys
# import re
# from moviepy.editor import *
# import pytube
# import os.path
# import glob
# from pathlib import Path
# from pydub import AudioSegment
# import asyncio

# sys.path.append('/Users/songsuyeong/PF-programs/model/')
# from GetText import getText

import time


def link(request):
    #if request.method == 'POST':
        #video_link = re.search("\'(.+?)\'", str(request.body)).group(1)
        #print(video_link)

        #yt = pytube.YouTube(video_link)

        # 특정영상 다운로드
        #yt.streams.filter(only_audio=True).first().download()
        #print('success')

        #str_result = ''
        # 굳이 안쓰는 애. 삭제할 예정.

        #path = '/Users/songsuyeong/PF-programs/back/'

        #files = glob.glob("*.mp4")
        #for x in files:
        #    if not os.path.isdir(x):
        #        filename = os.path.splitext(x)
        #        try:
        #            os.rename(x, filename[0] + '.mp3')
        #        except:
        #            pass

        #file = Path('../../PF-programs/back/' + filename[0] + '.mp3')
        #while (1):
        #    if file.exists():
        #        break
        #print("파일 생성")

        #str_result = getText(filename[0]+".mp3")
        #print(str_result)

    #return HttpResponse(str_result)
    return HttpResponse("link complete")


def video(request):
    #video_file = request.FILES['file']
    #default_storage.save(video_file.name, video_file)

    #str_result = ''
    #path = '/Users/songsuyeong/PF-programs/back/'
    #dst = "audio.wav"

    #files = glob.glob("*.mp4")
    #for x in files:
    #    if not os.path.isdir(x):
    #        filename = os.path.splitext(x)
    #        try:
    #            clip = VideoFileClip(filename[0] + '.mp4')
    #            clip.audio.write_audiofile(filename[0] + ".mp3")
    #        except:
    #            pass

    #file = Path('../../PF-programs/back/' + filename[0] + '.mp3')

    #while (1):
    #    if file.exists():
    #        break
    #print("파일 생성")

    #str_result = getText(filename[0] + '.mp3')
    #print(str_result)

    #return HttpResponse(str_result)
    return HttpResponse("video complete")

