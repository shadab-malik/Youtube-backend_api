from celery import shared_task
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from .models import Video
from datetime import datetime

@shared_task
def fetch_and_store_videos(api_keys):
    for api_key in api_keys:
        try:
            youtube = build('youtube', 'v3', developerKey=api_key)

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
            break # If the API call is successful, break the loop
        
        except HttpError as e:
            if e.resp.status == 403: # Quota exceeded
                error_message = e.content.decode('utf-8')
                if 'quota' in error_message.lower():
                    continue # Try the next API key
                else:
                    raise # Re-raise the exception if it's not quota related
            else:
                raise # Re-raise the exception if it's not a quota error
