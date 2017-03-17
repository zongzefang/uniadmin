from rest_framework import serializers
from user.models import *
from uniworld.settings import SERVER_ADDRESS, DEFAULT_LOGO
from other.serializers import LabelInfoSerializer

import json


class CreateUniUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UniUser
        fields = ('username', 'email', 'password')


class UserInfoSerializer(serializers.ModelSerializer):
    avatar = serializers.SerializerMethodField()

    def get_avatar(selfself, user):
        if user.avatar:
            return SERVER_ADDRESS + user.avatar['user'].url
        else:
            return SERVER_ADDRESS + DEFAULT_LOGO

    def to_representation(self, obj):
        if isinstance(obj, Organization):
            return OrganizationInfoSerializer(obj, context=self.context).to_representation(obj)
        return super(UserInfoSerializer, self).to_representation(obj)

    class Meta:
        model = UniUser
        fields = ('name', 'id', 'avatar', 'signature')


class OrganizationInfoSerializer(UserInfoSerializer):
    class Meta:
        model = Organization
        fields = ('name', 'id', 'avatar', 'signature')


class UserDetailSerializer(serializers.ModelSerializer):
    avatar = serializers.SerializerMethodField()
    avatar_thumbnail = serializers.SerializerMethodField()
    participant_credit = serializers.SerializerMethodField()
    host_credit = serializers.SerializerMethodField()
    labels = LabelInfoSerializer(read_only=True, many=True)

    def get_avatar(self, user):
        if user.avatar:
            return SERVER_ADDRESS + user.avatar.url
        else:
            return SERVER_ADDRESS + DEFAULT_LOGO

    def get_avatar_thumbnail(self, user):
        if user.avatar:
            return SERVER_ADDRESS + user.avatar['user'].url
        else:
            return SERVER_ADDRESS + DEFAULT_LOGO

    def get_participant_credit(self, user):
        sum = user.p_thumb_ups_from.count() + user.p_thumb_downs_from.count()
        if not sum:
            return 0
        return user.thumb_ups / sum

    def get_host_credit(self, user):
        sum = user.h_thumb_ups_from.count() + user.h_thumb_downs_from.count()
        if not sum:
            return 0
        return user.thumb_ups / sum

    def to_representation(self, obj):
        if isinstance(obj, Organization):
            return OrganizationDetailSerializer(obj, context=self.context).to_representation(obj)
        return super(UserDetailSerializer, self).to_representation(obj)

    class Meta:
        model = UniUser
        exclude = (
            'p_thumb_ups_from', 'p_thumb_downs_from', 'h_thumb_ups_from', 'h_thumb_downs_from', 'password', 'username',
            'user_permissions')

class OrganizationDetailSerializer(UserDetailSerializer):
    class Meta:
        model = Organization
        exclude = (
            'p_thumb_ups_from', 'p_thumb_downs_from', 'h_thumb_ups_from', 'h_thumb_downs_from', 'password', 'username',
            'user_permissions')



class ProfileEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = UniUser
        exclude = ('id', 'university', 'username', 'password')
