from celery import shared_task
from googleapiclient.discovery import build
from .models import Video
from datetime import datetime

@shared_task
def fetch_and_store_videos():
    youtube = build('youtube', 'v3', developerKey='AIzaSyDpTnhfUvO3aOUEEFZ4ptrw96iKvjS207g')
    request = youtube.search().list(q='cricket', type='video', part='snippet', maxResults=50)
    response = request.execute()

    for item in response['items']:
        video = Video(
            title=item['snippet']['title'],
            description=item['snippet']['description'],
            published_datetime=datetime.strptime(item['snippet']['publishedAt'], '%Y-%m-%dT%H:%M:%SZ'),
            thumbnails_urls=item['snippet']['thumbnails']
        )
        video.save()
