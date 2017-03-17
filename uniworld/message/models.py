from django.db import models
from user.models import UniUser
from room.models import Room

class Questionnaire(models.Model):
    is_announcement = models.BooleanField(default=True)
    title = models.TextField()
    description = models.TextField(blank=True, null=True)
    room = models.ForeignKey('room.Room', related_name='questionnaires')
    choices = models.TextField(blank=True, null=True)  # json.dumps


class Reply(models.Model):
    text = models.TextField()
    questionnaire = models.ForeignKey('message.Questionnaire', related_name='replies')
    user = models.ForeignKey('user.UniUser', blank=True, null=True)


class Message(models.Model):
    room = models.ForeignKey('room.Room', related_name='messages')
    sender = models.ForeignKey('user.UniUser')
    text = models.TextField()
    time = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-id']


class Application(models.Model):
    room = models.ForeignKey('room.AdvancedRoom')
    user = models.ForeignKey('user.UniUser')
    text = models.TextField()
