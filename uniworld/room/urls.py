from django.conf.urls import url, include
from room.views import *

room_urls = [
    #Basic
    url(r'^$', room_detail),
    url(r'^participants/$', room_participants),
    url(r'^join/$', join),
    url(r'^apply/$', apply),
    url(r'^leave/$', leave),
    url(r'^mark/$', mark),
    url(r'^unmark/$',unmark),
    url(r'^thumb_up/(?P<user_id>[0-9]+)/$',thumb_up),
    url(r'^thumb_down/(?P<user_id>[0-9]+)/$',thumb_down),
    #Message
    url(r'^send_message/$', send_message),
    url(r'^questionnaire/(?P<questionnaire_id>[0-9]+)/$', send_reply),
    url(r'^messages/$', MessageHistory.as_view()),
    #Host
    url(r'^close/$', room_close),  #Necessary?
    url(r'^upload_avatar/$', upload_avatar),
    url(r'^edit/$', room_edit),
    url(r'^create_announcement/$', create_announcement),
    url(r'^delete_announcement/(?P<announcement_id>[0-9]+)/$', delete_announcement),
]
