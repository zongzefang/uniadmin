from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework import generics
from django.utils.timezone import utc
from django.contrib.auth import authenticate
from user.models import *
from user.serializers import *
# from user.permissions import *
from user.utils import EmailVerification, Confirm
from user.authentication import *
from room.serializers import RoomInfoSerializer
import django_filters


class ObtainExpiringAuthToken(ObtainAuthToken):
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            token, created = Token.objects.get_or_create(user=serializer.validated_data['user'])
            valid_since = (datetime.utcnow() - timedelta(days=3))
            if not created and token.created < valid_since:
                token.delete()
                token = Token.objects.create(user=serializer.validated_data['user'])
                token.created = datetime.utcnow()
                token.save()
            return Response({'token': token.key})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes(())
@authentication_classes(())
def register(request):
    try:
        user = UniUser.objects.get(username=request.data['username'])
        if not user.is_active:
            user.delete()
    except Exception:
        pass
    serialized = CreateUniUserSerializer(data=request.data)
    if serialized.is_valid():
        university = EmailVerification(serialized.initial_data["username"], serialized.initial_data["email"])
        if not university:
            return Response("Sorry but the email you provided is not supported by Uniworld for now.",
                            status=status.HTTP_401_UNAUTHORIZED)
        UniUser.objects.create_user(
            email=serialized.initial_data["email"],
            username=serialized.initial_data["username"],
            password=serialized.initial_data["password"],
            university=university,
            is_active=False
        )
        return Response(
            "Congratulations, you have successfully registered. \
            Please check your email to activate your account! \
            Due to some reason, it may take a while to receive the activation email...",
            status=status.HTTP_201_CREATED)
    else:
        return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes(())
@authentication_classes(())
def activate(request, token):
    username = Confirm(token)
    user = UniUser.objects.get(username=username)
    user.is_active = True
    user.save()
    return Response("Congratulations, " + username + ", You have activated your account!", status=status.HTTP_200_OK)


@api_view(['GET'])
def get_id(request):
    return Response(request.user.id, status=status.HTTP_200_OK)


@api_view(['GET'])
def user_detail(request, user_id):
    try:
        user = UniUser.objects.get(id=user_id)
    except UniUser.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    return Response(UserDetailSerializer(user).data, status=status.HTTP_200_OK)

@api_view(['GET'])
def my_detail(request):
    return Response(UserDetailSerializer(request.user).data, status=status.HTTP_200_OK)

@api_view(['GET'])
def my_rooms(request):
    joined=RoomInfoSerializer(request.user.joined_rooms.filter(expired=False), many=True)
    marked=RoomInfoSerializer(request.user.marked_rooms.filter(expired=False), many=True)
    hosted=RoomInfoSerializer(request.user.hosted_rooms.filter(expired=False), many=True)
    return Response({'joined': joined.data, 'marked':marked.data, 'hosted':hosted.data}, status=status.HTTP_200_OK)


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
def follow(request, user_id):
    try:
        if int(user_id) == request.user.id:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        user = UniUser.objects.get(id=user_id)
        request.user.follows.add(user)
    except UniUser.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    return Response(status=status.HTTP_200_OK)


@api_view(['GET'])
def unfollow(request, user_id):
    try:
        if int(user_id) == request.user.id:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        user = UniUser.objects.get(id=user_id)
        request.user.follows.remove(user)
    except UniUser.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    return Response(status=status.HTTP_200_OK)


