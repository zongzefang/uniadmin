from django.conf.urls import url, include
from django.conf.urls.static import static
from django.conf import settings
from other.views import *

other_urls = [
    url(r'^label/create/$', create_label),
]

label_urls=[
    url(r'^detail/$', label_detail),
    url(r'^follow/$', follow),
    url(r'^unfollow/$', unfollow),
]

university_urls=[
    url(r'^$', university_detail),
]
