from django.db import models
from django.contrib.auth.models import AbstractUser
from easy_thumbnails.fields import ThumbnailerImageField
from other.models import *
from polymorphic.models import PolymorphicModel
from room.models import *

def upload_to(instance, filename):
    return 'uploads/{}/{}/avatars/{}'.format(instance.__class__.__name__, instance.id, filename)


class UniUser(AbstractUser):
    name = models.CharField(max_length=15)
    avatar = ThumbnailerImageField(blank=True, null=True, upload_to=upload_to)
    gender = models.NullBooleanField(blank=True, null=True)
    signature = models.CharField(max_length=50, blank=True)
    university = models.ForeignKey('other.University', blank=True)
    department = models.CharField(max_length=20, blank=True)
    year = models.CharField(max_length=4, blank=True)
    follows = models.ManyToManyField('self', related_name='followers', blank=True)
    labels = models.ManyToManyField('other.Label', blank=True)
    # Thumbs recieved as participant
    p_thumb_ups_from = models.ManyToManyField('self', symmetrical=False, related_name='p_thumb_ups_to',
                                              through='ParticipantThumbUp', through_fields=('target', 'user'))
    p_thumb_downs_from = models.ManyToManyField('self', symmetrical=False, related_name='p_thumb_downs_to',
                                                through='ParticipantThumbDown', through_fields=('target', 'user'))
    # Thumbs recieved as host
    h_thumb_ups_from = models.ManyToManyField('self', symmetrical=False, related_name='h_thumb_ups_to',
                                              through='HostThumbUp', through_fields=('target', 'user'))
    h_thumb_downs_from = models.ManyToManyField('self', symmetrical=False, related_name='h_thumb_downs_to',
                                                through='HostThumbDown', through_fields=('target', 'user'))


class Organization(UniUser):
    description_ch = models.TextField()
    description_en = models.TextField()
    location = models.TextField()
    # license....


class ParticipantThumbUp(models.Model):
    user = models.ForeignKey(UniUser, related_name='p_thumb_ups_sent')
    target = models.ForeignKey(UniUser, related_name='p_thumb_ups_recv')
    text=models.TextField(blank=True)
    room = models.ForeignKey('room.Room')

    class Meta:
        unique_together = ('room', 'user', 'target')


class ParticipantThumbDown(models.Model):
    user = models.ForeignKey(UniUser, related_name='p_thumb_downs_sent')
    target = models.ForeignKey(UniUser, related_name='p_thumb_downs_recv')
    text=models.TextField()
    room = models.ForeignKey('room.Room')

    class Meta:
        unique_together = ('room', 'user', 'target')


class HostThumbUp(models.Model):
    user = models.ForeignKey(UniUser, related_name='h_thumb_ups_sent')
    target = models.ForeignKey(UniUser, related_name='h_thumb_ups_recv')
    text=models.TextField(blank=True)
    room = models.ForeignKey('room.Room')

    class Meta:
        unique_together = ('room', 'user', 'target')


class HostThumbDown(models.Model):
    user = models.ForeignKey(UniUser, related_name='h_thumb_downs_sent')
    target = models.ForeignKey(UniUser, related_name='h_thumb_downs_recv')
    text=models.TextField()
    room = models.ForeignKey('room.Room')

    class Meta:
        unique_together = ('room', 'user', 'target')
