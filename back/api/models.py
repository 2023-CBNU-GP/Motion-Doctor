# Create your models here.
import os
from django.contrib.auth.models import User
from django.db import models


def upload_path(filename):
    return os.path.join('media')


class LinkServicesUploads(models.Model):
    video_link = models.CharField(blank=True, null=True, max_length=50)


class VideoServicesUploads(models.Model):
    file_name = models.CharField(blank=True, null=True, max_length=1500)
    file_video = models.FileField(blank=True, null=True, upload_to='media/')
