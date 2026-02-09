import os
import subprocess
import sys
from prompt_toolkit import prompt
from prompt_toolkit.validation import Validator, ValidationError

# URL 유효성 검사를 위한 사용자 정의 Validator
class URLValidator(Validator):
    def validate(self, document):
        text = document.text
        # 간단한 URL 유효성 검사 (실제 사용 시 더 강력한 정규식 필요)
        if not (text.startswith("http://") or text.startswith("https://")):
            raise ValidationError(
                message="URL은 'http://' 또는 'https://'로 시작해야 합니다.",
                cursor_position=len(text)
            )
        if "spotify.com" not in text:
            raise ValidationError(
                message="Spotify URL이어야 합니다. (예: https://open.spotify.com/playlist/...)",
                cursor_position=len(text)
            )

def run_spotify_dl(playlist_url):
    """
    Spotify API 자격 증명을 환경 변수로 설정하고,
    주어진 플레이리스트 URL로 spotify_dl 명령을 실행합니다.
    """
    os.environ['SPOTIPY_CLIENT_ID'] = '31c8664105bc488cb9c9357182369335'
    os.environ['SPOTIPY_CLIENT_SECRET'] = 'e5b427f1818c43758c95f45a73273327'

    command = ["spotify_dl", "-l", playlist_url]

    try:
        print(f"\n[INFO] Spotify DL 실행 중: {playlist_url}")
        subprocess.run(command, check=True, text=True, capture_output=False, shell=False)
        print(f"\n[SUCCESS] '{playlist_url}'에 대한 spotify_dl 실행 완료.")
    except FileNotFoundError:
        print(f"\n[ERROR] 'spotify_dl' 명령을 찾을 수 없습니다.", file=sys.stderr)
        print(f"       'spotify_dl'이 설치되어 있고 시스템 PATH에 있는지 확인하세요.", file=sys.stderr)
        print(f"       'pip install spotify-dl'로 설치할 수 있습니다.", file=sys.stderr)
    except subprocess.CalledProcessError as e:
        print(f"\n[ERROR] spotify_dl 실행 중 오류 발생:", file=sys.stderr)
        print(f"       명령: {' '.join(e.cmd)}", file=sys.stderr)
        print(f"       종료 코드: {e.returncode}", file=sys.stderr)
        if e.stdout:
            print(f"       STDOUT:\n{e.stdout}", file=sys.stderr)
        if e.stderr:
            print(f"       STDERR:\n{e.stderr}", file=sys.stderr)
    except Exception as e:
        print(f"\n[ERROR] 예상치 못한 오류가 발생했습니다: {e}", file=sys.stderr)

if __name__ == "__main__":
    playlist_url = None

    # 명령줄 인수 확인
    if len(sys.argv) > 1:
        playlist_url = sys.argv[1]
    else:
        # 인수가 없으면 prompt-toolkit으로 입력 받기
        print("Spotify 플레이리스트/앨범/트랙 URL을 입력하세요.")
        print("(예: https://open.spotify.com/playlist/37i9dQZEVXbMDoHDwVN2tF)")
        try:
            playlist_url = prompt("URL 입력: ", validator=URLValidator(), validate_while_typing=True)
        except EOFError:
            print("\n입력이 취소되었습니다. 스크립트를 종료합니다.", file=sys.stderr)
            sys.exit(1)
        except KeyboardInterrupt:
            print("\n입력이 중단되었습니다. 스크립트를 종료합니다.", file=sys.stderr)
            sys.exit(1)

    if playlist_url:
        run_spotify_dl(playlist_url)
    else:
        print("[ERROR] URL을 제공하지 않았거나 입력하지 않았습니다. 스크립트를 종료합니다.", file=sys.stderr)
        sys.exit(1)