from django.contrib import admin
from .models import Channel, UploadVideo, Subscription, VideoLike, VideoDislike, Comment, ReplayComment, WatchLater, CommentLike, CommentDislike, Notification, ResolutionVideos, Feedback

admin.site.register([Channel, UploadVideo, Subscription, VideoLike, VideoDislike, Comment, ReplayComment, WatchLater, CommentLike, CommentDislike, Notification, ResolutionVideos, Feedback])