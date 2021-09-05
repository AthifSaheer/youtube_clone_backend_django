from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User
from studio.models import UploadVideo
from rest_framework import viewsets
from rest_framework import status
from django.utils import timezone
from django.db.models import Q
from datetime import timedelta
from studio.models import *
from .serializers import *
from .forms import *

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class DisplayVideo(viewsets.ModelViewSet):
    queryset = UploadVideo.objects.filter(visibility="public")
    serializer_class = DisplayVideoSerializer


@api_view(['GET'])
def watch_videos(request, videoID):
    if request.method == 'GET':
        video = UploadVideo.objects.all().order_by('-id')
        srlzr = WatchVideoSerializer(video, context={'request': request}, many=True)
        return Response(srlzr.data, status=status.HTTP_201_CREATED)
    return Response(status=status.HTTP_400_BAD_REQUEST)    


@api_view(['GET'])
def update_videos_count(request, videoID):
    if request.method == 'GET':
        get_one_video = UploadVideo.objects.get(id=videoID)
        get_one_video.view_count += 1
        get_one_video.save()
        srlzr = WatchVideoSerializer(get_one_video, context={'request': request}, many=False)
        return Response(srlzr.data, status=status.HTTP_201_CREATED)
    return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
def notifications(request, channelID):
    if request.method == 'GET':
        try:
            notf = Notification.objects.filter(subscriber=channelID).order_by('-id')
            count = notf.count()
            if count < 1:
                pass
            else:
                srlzr = NotificationSerializer(notf, context={'request': request}, many=True)
                return Response(srlzr.data, status=status.HTTP_201_CREATED)
        except Notification.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)    
    
    if request.method == 'POST':
        notfs = Notification.objects.filter(subscriber=channelID)
        for notf in notfs:
            notf.is_seen = False
            notf.save()
        data = {"completed":"completed"}
        return Response(data, status=status.HTTP_201_CREATED)
        
    return Response(status=status.HTTP_400_BAD_REQUEST)    

@api_view(['GET'])
def search_videos(request, keyword):
    if request.method == 'GET':
        video = UploadVideo.objects.filter(Q(title__icontains=keyword), channel__is_active=True)
        count = video.count()
        if count < 1:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            srlzr = WatchVideoSerializer(video, many=True)
            return Response(srlzr.data, status=status.HTTP_201_CREATED)
    return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def search_channel(request, keyword):
    if request.method == 'GET':
        channel = Channel.objects.filter(Q(channel_name__icontains=keyword), is_active=True)
        count = channel.count()
        if count < 1:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        else:
            for ch in channel:
                videos = UploadVideo.objects.filter(channel=ch)
                video_count_ = videos.count()

                srlzr = ChannelSrzl(channel, context={'video_count_': video_count_}, many=True)
                return Response(srlzr.data, status=status.HTTP_201_CREATED)
    print("......003")
    return Response(status=status.HTTP_400_BAD_REQUEST)
    


@api_view(['GET', 'POST'])
def subscribe_channel(request):
    if request.method == 'GET':
        pass

    elif request.method == 'POST':
        token = request.data['token']
        method = request.data['method']
        user_channel = int(request.data['user_channel'])
        which_channels = int(request.data['which_channels'])

        if method == 'get':
            try:
                sub = Subscription.objects.get(user_channel=user_channel, which_channels=which_channels)
                if sub:
                    if sub.subscribe == False:
                        data = {"unsubscribed": "unsubscribed"}
                        return Response(data, status=status.HTTP_201_CREATED)
                    
                    elif sub.subscribe == True:
                        data = {"subscribed": "subscribed"}
                        return Response(data, status=status.HTTP_201_CREATED)
                else:
                    data = {"unsubscribed": "unsubscribed"}
                    return Response(data, status=status.HTTP_201_CREATED)
            except Subscription.DoesNotExist:
                data = {"unsubscribed": "unsubscribed"}
                return Response(data, status=status.HTTP_201_CREATED)

        if method == "post":
            if Subscription.objects.filter(user_channel=user_channel, which_channels=which_channels).exists():

                sub = Subscription.objects.get(user_channel=user_channel, which_channels=which_channels)
                channel = Channel.objects.get(id=which_channels)
                print("--reached------001---")

                if sub.subscribe == False:
                    print("--reached------002---")
                    sub.subscribe = True
                    sub.save()
                    
                    channel.subscribers += 1
                    channel.save()
                    data = {"subscribed": "subscribed"}
                    return Response(data, status=status.HTTP_201_CREATED)

                elif sub.subscribe == True:
                    print("--reached------003---")
                    sub.subscribe = False
                    sub.save()

                    channel.subscribers -= 1
                    channel.save()
                    data = {"unsubscribed": "unsubscribed"}
                    return Response(data, status=status.HTTP_201_CREATED)
            else:
                if user_channel == which_channels:
                    print("--reached------004---")
                    data = {"your_own_channel": "You can't subscribe for your own channel.'"}
                    return Response(data, status=status.HTTP_200_OK)

                print("--reached------005---")
                form_data = {"token": token, "user_channel": user_channel, "which_channels": which_channels, "subscribe":True}
                print("--reached------006---")
                
                try:
                    print("--reached------007---")
                    channel = Channel.objects.get(id=which_channels)
                    form = SubscriptionForm(form_data)
                    if form.is_valid():
                        form.save()
                        channel.subscribers += 1
                        channel.save()
                        data = {"created_subscribed": "created_subscribed"}
                        print("--reached------008---")
                        return Response(data, status=status.HTTP_201_CREATED)
                except Channel.DoesNotExist:
                    print("----- Channel does not exists------")
                    data = {"channel_does_not_exists": "Channel not selected or exists...!"}
                    return Response(data, status=status.HTTP_201_CREATED)
                

        return Response(status=status.HTTP_200_OK)
    return Response(status=status.HTTP_200_OK)
 
    
