from django.conf.urls import url
from . import views
app_name = 'uniadmin'

urlpatterns=[
    url(r'^/$',views.room_index, name='room_index'),
    url(r'^room/(?P<room_id>[0-9]+)/questionaire',views.room_questionaire, name='room_questionaire'),
    url(r'^room/(?P<room_id>[0-9]+)/participant',views.room_participant, name='room_participant'),
    url(r'^room/(?P<room_id>[0-9]+)/participant(?P<participanct_id>[0-9]+)/delete',views.room_participant_delete, name='room_participant_delete'),
  #  url(r'^create',views.room_create, name='room_create'),
    url(r'^test$',views.test),
]
