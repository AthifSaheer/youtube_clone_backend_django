from django.urls import path, include
from . import views
# from rest_framework.routers import DefaultRouter

# router = DefaultRouter()
# router.register('watch/video', views.watch_videos)

urlpatterns = [
    # path('', include(router.urls)),
    path('login/', views.admin__login, name='admin_login'),
    path('users/', views.users, name='users'),

    path('block/user/<int:user_id>/', views.block_user, name='block_user'),
    path('unblock/user/<int:user_id>/', views.unblock_user, name='unblock_user'),

    path('popup/video/<int:channel_id>/', views.popup_video, name='popup_video'),

    path('channels/', views.channels, name='channels'),
    path('block/channel/<int:channel_id>/', views.block_channel, name='block_channel'),
    path('unblock/channel/<int:channel_id>/', views.unblock_channel, name='unblock_channel'),
]
