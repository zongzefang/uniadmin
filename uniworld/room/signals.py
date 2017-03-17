from django.dispatch import receiver
from django.db.models.signals import post_init, post_delete, post_save
from room.models import Room
from uniworld.utils import invalidate_cache


@receiver([post_init, post_delete], sender=Room.participants.through, weak=False, dispatch_uid='room_status_chack')
def assert_full(instance, **kwargs):
    room = instance.room
    if room.participants.count() == room.max_participants:
        room.full = True
    else:
        room.full = False
    room.save()


@receiver([post_save], sender=Room, weak=False, dispatch_uid='room_cache_refresh')
def refresh_cache(instance, **kwargs):
    path = '/room/' + str(instance.id) + '/'
    print('refreshing room cache', invalidate_cache(path))
