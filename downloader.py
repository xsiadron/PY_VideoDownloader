import yt_dlp
import json
import os
from datetime import datetime
from utils import clean_description, create_folder, format_timestamp

def download_tiktok_videos(username):
    main_folder = "data"
    create_folder(main_folder)
    
    folder_name = os.path.join(main_folder, username)
    create_folder(folder_name)

    url = f"https://www.tiktok.com/@{username}"
    print(f"Pobieranie filmów z profilu: {url}")

    ydl_opts = {
        'outtmpl': f'{folder_name}/%(id)s.%(ext)s',
        'noplaylist': True,
        'merge_output_format': 'mp4',
        'cookies': 'cookies.txt',
        'format': 'bestvideo+bestaudio/best',
        'retries': 5,
        'ignoreerrors': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            result = ydl.extract_info(url, download=False)
            videos = result.get('entries', [])

            if not videos:
                print("Brak filmów dla tego użytkownika.")
                return

            videos = sorted(videos, key=lambda x: (x['upload_date'], x.get('timestamp', 0)))
            video_data = {}

            for index, video in enumerate(videos):
                video_id = video['id']
                description = clean_description(video.get('description', 'brak_opisu'))
                upload_timestamp = datetime.fromtimestamp(video.get('timestamp', 0))
                formatted_date = format_timestamp(video.get('timestamp', 0))
                full_url = f"https://www.tiktok.com/@{username}/video/{video_id}"
                file_name = f"{index}_{formatted_date}_{description}.mp4"

                try:
                    ydl_opts['outtmpl'] = f'{folder_name}/{file_name}'
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl_download:
                        ydl_download.download([full_url])
                except Exception as e:
                    print(f"Nie udało się pobrać filmu {video_id}: {e}")
                    continue

                video_data[index] = {
                    'date': upload_timestamp.strftime('%Y-%m-%d %H:%M'),
                    'description': video.get('description', 'brak_opisu'),
                    'url': full_url,
                    'title': video.get('title', 'brak_tytułu'),
                    'id': video['id'],
                    'view_count': video.get('view_count', 'brak_danych'),
                    'like_count': video.get('like_count', 'brak_danych'),
                    'comment_count': video.get('comment_count', 'brak_danych')
                }

            json_file_path = os.path.join(folder_name, f'{username}.json')
            with open(json_file_path, 'w', encoding='utf-8') as json_file:
                json.dump(video_data, json_file, ensure_ascii=False, indent=4)

            print(f"Pobrano {len(videos)} filmów i zapisano dane do {json_file_path}")

    except Exception as e:
        print(f"Wystąpił błąd: {e}")
