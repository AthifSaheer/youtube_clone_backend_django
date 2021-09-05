from django.db.models import fields
from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.authtoken.views import Token
from .models import Channel, UploadVideo, Feedback

class ChannelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Channel
        fields = '__all__'

class UploadVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadVideo
        fields = '__all__'

class EditVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadVideo
        fields = ['title', 'description', 'category', 'visibility', 'comment_visibility']

class UserChannelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Channel
        fields = '__all__'


class UserVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadVideo
        fields = '__all__'

class FeedbackSerializer(serializers.ModelSerializer):
    channel = UserChannelSerializer()
    class Meta:
        model = Feedback
        fields = '__all__'
            

class AnalyticsVideoSerializer(serializers.ModelSerializer):
    channel = UserChannelSerializer()
    class Meta:
        model = UploadVideo
        fields = '__all__'