@api_view(['GET', 'POST'])
def watch_later(request, channel_id):
    if request.method == 'GET':
        try:
            wtlr = WatchLater.objects.filter(applied_channel=channel_id, watch_later=True)
            
            count = wtlr.count()
            if count < 1:
                data = {"no_watch_later_videos": "no_watch_later_videos"}
                return Response(data, status=status.HTTP_201_CREATED)
            
            srlzr = WatchLaterSerializer(wtlr, context={'request': request}, many=True)
            return Response(srlzr.data, status=status.HTTP_201_CREATED)

        except WatchLater.DoesNotExist:
            data = {"no_watch_later_videos": "no_watch_later_videos"}
            return Response(data, status=status.HTTP_201_CREATED)

    elif request.method == 'POST':
        token = request.data['token']
        method = request.data['method']
        applied_channel = int(request.data['applied_channel'])
        watch_later_video = int(request.data['watch_later_video'])

        if method == 'get':
            try:
                wtlr = WatchLater.objects.get(applied_channel=applied_channel, watch_later_video=watch_later_video)
                if wtlr:
                    if wtlr.watch_later == False:
                        data = {"watch_later_disapplied": "watch_later_disapplied"}
                        return Response(data, status=status.HTTP_201_CREATED)
                    
                    elif wtlr.watch_later == True:
                        data = {"watch_later_applied": "watch_later_applied"}
                        return Response(data, status=status.HTTP_201_CREATED)
                else:
                    data = {"watch_later_disapplied": "watch_later_disapplied"}
                    return Response(data, status=status.HTTP_201_CREATED)
                    
            except WatchLater.DoesNotExist:
                data = {"watch_later_disapplied": "watch_later_disapplied"}
                return Response(data, status=status.HTTP_201_CREATED)

        if method == "post":
            if WatchLater.objects.filter(applied_channel=applied_channel, watch_later_video=watch_later_video).exists():

                wtch_ltr = WatchLater.objects.get(applied_channel=applied_channel, watch_later_video=watch_later_video)
                print("--watch_later------001---")

                if wtch_ltr.watch_later == False:
                    print("--watch_later------002---")
                    wtch_ltr.watch_later = True
                    wtch_ltr.save()
                    
                    data = {"watch_later_applied": "watch_later_applied"}
                    return Response(data, status=status.HTTP_201_CREATED)

                elif wtch_ltr.watch_later == True:
                    print("--watch_later------003---")
                    wtch_ltr.watch_later = False
                    wtch_ltr.save()

                    data = {"watch_later_disapplied": "watch_later_disapplied"}
                    return Response(data, status=status.HTTP_201_CREATED)
            else:
                print("--watch_later------005---")
                form_data = {"token": token, "applied_channel": applied_channel, "watch_later_video": watch_later_video, "watch_later":True}
                print("--watch_later------006---")
                
                print("--watch_later------007---")
                form = WatchLaterForm(form_data)
                if form.is_valid():
                    form.save()
                    data = {"created_watch_later_applied": "created_watch_later_applied"}
                    print("--watch_later------008---")
                    return Response(data, status=status.HTTP_201_CREATED)
                    
    return Response(status=status.HTTP_201_CREATED)


