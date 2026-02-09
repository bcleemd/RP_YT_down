import eyed3
import os
import argparse
from prettytable import PrettyTable

def get_mp3_tags(folder_path):
    """
    지정된 폴더 내의 모든 MP3 파일에서 ID3 태그 정보를 추출합니다.
    """
    mp3_files = [f for f in os.listdir(folder_path) if f.lower().endswith('.mp3')]
    tag_data = []

    for mp3_file in mp3_files:
        file_path = os.path.join(folder_path, mp3_file)
        try:
            audio_file = eyed3.load(file_path)
            if audio_file and audio_file.tag:
                title = audio_file.tag.title if audio_file.tag.title else "N/A"
                artist = audio_file.tag.artist if audio_file.tag.artist else "N/A"
                album = audio_file.tag.album if audio_file.tag.album else "N/A"
                tag_data.append([mp3_file, title, artist, album])
            else:
                tag_data.append([mp3_file, "N/A (No ID3 Tag)", "N/A", "N/A"])
        except Exception as e:
            tag_data.append([mp3_file, f"Error: {e}", "N/A", "N/A"])
    return tag_data

def display_tags_as_table(tag_data):
    """
    추출된 ID3 태그 정보를 표 형태로 출력합니다.
    """
    if not tag_data:
        print("지정된 폴더에 MP3 파일이 없거나 태그를 읽을 수 없습니다.")
        return

    table = PrettyTable()
    table.field_names = ["파일 이름", "제목", "아티스트", "앨범"]
    table.align["파일 이름"] = "l"
    table.align["제목"] = "l"
    table.align["아티스트"] = "l"
    table.align["앨범"] = "l"

    for row in tag_data:
        table.add_row(row)
    print(table)

def main():
    parser = argparse.ArgumentParser(description="지정된 폴더 내 MP3 파일의 ID3 태그(제목, 아티스트, 앨범)를 표로 표시합니다.")
    parser.add_argument("folder_name", help="ID3 태그를 추출할 MP3 파일이 있는 폴더 경로")
    args = parser.parse_args()

    folder_path = args.folder_name

    if not os.path.isdir(folder_path):
        print(f"오류: '{folder_path}'는 유효한 디렉토리가 아닙니다.")
        return

    print(f"'{folder_path}' 폴더의 MP3 ID3 태그 정보를 불러오는 중...")
    tag_info = get_mp3_tags(folder_path)
    display_tags_as_table(tag_info)

if __name__ == "__main__":
    main()