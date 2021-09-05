from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from .views import UserViewSet
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('register/account', UserViewSet)
router.register('display/video', views.DisplayVideo)
# router.register('watch/video', views.watch_videos)

urlpatterns = [
    path('', include(router.urls)),
    path('login/', obtain_auth_token),

    path('watch/video/<str:videoID>/', views.watch_videos, name='watch_videos'),
    path('update/video/count/<str:videoID>/', views.update_videos_count, name='update_videos_count'),
    path('notifications/<str:channelID>/', views.notifications, name='notifications'),
    
    path('search/video/<str:keyword>/', views.search_videos, name='search_videos'),
    path('search/channel/<str:keyword>/', views.search_channel, name='search_channel'),
    path('search/filter/<str:keyword>/', views.search_filter, name='search_filter'), 

    path('channel/<int:channel_id>/', views.channel_view, name='channel_view'),
    path('channel/home/<int:channel_id>/', views.channel_home_view, name='channel_home_view'),
    path('channel/video/<int:channel_id>/', views.channel_video_view, name='channel_video_view'),

    path('subscribe/channel/', views.subscribe_channel, name='subscribe_channel'),
    path('watch/later/<str:channel_id>/', views.watch_later, name='watch_later'),

    path('feed/subscribers/video/<int:channel_id>/', views.subscribers_video, name='subscribers_video'),
    path('feed/subscribers/channel/<int:channel_id>/', views.subscribers_channel, name='subscribers_channel'),
    path('feed/explore/', views.explore_video, name='explore_video'),
    path('feed/liked/videos/<int:channel_id>/', views.liked_videos, name='liked_videos'),
    path('feed/my/comments/<int:channel_id>/', views.my_comments, name='my_comments'),

    path('like/video/', views.like_video, name='like_video'),
    path('dislike/video/', views.dislike_video, name='dislike_video'),
    
    path('add/comment/', views.add_comment, name='add_comment'),
    path('add/replay/', views.add_replay, name='add_replay'), 

    path('like/comment/', views.comment_like, name='comment_like'),
    path('dislike/comment/', views.comment_dislike, name='comment_dislike'),
]
