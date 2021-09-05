from django.db import models
from django.contrib.auth.models import User
from taggit.managers import TaggableManager
from django.utils.text import slugify 
from rest_framework.authtoken.views import Token

def chnl_logo_upload_path(instance, filename):
    return '/'.join(['logo', str(instance.channel_name), filename])

def chnl_banner_upload_path(instance, filename):
    return '/'.join(['logo', str(instance.channel_name), filename])


class Channel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    token = models.ForeignKey(Token, on_delete=models.CASCADE)
    channel_name = models.CharField(max_length=100)
    # slug = models.SlugField(unique=True)
    logo = models.ImageField(upload_to=chnl_logo_upload_path, blank=True, null=True)
    banner = models.ImageField(upload_to=chnl_banner_upload_path, blank=True, null=True)
    about = models.CharField(max_length=150)
    subscribers = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    # def save(self, *args, **kwargs):
    #     self.slug = slugify(self.channel_name)
    #     super(Channel, self).save(*args, **kwargs)

    def save(self, *args, **kwargs):
        token = Token.objects.get(key=self.token)
        user = User.objects.get(username=token.user)
        self.user = user
        super().save(*args, **kwargs)

    def __str__(self):
        return "ID:" + str(self.id) + " | Channel name: " + str(self.channel_name)

video_visibility = [
    ('public','public'),
    ('unlisted','unlisted'),
    ('private','private'),
]

comment_visibility = [
    ('public','public'),
    ('prevent','prevent'),
]

category = [
    ('Tech','Tech'),
    ('News','News'),
    ('Kids','Kids'),
    ('Eloctronics','Eloctronics'),
    ('Python','Python'),
    ('Driving','Driving'),
    ('Mahindra thar','Mahindra thar'),
    ('MKBHD','MKBHD'),
    ('Apple','Apple'),
    ('Titan','Titan'),
    ('Bill gates','Bill gates'),
    ('America','America'),
    ('India','India'),
    ('Music','Music'),
    ('TED','TED'),
]

class UploadVideo(models.Model):
    token = models.ForeignKey(Token, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE)
    video = models.FileField(upload_to="videos")
    title = models.CharField(max_length=200)
    # slug = models.SlugField(unique=True)
    description = models.TextField()
    thumbnail = models.ImageField(upload_to='thumbnail')
    visibility = models.CharField(max_length=20, choices=video_visibility)
    category = models.CharField(max_length=20, choices=category)
    # tag = TaggableManager()
    like = models.IntegerField(default=0)
    dislike = models.IntegerField(default=0)
    comment_visibility = models.CharField(max_length=20, choices=comment_visibility)
    view_count = models.IntegerField(default=0) 
    upload_date = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        token = Token.objects.get(key=self.token)
        user = User.objects.get(username=token.user)
        self.user = user
        super().save(*args, **kwargs)

    def __str__(self):
        return "ID:" + str(self.id) + " | Title: " + str(self.title)

