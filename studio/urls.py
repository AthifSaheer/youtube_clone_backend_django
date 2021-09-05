from django.urls import path, include
from . import views
from rest_framework import routers

# router = routers.DefaultRouter()
# router.register('create/channel', CreateChannel, basename='MyModel')

urlpatterns = [
    # path('', include(router.urls)),
    path('upload/video/', views.upload_video, name='upload_video'),
    path('delete/videos/', views.delete_videos, name='delete_videos'),
    path('edit/video/<str:video_id>/', views.edit_video, name='edit_video'),

    # path('create/channel/', views.create_channel, name='create_channel'),
    path('create/channel/', views.CreateChannel.as_view(), name='create_channel'),
    path('channels/<str:token>/', views.user_channels, name='user_channels'),
    path('videos/<str:channel_id>/', views.user_videos, name='user_videos'),

    path('send/feedback/', views.send_feedback, name='send_feedback'),

    path('analytics/<int:channel_id>/', views.analytics, name='analytics'),
]

