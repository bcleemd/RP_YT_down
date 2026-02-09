## with cookies.txt


import argparse
from yt_dlp import YoutubeDL
from pathlib import Path

# Basic_utils.py의 ic 함수가 없으므로 주석 처리하거나 해당 파일을 제공해야 합니다.
# from Basic_utils import ic 

def audiodown(urls, call_back=None):
    mp3_dir = "MP3s"
    cur_dir = Path.cwd()
    download_folder = cur_dir / mp3_dir
    print(f"다운로드 폴더: {download_folder}") # 다운로드 폴더 출력
    download_folder.mkdir(parents=True, exist_ok=True)

    ydl_opts = {
        'extract_flat': 'discard_in_playlist',
        'final_ext': 'mp3',
        'format': 'bestaudio/best',
        'fragment_retries': 10,
        'ignoreerrors': 'only_download',
        'outtmpl': {'default': '%(title)s.%(ext)s'},
        'postprocessors': [{'key': 'FFmpegExtractAudio',
                            'nopostoverwrites': False,
                            'preferredcodec': 'mp3',
                            'preferredquality': '320'},
                           {'key': 'FFmpegConcat',
                            'only_multi_video': True,
                            'when': 'playlist'}],
        'paths': {'home': f'./{mp3_dir}'},
        'retries': 10,
        # 'ffmpeg_location': '.', # FFmpeg 경로가 필요하면 주석 해제
        
        # *** 오류 해결을 위한 핵심 옵션: 브라우저에서 쿠키 가져오기 ***
        # 사용하시는 브라우저에 맞게 'chrome', 'firefox', 'edge', 'safari' 등으로 변경해주세요.
        # 이 값은 반드시 단일 문자열이어야 합니다.
        # 'cookiesfrombrowser': 'chrome',  # 'chrome', 'firefox', 'edge', 'safari' 등 브라우저 이름
        # 'cookiesfrombrowser': 'chrome:Defalut',  # 'chrome', 'firefox', 'edge', 'safari' 등 브라우저 이름
        # 'cookiefile': 'cookies.txt',  # 인증 정보 추가
        # 만약 특정 프로필을 사용한다면, 'cookiesfrombrowser': 'chrome:Default' 와 같이 지정할 수도 있습니다.
        # (콜론으로 구분된 문자열)
    }
    if call_back is not None:     
        ydl_opts['progress_hooks'] = [call_back]
    
    try:
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download(urls)
        print("다운로드가 완료되었습니다.")
    except Exception as e:
        print(f"다운로드 중 오류가 발생했습니다: {e}")
        print("YouTube에서 봇 방지 또는 연령 제한으로 인해 로그인이 필요할 수 있습니다.")
        print("브라우저에서 YouTube에 로그인되어 있는지 확인하고, 'cookiesfrombrowser' 옵션의 브라우저 이름을 올바르게 설정했는지 확인해주세요.")


def call_back(data):
    # 다운로드 진행 상황을 출력하는 콜백 함수
    if data['status'] == 'downloading':
        total_bytes = data.get('total_bytes') or data.get('total_bytes_estimate')
        downloaded_bytes = data.get('downloaded_bytes', 0)
        if total_bytes:
            progress = (downloaded_bytes / total_bytes) * 100
            print(f"   [***] 다운로드 중: {progress:.2f}%")
        else:
            print("   [***] 다운로드 중...")
    elif data['status'] == 'finished':
        print("   [***] 다운로드 완료.")
    elif data['status'] == 'error':
        print(f"   [***] 오류 발생: {data.get('error', '알 수 없는 오류')}")


def main():
    parser = argparse.ArgumentParser(description='YouTube 음악 다운로드')
    parser.add_argument('urls', nargs='+', help='다운로드할 YouTube 음악 URL 목록')
    args = parser.parse_args()
    urls = args.urls

    # ic(args) # Basic_utils.py의 ic 함수가 없으므로 주석 처리
    # ic(urls) # Basic_utils.py의 ic 함수가 없으므로 주석 처리

    audiodown(urls, call_back)


def test_audiodown():
    # 중요: 이 URL은 테스트를 위한 예시이며, 실제 YouTube URL이 아닙니다.
    # 실제 YouTube 동영상 URL을 사용해야 합니다.
    # 예시: 'https://www.youtube.com/watch?v=dQw4w9WgXcQ' (Rick Astley - Never Gonna Give You Up)
    # urls = ["https://www.youtube.com/watch?v=5ZOh6nG2xQ0"] 
    urls = ["https://open.spotify.com/playlist/3KSVckDuhEe5VlP4SYYTzy?si=b7JsimvPQeGp_yLI6P0Xgg"]  # Spotify URL 예시
    print(f"테스트 URL: {urls[0]}")
    audiodown(urls, call_back)


if __name__ == '__main__':
    # main() # 명령줄 인수를 사용하려면 주석 해제
    test_audiodown() # 테스트 함수 실행
