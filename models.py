from django.db import models


class FacebookPost(models.Model):
    message = models.TextField()
    

class LinkedInPost(models.Model):
    massage = models.TextField()
    

class TwitterPost(models.Model):
    massage = models.CharField(max_length=280)
   