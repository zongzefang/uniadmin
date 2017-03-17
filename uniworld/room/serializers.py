from rest_framework import serializers
from uniworld.settings import SERVER_ADDRESS, DEFAULT_LOGO
from room.models import *
from other.serializers import LabelInfoSerializer, TitleLabelSerializer
from user.serializers import UserInfoSerializer


class RoomCreateSerializer(serializers.ModelSerializer):

    def validate_max_participants(self, value):
        if not value:
            return value
        if value < 2:
            return 2
        return value

    class Meta:
        model = Room
        exclude = (
            'expired', 'banned', 'views', 'marked_users', 'participants', 'title_labels', 'cover', 'is_chatroom',
            'is_matchroom', 'is_advanced')


class MatchRoomCreateSerializer(RoomCreateSerializer):
    def validate_is_matchroom(self, value):
        return True

    class Meta:
        model = MatchRoom
        exclude = ('expired', 'banned', 'views', 'marked_users', 'participants', 'title_labels',
                   'cover', 'is_chatroom', 'is_advanced', 'groups', 'matched')


class RoomDetailSerializer(serializers.ModelSerializer):
    cover_thumbnail = serializers.SerializerMethodField()
    cover = serializers.SerializerMethodField()
    labels = LabelInfoSerializer(read_only=True, many=True)
    title_labels = TitleLabelSerializer(read_only=True, many=True)
    participants = UserInfoSerializer(read_only=True, many=True)
    host = UserInfoSerializer(read_only=True)
    def get_cover_thumbnail(self, room):
        if room.cover:
            return SERVER_ADDRESS + room.cover['room'].url
        else:
            return SERVER_ADDRESS + DEFAULT_LOGO
    def get_cover(self, room):
        if room.cover:
            return SERVER_ADDRESS + room.cover.url
        else:
            return SERVER_ADDRESS + DEFAULT_LOGO


    def to_representation(self, obj):
        if isinstance(obj, AdvancedRoom):
            return AdvancedRoomDetailSerializer(obj, context=self.context).to_representation(obj)
        elif isinstance(obj, MatchRoom):
            return MatchRoomDetailSerializer(obj, context=self.context).to_representation(obj)
        return super(RoomDetailSerializer, self).to_representation(obj)

    class Meta:
        model = Room
        exclude = ('polymorphic_ctype',)


class RoomInfoSerializer(serializers.ModelSerializer):
    labels = LabelInfoSerializer(read_only=True, many=True)
    title_labels = TitleLabelSerializer(read_only=True, many=True)
    cover = serializers.SerializerMethodField()
    marked_count = serializers.SerializerMethodField()
    participant_count = serializers.SerializerMethodField()

    def get_cover(self, room):
        if room.cover:
            return SERVER_ADDRESS + room.cover['room'].url
        else:
            return SERVER_ADDRESS + DEFAULT_LOGO

    def get_marked_count(self, room):
        return room.marked_users.count()

    def get_participant_count(self, room):
        return room.participants.count()

    def to_representation(self, obj):
        if isinstance(obj, AdvancedRoom):
            return AdvancedRoomInfoSerializer(obj, context=self.context).to_representation(obj)
        elif isinstance(obj, MatchRoom):
            return MatchRoomInfoSerializer(obj, context=self.context).to_representation(obj)
        return super(RoomInfoSerializer, self).to_representation(obj)

    class Meta:
        model = Room
        exclude = ('polymorphic_ctype', 'description', 'marked_users', 'participants', 'views')


class AdvancedRoomDetailSerializer(RoomDetailSerializer):
    class Meta:
        model = AdvancedRoom
        exclude = ('polymorphic_ctype',)


class MatchRoomDetailSerializer(RoomDetailSerializer):
    class Meta:
        model = MatchRoom
        exclude = ('polymorphic_ctype',)


class AdvancedRoomInfoSerializer(RoomInfoSerializer):
    class Meta:
        model = AdvancedRoom
        exclude = (
            'polymorphic_ctype', 'description', 'marked_users', 'participants', 'views')


class MatchRoomInfoSerializer(RoomInfoSerializer):
    class Meta:
        model = MatchRoom
        exclude = (
            'polymorphic_ctype', 'description', 'marked_users', 'participants', 'views')
