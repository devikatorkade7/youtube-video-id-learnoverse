

# Create your models here.
# app/models.py
from django.db import models

class Video(models.Model):
    title = models.CharField(max_length=255)
    youtube_id = models.CharField(max_length=50)

    def __str__(self):
        return self.title
