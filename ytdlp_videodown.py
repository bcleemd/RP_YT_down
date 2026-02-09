import argparse
from yt_dlp import YoutubeDL
from Basic_utils import ic 
from  pathlib import Path

def videodown(urls,call_back=None) : 
    mp4_dir = "MP4s"
    cur_dir = Path.cwd()
    download_folder = cur_dir / mp4_dir
    print(download_folder)
    download_folder.mkdir(parents=True, exist_ok=True)

    ydl_opts = {
        'extract_flat': 'discard_in_playlist',
        'fragment_retries': 10,
        'ignoreerrors': 'only_download',
        # 'format': args.format,  # 사용자 지정 포맷
        'format': 'bestvideo[height<=1080][ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'postprocessors': [{'key': 'FFmpegConcat',
                            'only_multi_video': True,
                            'when': 'playlist'}],
        'paths': {'home': f'./{mp4_dir}'},
        'retries': 10
    }
    if call_back is not None :     
        ydl_opts['progress_hooks'] = [call_back]
    
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download(urls)


def call_back(data) :
    print("   [***]  ")


def main():
    parser = argparse.ArgumentParser(description='YouTube 동영상 다운로드')
    parser.add_argument('urls', nargs='+', help='다운로드할 YouTube 동영상 URL 목록')
    parser.add_argument('--format', default='bestvideo[height<=1080][ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
                        help='다운로드할 포맷 (기본값: %(default)s)')
    args = parser.parse_args()
    urls = args.urls

    ic(args)
    ic(args.urls)

    videodown(urls,call_back)
    # videodown(urls)



if __name__ == '__main__':
    main()

"""
코드 분석 및 개선점
제공된 코드는 yt_dlp를 이용하여 YouTube 동영상을 다운로드하는 기능을 가지고 있습니다. 이 코드를 argparse를 이용하여 다중 URL을 입력 받아 실행하도록 개선하는 목표입니다.

개선 방향:

argparse를 이용한 명령줄 인터페이스 구현: 사용자가 명령줄에서 다양한 옵션을 지정할 수 있도록 합니다.
URL 입력: 다수의 URL을 공백으로 구분하여 입력받을 수 있도록 합니다.
기존 옵션 유지: ydl_options에 설정된 기존 옵션들을 유지합니다.
오류 처리: 잘못된 URL이나 옵션이 입력될 경우 적절한 에러 메시지를 출력합니다.

"""

"""
코드 설명
argparse 설정:
ArgumentParser를 이용하여 명령줄 인터페이스를 생성합니다.
add_argument를 이용하여 urls 인수를 추가합니다. nargs='+'는 다수의 인수를 받도록 설정합니다.
--format 옵션을 추가하여 사용자가 다운로드 포맷을 지정할 수 있도록 합니다.
ydl_opts 설정:
args.format을 이용하여 사용자가 지정한 포맷을 ydl_opts에 적용합니다.
YoutubeDL 실행:
with 문을 사용하여 YoutubeDL 객체를 생성하고, download 메서드를 이용하여 다운로드를 진행합니다.
사용법
Bash
python your_script.py https://youtu.be/UxfDM0TtTYY https://youtu.be/yEaD_yqlaes --format best
코드를 사용할 때는 주의가 필요합니다.

위와 같이 명령줄에서 다운로드할 URL 목록과 (선택적으로) 다운로드 포맷을 지정하여 실행할 수 있습니다.

추가 기능
출력 파일 이름 지정: --output 옵션을 추가하여 출력 파일 이름을 지정할 수 있도록 합니다.
자막 다운로드: --writeautomaticsub 옵션을 추가하여 자동 자막을 다운로드할 수 있도록 합니다.
에러 로그: 다운로드 실패 시 에러 로그를 파일로 저장하도록 합니다.
주의:

yt_dlp의 옵션은 매우 다양하므로, 필요에 따라 추가적인 옵션을 설정할 수 있습니다.
YouTube의 이용 약관을 준수하여 동영상을 다운로드해야 합니다.
이 개선된 코드를 통해 사용자는 명령줄에서 간편하게 다수의 YouTube 동영상을 다운로드할 수 있습니다.

"""

'''

from yt_dlp import YoutubeDL

# urls = ['https://www.youtube.com/watch?v=BaW_jenozKc']
# urls = ['https://www.youtube.com/watch?v=lkz835kJuno ']  # total maxillectomy  , age restricted 
urls = ['https://youtu.be/UxfDM0TtTYY',
        'https://youtu.be/yEaD_yqlaes',
        'https://youtu.be/q4fFDbTZTrs',
        'https://youtu.be/j-ZURRhcvhA']

ydl_options = {'extract_flat': 'discard_in_playlist',
 'fragment_retries': 10,
 'ignoreerrors': 'only_download',

 'format': ' '
           "bestvideo[height<=1080][ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
#  'keepvideo': True,
 'postprocessors': [{'key': 'FFmpegConcat',
                     'only_multi_video': True,
                     'when': 'playlist'}],
 'retries': 10
 }




with YoutubeDL(ydl_options) as ydl:
    ydl.download(urls)


'''



    
