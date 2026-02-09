import os
import argparse
import eyed3
from eyed3.id3 import Tag, ID3_V2_3

def update_mp3_tags_eyed3(folder_path, delimeter, recursive):
    """
    폴더 내 MP3 파일의 태그를 파일 이름에서 추출하여 업데이트합니다. (eyed3 모듈 사용)
    파일 이름에 구분자가 없으면 파일 이름 전체를 제목으로 간주하여 제목 태그만 업데이트합니다.

    Args:
        folder_path (str): MP3 파일이 있는 폴더 경로.
        delimeter (str): 파일 이름에서 제목과 아티스트를 구분하는 구분자.
        recursive (bool): 서브 폴더까지 재귀적으로 검색할지 여부.
    """

    for root, _, files in os.walk(folder_path):
        if not recursive and root != folder_path:
            continue  # 재귀 모드가 아니면 현재 폴더만 처리

        for filename in files:
            if filename.lower().endswith(".mp3"):
                filepath = os.path.join(root, filename)
                base_name = os.path.splitext(filename)[0] # 확장자를 제외한 파일 이름

                try:
                    audio = eyed3.load(filepath)
                    if audio is None:
                        print(f"Error: Could not load MP3 file '{filename}'. Skipping.")
                        continue

                    # 태그가 없으면 새로 생성
                    if audio.tag is None:
                        audio.initTag(version=ID3_V2_3) # ID3v2.3 버전으로 초기화 (일반적)
                        print(f"Initialized new ID3v2.3 tag for '{filename}'")

                    if delimeter in base_name:
                        # 구분자가 있으면 제목과 아티스트 모두 추출 및 업데이트
                        parts = base_name.split(delimeter, 1)
                        title = parts[0].strip()
                        artist = parts[1].strip()

                        audio.tag.title = title
                        audio.tag.artist = artist
                        print(f"Updated: '{filename}' -> Title: '{title}', Artist: '{artist}'")
                    else:
                        # 구분자가 없으면 파일 이름 전체를 제목으로 간주하고 아티스트는 비움
                        title = base_name.strip()
                        audio.tag.title = title
                        audio.tag.artist = "" # 아티스트 태그는 비웁니다.
                        print(f"Updated (Title only): '{filename}' -> Title: '{title}' (No delimeter found)")

                    audio.tag.save()

                except Exception as e:
                    print(f"Error processing '{filename}': {e}")

def main():
    parser = argparse.ArgumentParser(description="MP3 파일의 태그를 파일 이름에서 추출하여 업데이트합니다. (eyed3 모듈 사용)")
    parser.add_argument("folder", help="MP3 파일이 있는 폴더 경로")
    parser.add_argument("-S", action="store_true", dest="recursive",
                        help="서브 폴더까지 재귀적으로 탐색합니다.")
    parser.add_argument("-D", "--delimeter", default=" -by ",
                        help="파일 이름에서 제목과 아티스트를 구분하는 구분자 (기본값: ' -by ')")

    args = parser.parse_args()

    if not os.path.isdir(args.folder):
        print(f"오류: '{args.folder}' 는 유효한 폴더 경로가 아닙니다.")
        return

    update_mp3_tags_eyed3(args.folder, args.delimeter, args.recursive)

if __name__ == "__main__":
    main()