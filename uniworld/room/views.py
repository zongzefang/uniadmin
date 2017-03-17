from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from django.core.cache import cache
from django.views.decorators.cache import cache_page

from room.serializers import *
from room.permissions import *
from user.models import ParticipantThumbDown, ParticipantThumbUp, HostThumbDown, HostThumbUp
from message.models import *
from message.paginators import *
from message.serializers import *
import django_filters


@api_view(['GET'])
@cache_page(60*60)
def room_detail(request, room_id):
    try:
        room = Room.objects.get(id=room_id)
    except Room.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if room.banned:
        return Response(status=status.HTTP_403_FORBIDDEN)
    #Saving the room causes cache to refresh, ignoring counts for now
    #room.views += 1
    #room.save()
    print('no cache!')
    return Response(RoomDetailSerializer(room).data, status=status.HTTP_200_OK)


@api_view(['GET'])
def room_participants(request, room_id):
    try:
        room = Room.objects.get(id=room_id)
        data = RoomDetailSerializer(room).data
        return Response({'participants': data['participants'], 'host': data['host']}, status=status.HTTP_200_OK)
    except Exception as e:
        print(e)
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def join(request, room_id):
    try:
        room = Room.objects.get(id=room_id)
        try:
            apply = room.apply
        except:
            apply = False
        if room.full or room.expired or room.banned or apply:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        Participance.objects.get_or_create(room=room, user=request.user)
        return Response(status=status.HTTP_200_OK)
    except Exception as e:
        print(e)
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def apply(request, room_id):
    try:
        room = Room.objects.get(room_id=room_id)
        if not room.apply:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        Application.objects.create(room=room, user=request.user, text=request.data['text'])
        return Response(status=status.HTTP_200_OK)
    except Exception as e:
        print(e)
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def leave(request, room_id):
    try:
        room = Room.objects.get(id=room_id)
        if room.expired or room.banned:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        if room.is_advanced:
            if room.host is request.user:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        participance = Participance.objects.get(room=room, user=request.user)
        participance.delete()
        if room.participants.count()==0:
            room.expired=True
            room.save()
            return Response(status=status.HTTP_200_OK)
        room.host=room.participants.first()
        room.save()
        return Response(status=status.HTTP_200_OK)
    except Exception as e:
        print(e)
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def mark(request, room_id):
    try:
        room = Room.objects.get(id=room_id)
        user = request.user
        if room.banned:
            return Response(status=status.HTTP_403_FORBIDDEN)
        room.marked_users.add(user)
        return Response(status=status.HTTP_200_OK)
    except Exception as e:
        print(e)
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def unmark(request, room_id):
    try:
        room = Room.objects.get(id=room_id)
        room.marked_users.remove(request.user)
        return Response(status=status.HTTP_200_OK)
    except Exception as e:
        print(e)
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def thumb_up(request, room_id, user_id):
    try:
        room = Room.objects.get(id=room_id)
        user = Room.participants.get(id=user_id)
        if not IsParticipant(request, room):
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        if room.host_id == user.id:
            HostThumbUp.objects.create(user=request.user, target=user, text=request.data['text'], room=room)
        else:
            ParticipantThumbUp.objects.create(user=request.user, target=user, text=request.data['text'], room=room)
        return Response(status=status.HTTP_200_OK)
    except Exception as e:
        print(e)
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def thumb_down(request, room_id, user_id):
    try:
        room = Room.objects.get(id=room_id)
        user = Room.participants.get(id=user_id)
        if not IsParticipant(request, room):
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        if room.host_id == user.id:
            HostThumbDown.objects.create(user=request.user, target=user, text=request.data['text'], room=room)
        else:
            ParticipantThumbDown.objects.create(user=request.user, target=user, text=request.data['text'], room=room)

        return Response(status=status.HTTP_200_OK)
    except Exception as e:
        print(e)
        return Response(status=status.HTTP_400_BAD_REQUEST)


'''
Message
'''


@api_view(['POST'])
def send_message(request, room_id):
    try:
        room = Room.objects.get(id=room_id)
        participants = room.participants.values_list('id', flat=True)
        if not IsParticipant(request, room):
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        message = Message.objects.create(sender=request.user, room=room, text=request.data['text'])
        cache.set_many({str(p) + '_unread_' + str(room.id): (
        cache.get(str(p) + '_unread_' + str(room.id), default=[]).extend([message])) for p in participants},timeout=10)
        return Response(message.id, status=status.HTTP_200_OK)
    except Exception as e:
        print(e)
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def send_reply(request, room_id, questionnaire_id):
    try:
        room = Room.objects.get(id=room_id)
        if not IsParticipant(request, room):
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        questionnaire = Questionnaire.get(id=questionnaire_id)
        if questionnaire.is_announcement:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        Reply.objects.create(questionnaire=questionnaire, user=request.user, text=request.data['text'])
        return Response(status=status.HTTP_200_OK)
    except Exception as e:
        print(e)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class MessageHistory(ListAPIView):
    serializer_class = MessageSerializer
    pagination_class = RoomMessagePagination

    def get_queryset(self):
        room = Room.objects.get(id=self.kwargs['room_id'])
        if self.request.user not in room.participants:
            self.permission_denied(self.request)
        return room.messages


'''
Host
'''


@api_view(['PUT'])
def room_edit(request, room_id):
    room = Room.objects.get(id=room_id)
    if not IsHost(request.user, room):
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    if room.expired:
        return Response(status=status.HTTP_403_FORBIDDEN)
    serializer = RoomDetailSerializer(room, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def room_close(request, room_id):
    try:
        room = Room.objects.get(id=room_id)
        if not IsHost(request, room):
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        room.expired = True
        room.save()
        return Response(status=status.HTTP_200_OK)
    except Exception as e:
        print(e)
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def upload_avatar(request, room_id):
    try:
        room = Room.objects.get(id=room_id)
        cover = request.FILES.get('cover')
    except Exception:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    if not cover:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    if cover.size < 5000000:
        room.cover = cover
        room.save()
        return Response(status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def create_announcement(request, room_id):
    try:
        room = Room.objects.get(id=room_id)
        if not IsHost(request, room):
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        announcement = Questionnaire.create(title=request.data['title'], description=request.data['description'],
                                            room=room)
        return Response(announcement.id, status=status.HTTP_200_OK)
    except Exception as e:
        print(e)
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def delete_announcement(request, room_id, announcement_id):
    try:
        room = Room.objects.get(id=room_id)
        if not IsHost(request, room):
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        announcement = Questionnaire.objects.get(id=announcement_id)
        announcement.delete()
        return Response(status=status.HTTP_200_OK)
    except Exception as e:
        print(e)
        return Response(status=status.HTTP_400_BAD_REQUEST)
