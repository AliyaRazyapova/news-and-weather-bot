from django.db import models


class Message(models.Model):
    user_id = models.IntegerField()
    message = models.TextField()
    is_bot = models.BooleanField()
    timestamp = models.DateTimeField(auto_now_add=True)
