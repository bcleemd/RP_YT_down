from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import time
from datetime import datetime

from pytube import YouTube
import os
import ffmpeg

import telegram
from conf import *

# 텔레그램 메신저를 사용하기위한 토큰 설정부분
bot = telegram.Bot(token=TELEGRAM_TOKEN)


# YouTube Data API의 API key를 입력합니다.
api_key = YOUTUBE_APIKEY

# 가져올 채널의 ID를 입력합니다.
channel_id = 'UChBYnUkgXUk2rmkQlIMNXNw'


# YouTube Data API 클라이언트를 빌드합니다.
youtube = build('youtube', 'v3', developerKey=api_key)

############################################################################
# 화질 720
def on_progress(vid, chunk, bytes_remaining):
    total_size = vid.filesize
    bytes_downloaded = total_size - bytes_remaining
    percentage_of_completion = bytes_downloaded / total_size * 100
    totalsz = (total_size/1024)/1024
    totalsz = round(totalsz,1)
    remain = (bytes_remaining / 1024) / 1024
    remain = round(remain, 1)
    dwnd = (bytes_downloaded / 1024) / 1024
    dwnd = round(dwnd, 1)
    percentage_of_completion = round(percentage_of_completion,2)

    #print(f'Total Size: {totalsz} MB')
    print(f'Download Progress: {percentage_of_completion}%, Total Size:{totalsz} MB, Downloaded: {dwnd} MB, Remaining:{remain} MB')

# 화질 720
def download_youtube_720(title, url):
    url = 'https://youtu.be/' + url 
    print("제목 : ", title, "\t주소 : ", url, " 영상을 다운로드 받습니다.")
    bot.sendMessage(chat_id=TELEGRAM_CHAT_ID, text="제목 : "+title+"\t주소 : "+url+" 영상을 다운로드 받습니다.")

    # url = 'https://www.youtube.com/watch?v=4ASVa2HPr6M&t=9s'
    YouTube(url, use_oauth=True, allow_oauth_cache=True, on_progress_callback=on_progress).streams.filter(res="720p").first().download()

    if os.path.exists(title+'.mp4'):
        os.rename(title+'.mp4', title+"_720p_"+date__+'.mp4')



# 화질 1080
def download_youtube_1080(title, url):
    url = 'https://youtu.be/' + url 
    print("제목 : ", title, "\t주소 : ", url, " 영상을 다운로드 받습니다.")
    bot.sendMessage(chat_id=TELEGRAM_CHAT_ID, text="제목 : "+title+"\t주소 : "+url+" 영상을 다운로드 받습니다.")
    # youtube = YouTube('https://youtu.be/JF9YUMr6b3I') # 유튜브 영상 주소
    youtube = YouTube(url, use_oauth=True, allow_oauth_cache=True) # 유튜브 영상 주소

    video = youtube.streams.filter(res="1080p").first().download()
    os.rename(video,"video_1080.mp4")
    audio = youtube.streams.filter(only_audio=True)
    audio[0].download()
    print("video, audio download 완료")


    # 비디오와 오디오를 합쳐서 최종 영상 생성
    video_stream = ffmpeg.input('video_1080.mp4')
    title = title.replace(".","") #<-------- 영상제목에 "." 가 포함된 경우 삭제되므로 이를 제거해 주어야 에러가 발생하지 않음
    audio_stream = ffmpeg.input(title+'.mp4') # 유튜브 영상 제목
    ffmpeg.output(audio_stream, video_stream, 'out.mp4').run()

    if os.path.exists('video_1080.mp4'):
        os.remove('video_1080.mp4')
    if os.path.exists(title+'.mp4'):
        os.remove(title+'.mp4')
    if os.path.exists('out.mp4'):
        os.rename('out.mp4', title+"_1080p_"+date__+'.mp4')

########################################################################

beforeVideos = [] # 현재 비디오 목록 10개
beforeVideos_dic = {}

