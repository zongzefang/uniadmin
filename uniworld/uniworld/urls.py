"""uniworld URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from rest_framework.urlpatterns import format_suffix_patterns
from user.urls import *
from other.urls import *
from room.urls import *
from user.views import *
from other.views import *
from room.views import *
from message.views import *
from uniworld.views import *

core_urls = [
    url(r'^plaza/$', plaza),
    url(r'^quick_join/$', quick_join),
    url(r'^create/$', create_room),
    url(r'^search$', SearchView.as_view())
]

auth_urls=[
    url(r'^register/$', register),
    url(r'^activate/(?P<token>\w+.[-_\w]*\w+.[-_\w]*\w+)/$', activate),
    url(r'^token/$', ObtainExpiringAuthToken.as_view()),
    url(r'^myid/$', get_id),
]

urlpatterns = [
    #Apps
    url(r'^user/(?P<user_id>[0-9]+)/', include(user_urls)),
    url(r'^room/(?P<room_id>[0-9]+)/' ,include(room_urls)),
    url(r'^label/(?P<label_id>[0-9]+)/', include(label_urls)),
    url(r'^uniadmin/', uniadmin.views.index, name = 'index'),
    url(r'uniadmin/', include('uniadmin.urls')),
    #Others
    url(r'^admin/', include(other_urls)),   #Delete this in the future
    url(r'^profile/', include(account_setting_urls)),
    url(r'^label/search', LabelSearch.as_view()),
    url(r'^receive_messages/', receive_messages),
]

urlpatterns+=core_urls

urlpatterns+=auth_urls

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns = format_suffix_patterns(urlpatterns)
