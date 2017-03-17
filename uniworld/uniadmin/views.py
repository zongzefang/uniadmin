from django.shortcuts import  HttpResponse, render_to_response,HttpResponseRedirect, reverse
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.decorators import login_required
from

#MVC MODE
@login_required
def index(request):
    rooms_filter = request.GET.get('rooms_filter')
    if rooms_filter == 'underway':
        rooms = AdvancedRoom.objects.filter(expired = False)
    elif rooms_filter == 'finished':
        rooms = AdvancedRoom.objects.filter(expired = True)

    else:
        rooms =AdvancedRoom.objects.all()
        #房间种类过滤器

    username = request.user.username
    resp=json.dumps("11111",ensure_ascii=False)
    response=HttpResponse(resp)
    response['Access-Control-Allow-Origin']='*'
    response["Access-Control-Allow-Headers"] = "*"
    return response
       #房间列表页,/index

@login_required
def check_room(request, room_id):                           #检查房主是否为当前用户
    try:
        room = AdvancedRoom.objects.get(id = room_id)
    except ObjectDoesNotExist:
        return False
    if not room.host == request.user:             #user 还是 uniuser????
        return 'fake'
    return room

@login_required
def room_index(request, room_id = -1):
    room = check_room(request,room_id)
    if room =='fake':
        return HttpResponseRedirect(reverse('index'))
    return render_to_response('room_index.html',{'room':room})

@login_required()
def room_questionaire(request, room_id = -1):
    room = check_room(request, room_id)
    if room =='fake':
        return HttpResponseRedirect(reverse('index'))


    questionaire_filter = request.GET.get('rooms_filter')
    if questionaire_filter == 'Announcement':
        questionaires = room.questionaires.filter(is_announcement = True)


                                                               #问卷过滤器
    else :
        questionaires = room.questionaires.all()


    return render_to_response('questionaire.html',{'room':room, 'questionaires':questionaires})

@login_required
def room_participant(request,room_id=-1):
    room = check_room(request, room_id)
    if room =='fake':
        return HttpResponseRedirect(reverse('index'))
    participants = room.participants.all()
    return render_to_response('room_participant.html',{'participants':participants})

@login_required
def room_participant_delete(request, room_id=-1, participant_id = -1):
    room = check_room(request, room_id)
    if room =='fake':
        return HttpResponseRedirect(reverse('index'))
    participants = room.participants.all()
    try:
        participant = participants.get(id = participant_id)
    except:
        return HttpResponseRedirect(reverse("uniadmin:room_questionaire", args=[room_id]))
    participance = Participance.objects.get(room=room, user=participant)
    participance.delete()

    return HttpResponseRedirect(reverse("uniadmin:room_questionaire", args=[room_id]))


#@login_required
def test(request):

    resp=json.dumps("hello,xukaifeng",ensure_ascii=False)
    response=HttpResponse(resp)
    response['Access-Control-Allow-Origin']='*'
    response["Access-Control-Allow-Headers"] = "*"
    return response


#new ways


@api_view(['POST'])
def create_room(request):
    try:
        request.data['host'] = request.user_id
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


@api_view(['GET'])
def room_detail(request, room_id):
    try:
        room = Room.objects.get(id=room_id)
    except Room.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if room.banned:
        return Response(status=status.HTTP_403_FORBIDDEN)
    room.views += 1
    room.save()
    return Response(RoomDetailSerializer(room).data, status=status.HTTP_200_OK)


@api_view(['GET'])
def room_participants(request, room_id):
    try:
        room = Room.objects.get(id=room_id)
        return Response(RoomDetailSerializer(room).data['participants'], status=status.HTTP_200_OK)
    except Exception as e:
        print(e)
        return Response(status=status.HTTP_400_BAD_REQUEST)

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

@api_view(['GET'])
def user_detail(request, user_id):
    try:
        user = UniUser.objects.get(id=user_id)
    except UniUser.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    return Response(UserDetailSerializer(user).data, status=status.HTTP_200_OK)


@api_view(['POST'])
def upload_avatar(request):
    user = request.user
    try:
        avatar = request.FILES.get('avatar')
    except Exception:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    if not avatar:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    if avatar.size < 5000000:
        user.avatar = avatar
        user.save()
        data = UserDetailSerializer(user).data
        return Response([data['avatar'], data['avatar_thumbnail']], status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def edit_profile(request):
    user = request.user
    serializer = ProfileEditSerializer(user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
def approve(request, room_id,application_id):
    room = check_room(request, room_id)
    if room is None:
        return Response(status=status.HTTP_404_NOT_FOUND)

    try:
        application = Application.objects.get(id = application_id, room = room)
    except Application.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.GET.get('is_approved') is 'approved':
        Participance.objects.create(room = application.room, user=application.user)
        application.delete()
    elif request.GET.get('is_approved') is 'rejected':
        application.delete()

    return Response(status=status.HTTP_200_OK)


# Create your views here.
