import argparse
from Basic_utils import ic

parser = argparse.ArgumentParser(description='YouTube 동영상 다운로드')
parser.add_argument('urls', nargs='+', help='다운로드할 YouTube 동영상 URL 목록')
parser.add_argument('--format', default='bestvideo[height<=1080][ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
                    help='다운로드할 포맷 (기본값: %(default)s)')
args = parser.parse_args()
urls = args.urls

ic(args)
ic(args.urls)
ic(args.format)

ic(args._get_args())

