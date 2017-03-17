from django.db import models
from django.utils import timezone
from easy_thumbnails.fields import ThumbnailerImageField
from user.models import *
from polymorphic.models import PolymorphicModel



def upload_to(instance, filename):
    return 'uploads/{}/{}/avatars/{}'.format(instance.__class__.__name__, instance.id, filename)


class Room(PolymorphicModel):
    # Users
    host = models.ForeignKey('user.UniUser', related_name='hosted_rooms')
    participants = models.ManyToManyField('user.UniUser', related_name='joined_rooms', through='Participance')
    marked_users = models.ManyToManyField('user.UniUser', related_name='marked_rooms', blank=True)

    # Room info
    title = models.CharField(max_length=30)
    title_labels = models.ManyToManyField('other.TitleLabel', blank=True)
    cover = ThumbnailerImageField(blank=True, null=True, upload_to=upload_to)
    description = models.TextField(blank=True, null=True)
    labels = models.ManyToManyField('other.Label', related_name='rooms', blank=True)
    max_participants = models.PositiveSmallIntegerField(default=2, null=True)
    date_time_start = models.DateTimeField(default=timezone.now)
    date_time_end = models.DateTimeField(blank=True, null=True)
    views = models.PositiveIntegerField(default=0)
    #Convenience for app
    is_advanced=models.BooleanField(default=False)
    is_matchroom=models.BooleanField(default=False)
    is_chatroom=models.BooleanField(default=False)

    #Options, use json.dumps
    options = models.TextField(blank=True, null=True)

    # Location
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    location_string = models.CharField(max_length=30)

    # Status
    expired = models.BooleanField(default=False)
    banned = models.BooleanField(default=False)
    full = models.BooleanField(default=False)
    show = models.BooleanField(default=True)

    class Meta:
        ordering = ['-id']


class AdvancedRoom(Room):
    # Universities in which to advertise
    advertising = models.ManyToManyField('other.University', related_name='advanced_rooms')
    # Json.dumps
    # Whether application is required
    apply = models.BooleanField(default=False)

    class Meta:
        ordering = ['-id']

class MatchRoom(Room):
    matching_time=models.DateTimeField()
    matched=models.BooleanField(default=False)
    groups=models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['-id']



class Participance(models.Model):
    room = models.ForeignKey(Room)
    user = models.ForeignKey('user.UniUser')

    class Meta:
        unique_together = ('room', 'user')
