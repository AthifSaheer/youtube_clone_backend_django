from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.http import HttpResponse
from rest_framework import status
from studio.models import *
from .serializers import *
import json

# from django.shortcuts import render
# from rest_framework import status
# from django.views.decorators.csrf import csrf_exempt
# from rest_framework.authtoken.views import Token
# from rest_framework import viewsets

# @csrf_exempt
@api_view(['GET', 'POST'])
def admin__login(request):
    if request.method == 'GET':
        user = User.objects.all()
        login_serializer = AdminLogin(user, many=True)
        return Response(login_serializer.data)

    if request.method == 'POST':
        value = list(request.data.values())
        username = value[0]
        try:
            user = User.objects.get(username=username)
            if user.is_staff == True:
                return HttpResponse(json.dumps({'token':"validadmintoken"}))
            return HttpResponse(json.dumps({'nontoken':"invalidadmintoken"}))
        except:
            return HttpResponse(json.dumps({'nontoken':"invalidadmintoken"}))

@api_view(['GET'])
def users(request):
    if request.method == 'GET':
        users = User.objects.all()
        srlzr = UsersListSerializer(users, many=True)
        return Response(srlzr.data)

@api_view(['GET'])
def channels(request):
    if request.method == 'GET':
        try:
            channels = Channel.objects.all()
            srlzr = ChannelSerializer(channels, many=True)
            return Response(srlzr.data, status=status.HTTP_201_CREATED)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def popup_video(request, channel_id):
    if request.method == 'GET':
        try:
            video = UploadVideo.objects.filter(channel=channel_id)
            srlzr = VideoSerializer(video, many=True)
            return Response(srlzr.data, status=status.HTTP_201_CREATED)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def block_user(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        user.is_active = False
        user.save()
        return HttpResponse(json.dumps({'block_user':"true"}))
    except User.DoesNotExist:
        return HttpResponse(json.dumps({'block_user':"false"}))

@api_view(['GET'])
def unblock_user(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        user.is_active = True
        user.save()
        return HttpResponse(json.dumps({'block_user':"true"}))
    except User.DoesNotExist:
        return HttpResponse(json.dumps({'block_user':"false"}))

@api_view(['GET'])
def block_channel(request, channel_id):
    try:
        channel = Channel.objects.get(id=channel_id)
        channel.is_active = False
        channel.save()
        return HttpResponse(json.dumps({'block_channel':"true"}))
    except User.DoesNotExist:
        return HttpResponse(json.dumps({'block_channel':"false"}))

@api_view(['GET'])
def unblock_channel(request, channel_id):
    try:
        print("`````````````hai```````")
        channel = Channel.objects.get(id=channel_id)
        print("`````````````hai```````", channel)
        channel.is_active = True
        channel.save()
        return HttpResponse(json.dumps({'block_channel':"true"}))
    except User.DoesNotExist:
        return HttpResponse(json.dumps({'block_channel':"false"}))
