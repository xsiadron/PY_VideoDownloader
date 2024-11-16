import yt_dlp
import json
import os
import requests
from datetime import datetime
from utils import clean_description, create_folder, format_timestamp
from config import MAIN_FOLDER, COOKIES_FILE, MAX_RETRIES, VIDEO_FORMAT, THUMBNAIL_FORMAT, VIDEOS_FOLDER_NAME, THUMBNAILS_FOLDER_NAME


def download_tiktok_videos(username):
    create_folder(MAIN_FOLDER)

    folder_name = os.path.join(MAIN_FOLDER, username)
    videos_folder = os.path.join(folder_name, VIDEOS_FOLDER_NAME)
    thumbnails_folder = os.path.join(folder_name, THUMBNAILS_FOLDER_NAME)

    create_folder(videos_folder)
    create_folder(thumbnails_folder)

    url = f"https://www.tiktok.com/@{username}"
    ydl_opts = {
        'outtmpl': f'{videos_folder}/%(id)s.%(ext)s',
        'noplaylist': True,
        'merge_output_format': 'mp4',
        'cookies': COOKIES_FILE,
        'format': VIDEO_FORMAT,
        'retries': MAX_RETRIES,
        'ignoreerrors': True
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            result = ydl.extract_info(url, download=False)
            videos = result.get('entries', [])

            if not videos:
                return

            videos = sorted(videos, key=lambda x: (
                x['upload_date'], x.get('timestamp', 0)))
            video_data = {}

            for index, video in enumerate(videos):
                video_id = video['id']
                description = clean_description(
                    video.get('description', 'no_description'))
                upload_timestamp = datetime.fromtimestamp(
                    video.get('timestamp', 0))
                formatted_date = format_timestamp(video.get('timestamp', 0))
                full_url = f"https://www.tiktok.com/@{username}/video/{video_id}"
                file_name = f"{index}_{formatted_date}_{description}.mp4"
                thumbnail_file_name = f"{index}_{formatted_date}_{description}.{THUMBNAIL_FORMAT}"

                try:
                    ydl_opts['outtmpl'] = f'{videos_folder}/{file_name}'
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl_download:
                        ydl_download.download([full_url])

                    if 'thumbnail' in video:
                        thumbnail_url = video['thumbnail']
                        thumbnail_path = os.path.join(
                            thumbnails_folder, thumbnail_file_name)
                        download_thumbnail(thumbnail_url, thumbnail_path)
                        thumbnail_relative_path = f"{THUMBNAILS_FOLDER_NAME}/{thumbnail_file_name}"
                    else:
                        thumbnail_relative_path = 'no_thumbnail'

                except Exception as e:
                    print(f"Failed to download video {video_id}: {e}")
                    continue

                video_data[index] = {
                    'date': upload_timestamp.strftime('%Y-%m-%d %H:%M'),
                    'description': video.get('description', 'no_description'),
                    'url': full_url,
                    'title': video.get('title', 'no_title'),
                    'id': video['id'],
                    'view_count': video.get('view_count', 'no_data'),
                    'like_count': video.get('like_count', 'no_data'),
                    'comment_count': video.get('comment_count', 'no_data'),
                    'thumbnail': thumbnail_relative_path
                }

            json_file_path = os.path.join(folder_name, f'{username}.json')
            with open(json_file_path, 'w', encoding='utf-8') as json_file:
                json.dump(video_data, json_file, ensure_ascii=False, indent=4)

            print(
                f"Downloaded {len(videos)} videos and saved data to {json_file_path}")

    except Exception as e:
        print(f"An error occurred: {e}")


def download_thumbnail(url, path):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            with open(path, 'wb') as file:
                file.write(response.content)
    except Exception as e:
        print(f"Error downloading thumbnail: {e}")
