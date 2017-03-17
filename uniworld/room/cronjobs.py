from django_cron import CronJobBase, Schedule
from django.core.cache import caches
from room.models import *
import json


class RefreshPlaza(CronJobBase):
    RUN_EVERY_MINS = 10
    RETRY_AFTER_FAILURE_MINS = 0.1

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS, retry_after_failure_mins=RETRY_AFTER_FAILURE_MINS)
    code = 'room.cronjobs.refresh_plaza'

    def do(self):
        pass  # do your thing here


class ExpirationCheck(CronJobBase):
    RUN_AT_TIMES = ['00:00']

    schedule = Schedule(run_at_times=RUN_AT_TIMES)
    code = 'room.cronjobs.expiration_check'

    def do(self):
        pass  # do your thing here


class StartMatching(CronJobBase):
    LUNCH_TIMES = ['11:15', '11:30', '11:45', '12:00', '12:15', '12:30']
    RETRY_AFTER_FAILURE_MINS = 0.1

    schedule = Schedule(run_at_times=LUNCH_TIMES, retry_after_failure_mins=RETRY_AFTER_FAILURE_MINS)
    code = 'room.cronjobs.start_matching'

    def do(self):
        rooms = MatchRoom.objects.filter(matched=False)
        for room in rooms:
            groups = []
            females = room.participants.filter(gender=0).order_by('?').values_list('id')
            males = room.participants.filter(gender=1).order_by('?').values_list('id')
            whatevers = room.participants.exclude(gender=0).exclude(gender=1).order_by('?').values_list('id')
            females = list(females)
            males = list(males)
            whatevers = list(whatevers)
            if len(females) > len(males):
                whatevers += females[len(males):]
                females = females[:len(males)]
            elif len(females) == len(males):
                whatevers += males[len(males):]
                males = males[:len(males)]
            groups.extend(list(map(lambda x, y: (x, y), males, females)))
            groups.extend(list(map(lambda x, y: (x, y), whatevers[:len(whatevers)], whatevers[len(whatevers):])))
            room.group = json.dumps(groups)
            room.save()
            for group in groups:
                r=Room.objects.create(title='Chat room', is_chatroom=True)
                r.participants.add(group[0], group[1])
