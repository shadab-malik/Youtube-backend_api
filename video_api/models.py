
from django.db import models

class Video(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    published_datetime = models.DateTimeField()
    thumbnails_urls = models.JSONField()

    class Meta:
        ordering = ['-published_datetime']
