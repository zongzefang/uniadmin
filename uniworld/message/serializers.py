from rest_framework import serializers
from user.serializers import UserInfoSerializer
from message.models import *


class MessageSerializer(serializers.ModelSerializer):
    sender = UserInfoSerializer(read_only=True)

    class Meta:
        model = Message
        fields = '__all__'


class QuestionnaireSerializer(serializers.ModelSerializer):
    # Let app load the options
    class Meta:
        exclude = ('room',)
