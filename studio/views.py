from rest_framework.parsers import MultiPartParser, FormParser
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import *
from .serializers import *

import base64
from django.core.files.base import ContentFile

class CreateChannel(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def get(self, request, *args, **kwargs):
        posts = Channel.objects.all()
        serializer = ChannelSerializer(posts, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        # CONVERTING CROPPED IMAGE BASE64 TO IMAGE
        format, img = request.data['logo'].split(';base64,')
        ext = format.split('/')[-1]
        image = ContentFile(base64.b64decode(img), name = request.data['channel_name'] + '1.' + ext)
        request.data['logo'] = image

        channel_serializer = ChannelSerializer(data=request.data)

        if channel_serializer.is_valid():
            channel_serializer.save()
            return Response(channel_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(channel_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# from studio.video_converter import get_resolution, convert_video_resolution
@csrf_exempt
@api_view(['POST'])
def upload_video(request):
    if request.method == 'POST':
        # video_serializer = 0
        # time_count = 0
        # while True:
        #     if video_serializer == 0:
        #         time_count += 1
        #     else:
        #         break

        video = request.data['video']
        print("video path-------------", video)
        


        video_serializer = UploadVideoSerializer(data=request.data)
        
        '''
        DEF videoUploadTime:
            upload_time = 90
            return upload_time
        '''
        # videoUploadTime()

        if video_serializer.is_valid():
            video_serializer.save()

        video = UploadVideo.objects.filter(token=request.data['token']).order_by('-id').first()
        
        channel = request.data['channel']
        subscribers = Subscription.objects.filter(which_channels=channel)
        count = subscribers.count()

        # 🍔 VIDEO RESOLUTION DETECT AND CONVERT ---------
        # vsr = UploadVideoSerializer(video)
        # video_path = vsr.data['video']
        # resolution = get_resolution(video_path)

        # if resolution >= 1080:
        #     convert_video_resolution(video_path, 720, "%s_720p" %video_path.split('.')[0], video.id, video.token)
        #     convert_video_resolution(video_path, 480, "%s_480p" %video_path.split('.')[0], video.id, video.token)
        #     convert_video_resolution(video_path, 360, "%s_360p" %video_path.split('.')[0], video.id, video.token)
        #     convert_video_resolution(video_path, 240, "%s_240p" %video_path.split('.')[0], video.id, video.token)
        #     convert_video_resolution(video_path, 144, "%s_144p" %video_path.split('.')[0], video.id, video.token)
        # elif resolution == 720:
        #     convert_video_resolution(video_path, 480, "%s_480p" %video_path.split('.')[0], video.id, video.token)
        #     convert_video_resolution(video_path, 360, "%s_360p" %video_path.split('.')[0], video.id, video.token)
        #     convert_video_resolution(video_path, 240, "%s_240p" %video_path.split('.')[0], video.id, video.token)
        #     convert_video_resolution(video_path, 144, "%s_144p" %video_path.split('.')[0], video.id, video.token)
        # elif resolution == 480:
        #     convert_video_resolution(video_path, 360, "%s_360p" %video_path.split('.')[0], video.id, video.token)
        #     convert_video_resolution(video_path, 240, "%s_240p" %video_path.split('.')[0], video.id, video.token)
        #     convert_video_resolution(video_path, 144, "%s_144p" %video_path.split('.')[0], video.id, video.token)
        # elif resolution == 360:
        #     convert_video_resolution(video_path, 240, "%s_240p" %video_path.split('.')[0], video.id, video.token)
        #     convert_video_resolution(video_path, 144, "%s_144p" %video_path.split('.')[0], video.id, video.token)
        # elif resolution == 240:
        #     convert_video_resolution(video_path, 144, "%s_144p" %video_path.split('.')[0], video.id, video.token)

            
        if count < 1:
            return Response(video_serializer.data, status=status.HTTP_201_CREATED)
        else:
            for subsc in subscribers:
                notf = Notification()
                notf.subscriber = subsc.user_channel
                notf.video  = video
                notf.save()

            return Response(video_serializer.data, status=status.HTTP_201_CREATED)
        return Response(video_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def user_channels(request, token):
    if request.method == 'GET':
        try:
            channel = Channel.objects.filter(token=token)
            serializer = UserChannelSerializer(channel, many=True)
            return Response(serializer.data)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def user_videos(request, channel_id):
    if request.method == 'GET':
        try:
            videos = UploadVideo.objects.filter(channel=channel_id).order_by('-id')
            serializer = UserVideoSerializer(videos, context={"request": request}, many=True)
            return Response(serializer.data)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def delete_videos(request):
    if request.method == 'POST':
        user_token = request.data['user_token']
        channel_id = request.data['channel_id']
        video = request.data['video']

        try:
            video = UploadVideo.objects.get(id=video, token=user_token, channel=channel_id)
            video.delete()
        except UploadVideo.DoesNotExist:
            data = {"video_deleted_error": "video_deleted_error"}
            return Response(data, status=status.HTTP_201_CREATED)

        data = {"video_deleted": "video_deleted"}
        return Response(data, status=status.HTTP_201_CREATED)



@csrf_exempt
@api_view(['POST', 'GET'])
def edit_video(request, video_id):
    if request.method == 'GET':
        video = UploadVideo.objects.filter(id=video_id)
        video_serializer = UploadVideoSerializer(video, context={'request': request}, many=True)
        return Response(video_serializer.data)

    if request.method == 'POST':
        video = UploadVideo.objects.get(id=video_id)
        channel = Channel.objects.get(id=request.data['channel'])

        video.channel = channel
        video.title = request.data['title']
        video.description = request.data['description']
        video.category = request.data['category']
        video.visibility = request.data['visibility']
        video.comment_visibility = request.data['comment_visibility']
        video.save()

        data = {"edited":"edited"}
        return Response(data, status=status.HTTP_201_CREATED)
    return Response(status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view(['POST', 'GET'])
def send_feedback(request):
    if request.method == 'GET':
        feedback = Feedback.objects.all().order_by('-id')
        feedback_serializer = FeedbackSerializer(feedback, context={'request': request}, many=True)
        return Response(feedback_serializer.data, status=status.HTTP_201_CREATED)

    if request.method == 'POST':
        try:
            channel = Channel.objects.get(id=request.data['channel'])
            Feedback.objects.create(
                channel=channel, subject=request.data['subject'], message=request.data['message']
                )
            data = {"success":"success"}
            print("Success---------------------")
            return Response(data, status=status.HTTP_201_CREATED)
        except:
            data = {"error":"error"}
            return Response(data, status=status.HTTP_201_CREATED)

    return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST', 'GET'])
def analytics(request, channel_id):
    if request.method == 'GET':
        channel = Channel.objects.get(id=channel_id)
        videos = UploadVideo.objects.filter(channel=channel).order_by('-id')
        analytics_srzl = AnalyticsVideoSerializer(videos, context={'request': request}, many=True)
        return Response(analytics_srzl.data ,status=status.HTTP_201_CREATED)