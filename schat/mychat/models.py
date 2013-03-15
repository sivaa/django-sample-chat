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
    user   = models.OneToOneField(User)
    received_at = models.DateTimeField(auto_now = True)
    session = models.ForeignKey(Session)
    