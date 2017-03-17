from django.conf.urls import url, include
from user.views import *

user_urls = [
    url(r'^$', user_detail),
    url(r'^follow/$', follow),
    url(r'^unfollow/$', unfollow),
]

account_setting_urls=[
    url(r'^$', my_detail),
    url(r'^rooms/$', my_rooms),
    url(r'^edit/$', edit_profile),
    url(r'^upload_avatar/$', upload_avatar),
]
