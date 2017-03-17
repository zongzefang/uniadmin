'''
Core views
'''

from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from room.serializers import *
from other.models import *
from message.models import *
from room.models import *
from django.views.decorators.cache import cache_page
from user.models import *
import django_filters

@api_view(['GET'])
@cache_page(60*10)
@authentication_classes(())
@permission_classes(())
def plaza(request):
    pass

@api_view(['GET'])
def quick_join(request):
    pass

class RoomFilter(django_filters.rest_framework.FilterSet):
    labels=django_filters.ModelMultipleChoiceFilter(
        name='labels__id',
        to_field_name='id',
        queryset=Label.objects.all())
    title=django_filters.CharFilter(name='title',lookup_expr='contains')
    description=django_filters.CharFilter(name='description',lookup_expr='contains')
    time=django_filters.DateTimeFromToRangeFilter(name='date_time_start', lookup_expr='__date')

    class Meta:
        model = Room
        fields = ['id']


class SearchView(ListAPIView):
    queryset = Room.objects.filter(expired=False, banned=False, show=True)
    serializer_class = RoomInfoSerializer
    filter_class = RoomFilter



@api_view(['POST'])
def create_room(request):
    try:
        request.data['host'] = request.user.id
        if 'is_matchroom' in request.data and request.data['is_matchroom']:
            serializer = MatchRoomCreateSerializer(data=request.data)
        else:
            serializer = RoomCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            Participance.objects.create(room=serializer.instance, user=request.user)
            return Response(serializer.data['id'], status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        print(e)
        return Response(status=status.HTTP_400_BAD_REQUEST)

#TODO: Search