try:
    # 동영상 목록을 가져옵니다.
    request = youtube.search().list(
        part='id,snippet',
        channelId=channel_id,
        order='date',
        type='video',
        maxResults=10
    )
    response = request.execute()
    # print(response)

    # 동영상 제목과 ID를 출력합니다.
    for item in response['items']:
        video_title = item['snippet']['title']
        video_id = item['id']['videoId']
        print(f'{video_title}: {video_id}')
        beforeVideos.append(video_title)
        beforeVideos_dic[video_title] = video_id
    
    beforeSet = set(beforeVideos) # 현재 비디오 목록 10개, set으로 만들어야 뺄 수 있음
    # beforeSet_dic = set(beforeVideos_dic)
    # print(beforeSet)
    # print(beforeSet_dic)
    print("==========================================================================")

except HttpError as e:
    print(f'An HTTP error {e.resp.status} occurred:\n{e.content}')



time.sleep(2)

afterVideos = [] # 10초 후 비디오 목록 10개
afterVideos_dic = {}

while True:
# for i in range(0,2):
    now=datetime.now()
    date__ = str(now.year)+"-"+str(now.month)+"-"+str(now.day)+"-"+str(now.hour)+"-"+str(now.minute)
    try:
        # 동영상 목록을 가져옵니다.
        request = youtube.search().list(
            part='id,snippet',
            channelId=channel_id,
            order='date',
            type='video',
            maxResults=10
        )
        response = request.execute()
        # print(response)

        # 동영상 제목과 ID를 출력합니다.
        for item in response['items']:
            video_title = item['snippet']['title']
            video_id = item['id']['videoId']
            print(f'{video_title}: {video_id}')
            afterVideos.append(video_title)
            afterVideos_dic[video_title] = video_id
        
        afterSet = set(afterVideos) # 10초 후 비디오 목록 10개
        # afterSet_dic = set(afterVideos_dic)
        # print(afterSet)
        # print(afterSet_dic)
        print("==========================================================================")


        result = afterSet - beforeSet # afterSet이 많으면 변경발생(즉, 추가되면 변경발생), beforeSet이 많으면 변경 미발생임
        # result_dic = afterSet_dic - beforeSet_dic
        # print(result)


        if (result):
            print("동영상 목록(개수 등)에 변경이 발생했습니다.")
            print("추가된 동영상(제목) : ", result)
            bot.sendMessage(chat_id=TELEGRAM_CHAT_ID, text="동영상 목록(개수 등)에 변경이 발생했습니다.\n 추가된 동영상(제목) : "+str(result))
            # print("추가된 동영상의 url : ", result_dic)

            for item in result:
                # print(item) # 추가된 동영상 제목

                # 아래와 같이 다시 'afterVideos_dic.items():' <-- 이걸 쓰는 이유는 value 즉 url을 구하기 위함임, result(afterSet)만으로는 key 즉, 영상 제목만 구할 수 있으므로 별도 url을 구하는 방법이 필요했음
                for key, value in afterVideos_dic.items(): # afterVideos_dic 딕셔너리 내 key(title), value(url)로 돌면서 
                    if item == key: # 제목이 같으면(즉, 새로 추가된 영상이면 영상을 다운로드, 그렇지 않으면 다운로드하지 않음)
                        print("title : ",key, " url : ", value)
                        try:
                            pass
                            print("1080p 화질로 영상을 다운로드 받습니다.")
                            download_youtube_1080(key, value)
                        except:
                            pass
                            try:
                                pass
                                print("1080p 화질로 영상 다운로드 시 에러가 발생하여, 720p 화질로 영상을 다시 다운로드 받습니다.")
                                download_youtube_720(key, value)
                            except:
                                pass # 720p로 다운로드 시에도 에러 발생하면 프로그램 에러 발생으로 멈추지 않도록 pass로 통과 시킴
                        
            
        else:
            print("동영상 목록(개수 등)에 변경이 발생하지 않았습니다.")
            print("동영상 목록 : ", result)
            
        
        print("==========================================================================")
        print("###########################################################################\n\n")


        beforeSet = afterSet


    except HttpError as e:
        print(f'An HTTP error {e.resp.status} occurred:\n{e.content}')
    

    time.sleep(20) # API 요청/응답 갯수에 제한(10000/일)이 있으므로 실제로는 최소 1분~60분 정도로 늘려주어야 함

 
