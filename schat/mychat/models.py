from django.db import models
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session


class ChatMessage(models.Model):
    sender   = models.ForeignKey(User, related_name = 'sender_user')
    receiver = models.ForeignKey(User, related_name = 'receiver_user')
    message  = models.CharField(max_length = 200)
    received_at = models.DateTimeField(auto_now_add = True)
    session = models.ForeignKey(Session)
    is_read = models.BooleanField()

class LastActive(models.Model):    
    user   = models.OneToOneField(User, primary_key = True)
    received_at = models.DateTimeField(auto_now = True)
    session = models.ForeignKey(Session)

    def __str__(self):
        return self.user.username

class VideoSession(models.Model):
    sender   = models.ForeignKey(User, related_name = 'sender_user1')
    receiver = models.ForeignKey(User, related_name = 'receiver_user1')
    session_id  = models.CharField(max_length = 255)
    token_id    = models.TextField()
    
    