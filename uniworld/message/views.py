from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from django.core.cache import cache
from other.models import *
from other.serializers import *
from message.serializers import *
from time import sleep

@api_view(["GET"])
def receive_messages(request):
    id=int(request.GET.get('id'))
    room_messages={}
    room_questionnaires={}
    rooms=request.user.joined_rooms.all()
    '''
    Non-cache part
    '''
    for room in rooms:
        messages=room.messages.filter(id__gt=id)
        questionnaires=room.questionnaires(id__gt=id)
        if messages.count():
            room_messages[room.id]=MessageSerializer(messages, many=True).data
        if questionnaires.count():
            room_questionnaires[room.id]=QuestionnaireSerializer(questionnaires, many=True).data
    if len(room_messages) or len(room_questionnaires):
        data={'messages': room_messages, 'questionnaires': room_questionnaires}
        return Response(data, status=status.HTTP_200_OK)
    '''
    cache part
    '''
    room_ids=rooms.values_list('id', flat=True)
    for i in range(30):
        for room_id in room_ids:
            message=cache.get(str(room_id)+'_message')
            if message:
                room_messages[room.id]=[MessageSerializer(message)]
        if len(room_messages):
            return Response({'messages':room_messages}, status=status.HTTP_200_OK)
        sleep(1)
    return Response(status=status.HTTP_200_OK)