@api_view(['GET'])
def channel_view(request, channel_id):
    if request.method == 'GET':
        try:
            channel = Channel.objects.get(id=channel_id)
            videos = UploadVideo.objects.filter(channel=channel)
            video_count_ = videos.count()

            video_view_count_ = 0
            for vid in videos:
                video_view_count_ += vid.view_count
            context = {'request': request, 'video_count_': video_count_, "video_view_count_": video_view_count_}
            serializer = ChannelSrzl(channel, context=context, many=False)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Channel.DoesNotExist:
            # data = {"channel_does_not_exists": "Channel does not exists...!"}
            return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def channel_video_view(request, channel_id):
    if request.method == 'GET':

        try:
            print("--reached------001--")
            try:
                print("--reached------002--")
                videos = UploadVideo.objects.filter(channel=channel_id)
                count = videos.count()
                print("count-----", count)
                serializer = DisplayVideoSerializer(videos, context={'request': request}, many=True)
                
                if count == 0:
                    print("--reached------0023--")
                    data = {"videos_not_found": "Videos not found...!"}
                    return Response(data, status=status.HTTP_201_CREATED)

            except UploadVideo.AttributeError:
                print("--reached------003--")
                videos = UploadVideo.objects.get(channel=channel_id)
                serializer = DisplayVideoSerializer(videos, context={'request': request}, many=False)
            
                
            print("--reached------004--")
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except UploadVideo.DoesNotExist:
            print("--reached------005--")
            data = {"videos_not_found": "Videos not found...!"}
            return Response(data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
def channel_home_view(request, channel_id):
    if request.method == 'GET':

        try:
            print("--reached------001--")
            try:
                print("--reached------002--")
                videos = UploadVideo.objects.filter(channel=channel_id).order_by('-view_count')[:4]
                count = videos.count()
                print("count-----", count)
                serializer = DisplayVideoSerializer(videos, context={'request': request}, many=True)
                
                if count == 0:
                    print("--reached------0023--")
                    data = {"videos_not_found": "Videos not found...!"}
                    return Response(data, status=status.HTTP_201_CREATED)

            except UploadVideo.AttributeError:
                print("--reached------003--")
                videos = UploadVideo.objects.get(channel=channel_id)
                serializer = DisplayVideoSerializer(videos, context={'request': request}, many=False)
            
                
            print("--reached------004--")
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except UploadVideo.DoesNotExist:
            print("--reached------005--")
            data = {"videos_not_found": "Videos not found...!"}
            return Response(data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'POST'])
