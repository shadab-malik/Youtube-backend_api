# YouTube Data API

## Project Goal

To make an API to fetch latest videos sorted in reverse chronological order of their publishing date-time from YouTube for a given tag/search query in a paginated response.

## Basic Requirements:

- Server should call the YouTube API continuously in background (async) with some interval (say 10 seconds) for fetching the latest videos for a predefined search query taken as "CRICKET" and should store the data of videos (specifically these fields - Video title, description, publishing datetime, thumbnails URLs and any other fields you require) in a database with proper indexes.
- A GET API which returns the stored video data in a paginated response sorted in descending order of published datetime.
- A basic search API to search the stored videos using their title and description.
- Dockerize the project.
- It should be scalable and optimised.


### Technologies Used.
The command below, build the complete application using docker-compose
* Django Rest Framework 
* Redis (used from Docker)
* Celery Worker (pip install celery)
* Celery Beat

### How to run the application. 
 * python manage.py runserver
 * celery -A video_api_project worker --pool=solo (for celery worker)

### Url for the api call.
    http://localhost:8000/videos/
  You can also specify the page size and number of pages you want to see as cursor pagination is used.
    http://localhost:8000/videos/?page_size=10&page=1

## Additional Notes
- The application utilizes Celery with Redis as a message broker for background task scheduling.
- Proper documentation and comments are provided within the codebase for further understanding and maintenance.

