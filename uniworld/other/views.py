from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.generics import ListAPIView
from other.models import *
from other.serializers import *
import django_filters


@api_view(['POST'])
@permission_classes((IsAdminUser,))
def create_label(request):
    serializer = LabelDetailSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def university_detail(request, label_id):
    try:
        univeristy = University.objects.get(id=label_id)
    except University.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    return Response(UniversitySerializer(univeristy).data, status=status.HTTP_200_OK)


@api_view(['GET'])
def label_detail(request, label_id):
    try:
        label = Label.objects.get(id=label_id)
    except Label.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    return Response(LabelDetailSerializer(label).data, status=status.HTTP_200_OK)


@api_view(['GET'])
def follow(request, label_id):
    try:
        user = request.user
        label = Label.objects.get(id=label_id)
        user.labels.add(label)
        return Response(status=status.HTTP_200_OK)
    except Exception as e:
        print(e)
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def unfollow(request, label_id):
    try:
        user = request.user
        label = Label.objects.get(id=label_id)
        user.labels.remove(label)
        return Response(status=status.HTTP_200_OK)
    except Exception as e:
        print(e)
        return Response(status=status.HTTP_400_BAD_REQUEST)

class LabelSearch(ListAPIView):
    queryset = Label.objects.all
    serializer_class = LabelInfoSerializer
    lookup_fields=('name',)