class ResolutionVideos(models.Model):
    token = models.ForeignKey(Token, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    og_video = models.ForeignKey(UploadVideo, on_delete=models.CASCADE, related_name="og_video")
    
    video_720p = models.FileField(upload_to="video_720p", blank=True, null=True)
    video_480p = models.FileField(upload_to="video_480p", blank=True, null=True)
    video_360p = models.FileField(upload_to="video_360p", blank=True, null=True)
    video_240p = models.FileField(upload_to="video_240p", blank=True, null=True)
    video_144p = models.FileField(upload_to="video_144p", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        token = Token.objects.get(key=self.token)
        user = User.objects.get(username=token.user)
        self.user = user
        super().save(*args, **kwargs)

    def __str__(self):
        return "ID:" + str(self.id) + " | User: " + str(self.user)

class Subscription(models.Model):
    token = models.ForeignKey(Token, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    user_channel = models.ForeignKey(Channel, on_delete=models.CASCADE, related_name="user_channel")
    which_channels = models.ForeignKey(Channel, on_delete=models.CASCADE, related_name="which_channels")
    subscribe = models.BooleanField(default=False)
    # notification = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        token = Token.objects.get(key=self.token)
        user = User.objects.get(username=token.user)
        self.user = user
        super().save(*args, **kwargs)

    def __str__(self):
        return "ID:" + str(self.id) + " | User: " + str(self.user)


class VideoLike(models.Model):
    token = models.ForeignKey(Token, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    liked_channel = models.ForeignKey(Channel, on_delete=models.CASCADE, related_name="liked_channel")
    liked_video = models.ForeignKey(UploadVideo, on_delete=models.CASCADE, related_name="liked_video")
    like = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        token = Token.objects.get(key=self.token)
        user = User.objects.get(username=token.user)
        self.user = user
        super().save(*args, **kwargs)

    def __str__(self):
        return "ID:" + str(self.id) + " | User: " + str(self.user)

class VideoDislike(models.Model):
    token = models.ForeignKey(Token, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    disliked_channel = models.ForeignKey(Channel, on_delete=models.CASCADE, related_name="disliked_channel")
    disliked_video = models.ForeignKey(UploadVideo, on_delete=models.CASCADE, related_name="disliked_video")
    dislike = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        token = Token.objects.get(key=self.token)
        user = User.objects.get(username=token.user)
        self.user = user
        super().save(*args, **kwargs)

    def __str__(self):
        return "ID:" + str(self.id) + " | User: " + str(self.user)

class Comment(models.Model):
    token = models.ForeignKey(Token, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    received_channel = models.ForeignKey(Channel, on_delete=models.CASCADE, related_name="received_channel")
    received_video = models.ForeignKey(UploadVideo, on_delete=models.CASCADE, related_name="received_video")
    commented_channel = models.ForeignKey(Channel, on_delete=models.CASCADE, related_name="commented_channel")
    comment = models.TextField(blank=True)
    like = models.IntegerField(default=0)
    dislike = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        token = Token.objects.get(key=self.token)
        user = User.objects.get(username=token.user)
        self.user = user
        super().save(*args, **kwargs)

    def __str__(self):
        return "ID:" + str(self.id) + " | User: " + str(self.user)

class ReplayComment(models.Model):
    token = models.ForeignKey(Token, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    reply_received_channel = models.ForeignKey(Channel, on_delete=models.CASCADE, related_name="reply_received_channel")
    reply_received_video = models.ForeignKey(UploadVideo, on_delete=models.CASCADE, related_name="reply_received_video")
    received_parent_comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name="received_parent_comment")
    replied_channel = models.ForeignKey(Channel, on_delete=models.CASCADE, related_name="replied_channel")
    reply = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        token = Token.objects.get(key=self.token)
        user = User.objects.get(username=token.user)
        self.user = user
        super().save(*args, **kwargs)

    def __str__(self):
        return "ID:" + str(self.id) + " | User: " + str(self.user)


class WatchLater(models.Model):
    token = models.ForeignKey(Token, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    applied_channel = models.ForeignKey(Channel, on_delete=models.CASCADE, related_name="applied_channel")
    watch_later_video = models.ForeignKey(UploadVideo, on_delete=models.CASCADE, related_name="watch_later_video")
    watch_later = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        token = Token.objects.get(key=self.token)
        user = User.objects.get(username=token.user)
        self.user = user
        super().save(*args, **kwargs)

    def __str__(self):
        return "ID:" + str(self.id) + " | User: " + str(self.user)

class CommentLike(models.Model):
    token = models.ForeignKey(Token, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    comment_liked_channel = models.ForeignKey(Channel, on_delete=models.CASCADE, related_name="comment_liked_channel")
    which_comment_like = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name="which_comment_like")
    like = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        token = Token.objects.get(key=self.token)
        user = User.objects.get(username=token.user)
        self.user = user
        super().save(*args, **kwargs)

    def __str__(self):
        return "ID:" + str(self.id) + " | User: " + str(self.user)
    

class CommentDislike(models.Model):
    token = models.ForeignKey(Token, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    comment_disliked_channel = models.ForeignKey(Channel, on_delete=models.CASCADE, related_name="comment_disliked_channel")
    which_comment_dislike = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name="which_comment_dislike")
    dislike = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        token = Token.objects.get(key=self.token)
        user = User.objects.get(username=token.user)
        self.user = user
        super().save(*args, **kwargs)

    def __str__(self):
        return "ID:" + str(self.id) + " | User: " + str(self.user)


class Notification(models.Model):
    # token = models.ForeignKey(Token, on_delete=models.CASCADE)
    # user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    video = models.ForeignKey(UploadVideo, on_delete=models.CASCADE, related_name="notif_video")
    subscriber = models.ForeignKey(Channel, on_delete=models.CASCADE, related_name="subscriber_channel")
    is_seen = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "ID:" + str(self.id) + " | Seen: " + str(self.is_seen)

class Feedback(models.Model):
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE, related_name="channel")
    subject = models.CharField(max_length=100)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "ID:" + str(self.id) + " | Channel: " + str(self.channel)