def like_video(request):
    if request.method == 'GET':
        print("--get===reached------001----")
        pass
    if request.method == 'POST':
        print("--get===reached------002----")
        token = request.data['token']
        method = request.data['method']
        liked_channel = int(request.data['liked_channel'])
        liked_video = int(request.data['liked_video'])

        if method == 'get':
            try:
                vd_like = VideoLike.objects.get(liked_channel=liked_channel, liked_video=liked_video)
                if vd_like:
                    if vd_like.like == False:
                        data = {"disliked": "disliked"}
                        return Response(data, status=status.HTTP_201_CREATED)
                    
                    elif vd_like.like == True:
                        data = {"liked": "liked"}
                        return Response(data, status=status.HTTP_201_CREATED)
                else:
                    data = {"disliked": "disliked"}
                    return Response(data, status=status.HTTP_201_CREATED)
            except VideoLike.DoesNotExist:
                data = {"disliked": "disliked"}
                return Response(data, status=status.HTTP_201_CREATED)

        if method == "post":
            if VideoLike.objects.filter(liked_channel=liked_channel, liked_video=liked_video).exists():

                liked_vd = VideoLike.objects.get(liked_channel=liked_channel, liked_video=liked_video)
                video = UploadVideo.objects.get(id=liked_video)

                if liked_vd.like == False:
                    liked_vd.like = True
                    liked_vd.save()
                    
                    video.like += 1
                    video.save()

                    if VideoDislike.objects.filter(disliked_channel=liked_channel, disliked_video=liked_video):
                        disliked_vd = VideoDislike.objects.get(disliked_channel=liked_channel, disliked_video=liked_video)
                        if disliked_vd.dislike == True:
                            disliked_vd.dislike = False
                            disliked_vd.save()
                            video.dislike -= 1
                            video.save()

                            data = {"liked": "liked", "disliked_false":"disliked_false"}
                            return Response(data, status=status.HTTP_201_CREATED)
                        
                    data = {"liked": "liked"}
                    return Response(data, status=status.HTTP_201_CREATED)

                elif liked_vd.like == True:
                    liked_vd.like = False
                    liked_vd.save()
                    
                    video.like -= 1
                    video.save()

                    data = {"disliked": "disliked"}
                    return Response(data, status=status.HTTP_201_CREATED)
            else:
                form_data = {"token": token, "liked_channel": liked_channel, "liked_video": liked_video, "like":True}
                try:
                    video = UploadVideo.objects.get(id=liked_video)
                    form = VideoLikeForm(form_data)
                    if form.is_valid():
                        form.save()

                        video.like += 1
                        video.save()

                        if VideoDislike.objects.filter(disliked_channel=liked_channel, disliked_video=liked_video):
                            disliked_vd = VideoDislike.objects.get(disliked_channel=liked_channel, disliked_video=liked_video)
                            if disliked_vd.dislike == True:
                                disliked_vd.dislike = False
                                disliked_vd.save()
                                video.dislike -= 1
                                video.save()

                                data = {"liked": "liked", "disliked_false":"disliked_false"}
                                return Response(data, status=status.HTTP_201_CREATED)

                        data = {"created_liked": "created_liked"}
                        return Response(data, status=status.HTTP_201_CREATED)
                except Channel.DoesNotExist:
                    data = {"invalid_request": "Invalid request...!"}
                    return Response(data, status=status.HTTP_201_CREATED)
                
        return Response(status=status.HTTP_200_OK)
    return Response(status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
def dislike_video(request):
    if request.method == 'GET':
        print("--get reached dislike------001----")
    if request.method == 'POST':
        token = request.data['token']
        method = request.data['method']
        disliked_channel = int(request.data['liked_channel'])
        disliked_video = int(request.data['liked_video'])

        if method == 'get':
            try:
                print(".........dislike 001.........")
                vid_dislike = VideoDislike.objects.get(disliked_channel=disliked_channel, disliked_video=disliked_video)
                if vid_dislike:
                    if vid_dislike.dislike == False:
                        print(".........dislike 002.........")
                        data = {"disliked_false": "disliked_false"}
                        return Response(data, status=status.HTTP_201_CREATED)
                    
                    elif vid_dislike.dislike == True:
                        print(".........dislike 003.........")
                        data = {"disliked_true": "disliked_true"}
                        return Response(data, status=status.HTTP_201_CREATED)
                else:
                    print(".........dislike 004.........")
                    data = {"disliked_false": "disliked_false"}
                    return Response(data, status=status.HTTP_201_CREATED)
            except VideoDislike.DoesNotExist:
                print(".........dislike 005.........")
                data = {"disliked_false": "disliked_false"}
                return Response(data, status=status.HTTP_201_CREATED)

        if method == "post":
            if VideoDislike.objects.filter(disliked_channel=disliked_channel, disliked_video=disliked_video).exists():

                vid_disliked = VideoDislike.objects.get(disliked_channel=disliked_channel, disliked_video=disliked_video)
                video = UploadVideo.objects.get(id=disliked_video)
                if vid_disliked.dislike == False:
                    vid_disliked.dislike = True
                    vid_disliked.save()
                    
                    video.dislike += 1
                    video.save()

                    if VideoLike.objects.filter(liked_channel=disliked_channel, liked_video=disliked_video).exists():
                        vid_liked = VideoLike.objects.get(liked_channel=disliked_channel, liked_video=disliked_video)
                        if vid_liked.like == True:
                            vid_liked.like = False
                            vid_liked.save()
                            video.like -= 1
                            video.save()

                            data = {"disliked_true": "disliked_true", "disliked":"disliked"}
                            return Response(data, status=status.HTTP_201_CREATED)

                    data = {"disliked_true": "disliked_true"}
                    return Response(data, status=status.HTTP_201_CREATED)

                elif vid_disliked.dislike == True:
                    vid_disliked.dislike = False
                    vid_disliked.save()
                    
                    video.dislike -= 1
                    video.save()
                    
                    data = {"disliked_false": "disliked_false"}
                    return Response(data, status=status.HTTP_201_CREATED)
            else:
                form_data = {"token": token, "disliked_channel": disliked_channel, "disliked_video": disliked_video, "dislike":True}
                
                try:
                    video = UploadVideo.objects.get(id=disliked_video)
                    form = VideoDislikeForm(form_data)
                    if form.is_valid():
                        form.save()

                        video.dislike += 1
                        video.save()

                        if VideoLike.objects.filter(liked_channel=disliked_channel, liked_video=disliked_video).exists():
                            vid_liked = VideoLike.objects.get(liked_channel=disliked_channel, liked_video=disliked_video)
                            if vid_liked.like == True:
                                vid_liked.like = False
                                vid_liked.save()
                                video.like -= 1
                                video.save()

                                data = {"disliked_true": "disliked_true", "disliked":"disliked"}
                                return Response(data, status=status.HTTP_201_CREATED)
                        else:
                            data = {"created_disliked_true": "created_disliked_true"}
                            return Response(data, status=status.HTTP_201_CREATED)

                except Channel.DoesNotExist:
                    print("----- Channel does not exists in dislike view------")
                    data = {"invalid_request": "Invalid request...!"}
                    return Response(data, status=status.HTTP_201_CREATED)
                
        return Response(status=status.HTTP_200_OK)
    return Response(status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
def add_comment(request):
    if request.method == 'POST':
        method = request.data['method']

        if method == 'get':
            received_video = int(request.data['received_video'])

            try:
                comment = Comment.objects.filter(received_video=received_video)
                count = comment.count()
                if count < 1:
                    data = [{"no_comments": "Comments not found !"}]
                    print("~~~~~~~~~~~~~~`", data)
                    return Response(data, status=status.HTTP_201_CREATED)
                else:
                    srz = CommentSerializer(comment, many=True)
                    print("~~~~~~~~~~~09~~~`")
                    return Response(srz.data, status=status.HTTP_201_CREATED)

            except Comment.DoesNotExist:
                data = [{"no_comments": "Comments not found !"}]
                print("~~~~~~~~~~~~~~`", data)
                return Response(data, status=status.HTTP_201_CREATED)

        if method == "post":
            token = request.data['token']
            received_channel = int(request.data['received_channel'])
            received_video = int(request.data['received_video'])
            commented_channel = int(request.data['commented_channel'])
            comment = request.data['comment']
            
            comment_data = {"token": token, "received_channel": received_channel, "received_video": received_video, "commented_channel": commented_channel, "comment": comment}

            form = CommentForm(comment_data)
            if form.is_valid():
                form.save()
                data = {"comment_success": "comment_success"}
                return Response(data, status=status.HTTP_201_CREATED)

    data = {"error_occurred": "error_occurred"}
    return Response(data, status=status.HTTP_201_CREATED)



@api_view(['GET', 'POST'])
def add_replay(request):
    if request.method == 'POST':
        method = request.data['method']

        if method == 'get':
            print(request.data['reply_received_video'])
            reply_received_video = int(request.data['reply_received_video'])
            received_parent_comment = int(request.data['received_parent_comment'])

            try:
                reply = ReplayComment.objects.filter(reply_received_video=reply_received_video, received_parent_comment=received_parent_comment)
                count = reply.count()
                if count < 1:
                    data = [{"no_comments": "no_comments"}]
                    print("REPLY++++ ~~~~~~~~~~~~~~`", data)
                    return Response(data, status=status.HTTP_201_CREATED)
                else:
                    srz = ReplayCommentSerializer(reply, many=True)
                    print("REPLY++++ ~~~~~~~~~~~09~~~`")
                    return Response(srz.data, status=status.HTTP_201_CREATED)

            except ReplayComment.DoesNotExist:
                data = [{"no_comments": "no_comments"}]
                print("REPLY++++ ~~~~~~~~~~~~~~`", data)
                return Response(data, status=status.HTTP_201_CREATED)

        if method == "post":
            token = request.data['token']
            reply_received_channel = int(request.data['reply_received_channel'])
            reply_received_video = int(request.data['reply_received_video'])

            received_parent_comment = int(request.data['received_parent_comment'])
            replied_channel = int(request.data['replied_channel'])
            reply = request.data['reply']
            
            reply_data = {"token": token, "reply_received_channel": reply_received_channel, "reply_received_video": reply_received_video, "received_parent_comment": received_parent_comment, "replied_channel": replied_channel, "reply": reply}
            print("REPLY++++ ", reply_data)

            form = ReplyForm(reply_data)
            if form.is_valid():
                form.save()
                data = {"comment_success": "comment_success"}
                print("REPLY++++ --comment_success---------")
                return Response(data, status=status.HTTP_201_CREATED)
            print("REPLY++++ --reached error ---")

    data = {"error_occurred": "error_occurred"}
    return Response(data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
def search_filter(request, keyword):
    if request.method == 'GET':
        time_now = timezone.now()
        one_hour_later = time_now + timedelta(hours=-1)
        this_week = time_now + timedelta(days=-7)
    
        if keyword == 'last_hour':
            videos = UploadVideo.objects.filter(upload_date__gte=one_hour_later, upload_date__lte=time_now, channel__is_active=True)
        elif keyword == 'this_week':
            videos = UploadVideo.objects.filter(upload_date__gte=this_week, upload_date__lte=time_now, channel__is_active=True)
        elif keyword == 'view_count':
            videos = UploadVideo.objects.filter(channel__is_active=True).order_by('-view_count')
        elif keyword == 'upload_date':
            videos = UploadVideo.objects.filter(channel__is_active=True).order_by('-upload_date')

        count = videos.count()
        if count < 1:
            data = {'no_videos': 'no_videos'}
            return Response(data, status=status.HTTP_201_CREATED)
        else:
            srlzr = DisplayVideoSerializer(videos, context={'request': request}, many=True)
            return Response(srlzr.data, status=status.HTTP_201_CREATED)

@api_view(['GET'])
def subscribers_video(request, channel_id):
    if request.method == 'GET':
        try:
            subed_channels = Subscription.objects.filter(user_channel=channel_id, subscribe=True)
        
            listx = []
            for channel in subed_channels:
                videos = UploadVideo.objects.filter(channel=channel.which_channels)
                srlzr = DisplayVideoSerializer(videos, context={'request': request}, many=True)
                print(".....................", srlzr.data[0])
                listx.append(srlzr.data[0])

            count = subed_channels.count()
            if count < 1:
                data = [{"no_videos":"no_videos"}]
                return Response(data, status=status.HTTP_201_CREATED)

            return Response(listx, status=status.HTTP_201_CREATED)

        except:
            data = [{"no_videos":"no_videos"}]
            return Response(data, status=status.HTTP_201_CREATED)
    

@api_view(['GET'])
def subscribers_channel(request, channel_id):
    if request.method == 'GET':
        try:
            subed_channels = Subscription.objects.filter(user_channel=channel_id, subscribe=True)
        
            # listx = []
            # for channel in subed_channels:
            #     videos = UploadVideo.objects.filter(channel=channel.which_channels)
            #     print(".....................", srlzr.data[0])
            #     listx.append(srlzr.data[0])

            count = subed_channels.count()
            if count < 1:
                data = [{"no_channels":"no_channels"}]
                return Response(data, status=status.HTTP_201_CREATED)

            srlzr = SubscriptionSerializer(subed_channels, context={'request': request}, many=True)
            return Response(srlzr.data, status=status.HTTP_201_CREATED)

        except:
            data = [{"no_channels":"no_channels"}]
            return Response(data, status=status.HTTP_201_CREATED)

@api_view(['GET'])
def explore_video(request):
    if request.method == 'GET':
        try:
            videos = UploadVideo.objects.all().order_by('-view_count')

            count = videos.count()
            if count < 1:
                data = [{"no_videos":"no_videos"}]
                return Response(data, status=status.HTTP_201_CREATED)

            srlzr = WatchVideoSerializer(videos, context={'request': request}, many=True)
            return Response(srlzr.data, status=status.HTTP_201_CREATED)

        except:
            data = [{"no_videos":"no_videos"}]
            return Response(data, status=status.HTTP_201_CREATED)
    return Response(status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET'])
def liked_videos(request, channel_id):
    if request.method == 'GET':
        try:
            video_likes = VideoLike.objects.filter(liked_channel=channel_id, like=True)
            srlzr = VideoLikeSerializer(video_likes, context={'request': request}, many=True)
        

            count = video_likes.count()
            print("----count liked video--", count)

            if count < 1:
                data = [{"no_videos":"no_videos"}]
                return Response(data, status=status.HTTP_201_CREATED)

            return Response(srlzr.data, status=status.HTTP_201_CREATED)

        except:
            data = [{"no_videos":"no_videos"}]
            return Response(data, status=status.HTTP_201_CREATED)
    

@api_view(['GET'])
def my_comments(request, channel_id):
    if request.method == 'GET':
        try:
            comments = Comment.objects.filter(commented_channel=channel_id)

            count = comments.count()
            if count < 1:
                data = [{"no_comments":"no_comments"}]
                return Response(data, status=status.HTTP_201_CREATED)

            srlzr = CommentsSerializer(comments, context={'request': request}, many=True)
            return Response(srlzr.data, status=status.HTTP_201_CREATED)

        except:
            data = [{"no_comments":"no_comments"}]
            return Response(data, status=status.HTTP_201_CREATED)
    return Response(status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['GET', 'POST'])
def comment_like(request):
    if request.method == 'GET':
        pass
    if request.method == 'POST':
        print("--get===reached------002----")
        token = request.data['token']
        method = request.data['method']
        comment_liked_channel = int(request.data['comment_liked_channel'])
        which_comment_like = int(request.data['which_comment_like'])

        print("comntLiketoken--", token)
        print("comntLikemethod--", method)
        print("comntLikecomment_liked_channel--", comment_liked_channel)
        print("comntLikewhich_comment_like--", which_comment_like)

        if method == 'get':
            print("comntLike--get===reached------002----")
            try:
                comnt_like = CommentLike.objects.get(comment_liked_channel=comment_liked_channel, which_comment_like=which_comment_like)
                print("comntLike--vdlike==,", comnt_like)

                if comnt_like:

                    if comnt_like.like == False:
                        data = {"comment_disliked": "comment_disliked"}
                        return Response(data, status=status.HTTP_201_CREATED)
                    
                    elif comnt_like.like == True:
                        data = {"comment_liked": "comment_liked"}
                        return Response(data, status=status.HTTP_201_CREATED)
                       
                else:
                    data = {"comment_disliked": "comment_disliked"}
                    return Response(data, status=status.HTTP_201_CREATED)
                   
            except CommentLike.DoesNotExist:
                data = {"comment_disliked": "comment_disliked"}
                return Response(data, status=status.HTTP_201_CREATED)

        if method == "post":
            if CommentLike.objects.filter(comment_liked_channel=comment_liked_channel, which_comment_like=which_comment_like).exists():

                comnt_like = CommentLike.objects.get(comment_liked_channel=comment_liked_channel, which_comment_like=which_comment_like)
                comment = Comment.objects.get(id=which_comment_like)
                print("comntLike--reached------001---")

                if comnt_like.like == False:
                    print("comntLike--reached------002---")
                    comnt_like.like = True
                    comnt_like.save()
                    
                    comment.like += 1
                    comment.save()

                    if CommentDislike.objects.filter(comment_disliked_channel=comment_liked_channel, which_comment_dislike=which_comment_like):
                        comnt_dislike = CommentDislike.objects.get(comment_disliked_channel=comment_liked_channel, which_comment_dislike=which_comment_like)
                        if comnt_dislike.dislike == True:
                            comnt_dislike.dislike = False
                            comnt_dislike.save()
                            comment.dislike -= 1
                            comment.save()

                            data = {"comment_liked": "comment_liked", "disliked_false":"disliked_false"}
                            return Response(data, status=status.HTTP_201_CREATED)
                        
                    data = {"comment_liked": "comment_liked"}
                    return Response(data, status=status.HTTP_201_CREATED)

                elif comnt_like.like == True:
                    print("comntLike--reached------0012---")
                    comnt_like.like = False
                    comnt_like.save()
                    
                    comment.like -= 1
                    comment.save()

                    data = {"comment_disliked": "comment_disliked"}
                    return Response(data, status=status.HTTP_201_CREATED)
            else:
                form_data = {"token": token, "comment_liked_channel": comment_liked_channel, "which_comment_like": which_comment_like, "like":True}
                try:
                    print("comntLike--reached------007---")
                    comment = Comment.objects.get(id=which_comment_like)
                    form = CommentLikeForm(form_data)
                    if form.is_valid():
                        form.save()

                        comment.like += 1
                        comment.save()

                        if CommentDislike.objects.filter(comment_disliked_channel=comment_liked_channel, which_comment_dislike=which_comment_like):
                            comnt_dislike = CommentDislike.objects.get(comment_disliked_channel=comment_liked_channel, which_comment_dislike=which_comment_like)
                            if comnt_dislike.dislike == True:
                                comnt_dislike.dislike = False
                                comnt_dislike.save()
                                comment.dislike -= 1
                                comment.save()

                                data = {"comment_liked": "comment_liked", "disliked_false":"disliked_false"}
                                return Response(data, status=status.HTTP_201_CREATED)

                    data = {"comment_created_liked": "comment_created_liked"}
                    return Response(data, status=status.HTTP_201_CREATED)
                except Channel.DoesNotExist:
                    print("comntLike----- Channel does not exists------")
                    data = {"invalid_request": "Invalid request...!"}
                    return Response(data, status=status.HTTP_201_CREATED)
                
        return Response(status=status.HTTP_200_OK)
    return Response(status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
def comment_dislike(request):
    if request.method == 'GET':
        pass

    if request.method == 'POST':
        token = request.data['token']
        method = request.data['method']
        comment_disliked_channel = int(request.data['comment_disliked_channel'])
        which_comment_dislike = int(request.data['which_comment_dislike'])

        if method == 'get':
            try:
                cmnt_dislike = CommentDislike.objects.get(comment_disliked_channel=comment_disliked_channel, which_comment_dislike=which_comment_dislike)
                
                if cmnt_dislike:
                    
                    if cmnt_dislike.dislike == False:
                        data = {"disliked_false": "disliked_false"}
                        return Response(data, status=status.HTTP_201_CREATED)
                    
                    elif cmnt_dislike.dislike == True:
                        data = {"disliked_true": "disliked_true"}
                        return Response(data, status=status.HTTP_201_CREATED)
                        
                else:
                    data = {"disliked_false": "disliked_false"}
                    return Response(data, status=status.HTTP_201_CREATED)
                    
            except CommentDislike.DoesNotExist:
                data = {"disliked_false": "disliked_false"}
                return Response(data, status=status.HTTP_201_CREATED)

        if method == "post":
            if CommentDislike.objects.filter(comment_disliked_channel=comment_disliked_channel, which_comment_dislike=which_comment_dislike).exists():

                comnt_disliked = CommentDislike.objects.get(comment_disliked_channel=comment_disliked_channel, which_comment_dislike=which_comment_dislike)
                comment = Comment.objects.get(id=which_comment_dislike)
                if comnt_disliked.dislike == False:
                    comnt_disliked.dislike = True
                    comnt_disliked.save()
                    
                    comment.dislike += 1
                    comment.save()

                    if CommentLike.objects.filter(comment_liked_channel=comment_disliked_channel, which_comment_like=which_comment_dislike).exists():
                        cmnt_liked = CommentLike.objects.get(comment_liked_channel=comment_disliked_channel, which_comment_like=which_comment_dislike)
                        if cmnt_liked.like == True:
                            cmnt_liked.like = False
                            cmnt_liked.save()

                            comment.like -= 1
                            comment.save()

                            data = {"disliked_true": "disliked_true", "disliked":"disliked"}
                            return Response(data, status=status.HTTP_201_CREATED)

                    data = {"disliked_true": "disliked_true"}
                    return Response(data, status=status.HTTP_201_CREATED)

                elif comnt_disliked.dislike == True:
                    comnt_disliked.dislike = False
                    comnt_disliked.save()
                    
                    comment.dislike -= 1
                    comment.save()
                    
                    data = {"disliked_false": "disliked_false"}
                    return Response(data, status=status.HTTP_201_CREATED)
            else:
                form_data = {"token": token, "comment_disliked_channel": comment_disliked_channel, "which_comment_dislike": which_comment_dislike, "dislike": True}
                
                try:
                    comment = Comment.objects.get(id=which_comment_dislike)
                    form = CommentDislikeForm(form_data)
                    if form.is_valid():
                        form.save()

                        comment.dislike += 1
                        comment.save()

                        if CommentLike.objects.filter(comment_liked_channel=comment_disliked_channel, which_comment_like=which_comment_dislike).exists():
                            cmnt_liked = CommentLike.objects.get(comment_liked_channel=comment_disliked_channel, which_comment_like=which_comment_dislike)
                            if cmnt_liked.like == True:
                                cmnt_liked.like = False
                                cmnt_liked.save()

                                comment.like -= 1
                                comment.save()

                                data = {"disliked_true": "disliked_true", "disliked":"disliked"}
                                return Response(data, status=status.HTTP_201_CREATED)
                        data = {"created_disliked_true": "created_disliked_true"}
                        return Response(data, status=status.HTTP_201_CREATED)
                except Comment.DoesNotExist:
                    data = {"invalid_request": "Invalid request...!"}
                    return Response(data, status=status.HTTP_201_CREATED)
                
        return Response(status=status.HTTP_200_OK)
    return Response(status=status.HTTP_200_OK)

