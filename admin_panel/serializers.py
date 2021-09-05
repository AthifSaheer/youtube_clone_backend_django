from studio.models import *
from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.authtoken.views import Token

class TokenS(serializers.ModelSerializer):
    class Meta:
        model = Token
        fields = '__all__'
    
class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadVideo
        fields = '__all__'

class AdminLogin(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']

class UsersListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class ChannelSerializer(serializers.ModelSerializer):
    token = TokenS()
    user = UsersListSerializer()
    # token.user = UsersListSerializer()
    class Meta:
        model = Channel
        fields = '__all__'
        # fields = ['id', 'token', 'channel_name', 'logo', 'banner', 'about', 'created_at']
        # depth = 1


