from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.authtoken.views import Token
from studio.models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password']

        extra_kwargs = {'password':{
            'write_only':True,
            'required':True
        }}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        print("user",user)
        Token.objects.create(user=user)
        return user
    
class UserSrzl(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password']

class ChannelSrzl(serializers.ModelSerializer):
    video_count = serializers.SerializerMethodField()
    video_view_count = serializers.SerializerMethodField()

    def get_video_count(self, obj):
        if "video_count_" in self.context:
            return self.context["video_count_"]
        return None
    def get_video_view_count(self, obj):
        if "video_view_count_" in self.context:
            return self.context["video_view_count_"]
        return None

    class Meta:
        model = Channel
        fields = ['id', 'user', 'about', 'created_at', 'channel_name', 'token', 'logo', 'subscribers', 'banner', 'is_active', 'video_count', 'video_view_count']

class DisplayVideoSerializer(serializers.ModelSerializer):
    user = UserSrzl()
    channel = ChannelSrzl()
    upload_date = serializers.DateTimeField(read_only=True, format="%Y-%m-%d %H:%M:%S")
    class Meta:
        model = UploadVideo
        fields = ('id', 'user', 'channel', 'video', 'title', 'description', 'thumbnail', 'visibility', 'category', 'comment_visibility', 'view_count', 'upload_date')


class WatchVideoSerializer(serializers.ModelSerializer):
    channel = ChannelSrzl()
    upload_date = serializers.DateTimeField(read_only=True, format="%Y-%m-%d %H:%M:%S")
    class Meta:
        model = UploadVideo
        fields = '__all__'

class NotificationSerializer(serializers.ModelSerializer):
    video = DisplayVideoSerializer()

    class Meta:
        model = Notification
        fields = '__all__'

class SubscribersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = '__all__'

class CommentSerializer(serializers.ModelSerializer):
    commented_channel = ChannelSrzl()
    created_at = serializers.DateTimeField(read_only=True, format="%Y-%m-%d %H:%M:%S")
    class Meta:
        model = Comment
        fields = '__all__'

class ReplayCommentSerializer(serializers.ModelSerializer):
    replied_channel = ChannelSrzl()
    class Meta:
        model = ReplayComment
        fields = '__all__'
    
class WatchLaterSerializer(serializers.ModelSerializer):
    applied_channel = ChannelSrzl()
    watch_later_video = DisplayVideoSerializer()
    class Meta:
        model = WatchLater
        fields = '__all__'


class VideoLikeSerializer(serializers.ModelSerializer):
    liked_channel = ChannelSrzl()
    liked_video = DisplayVideoSerializer()
    class Meta:
        model = VideoLike
        fields = '__all__'

class CommentsSerializer(serializers.ModelSerializer):
    commented_channel = ChannelSrzl()
    received_video = DisplayVideoSerializer()
    class Meta:
        model = Comment
        fields = '__all__'


class SubscriptionSerializer(serializers.ModelSerializer):
    which_channels = ChannelSrzl()
    class Meta:
        model = Subscription
        fields = '__all__'
