from django import forms
from studio.models import *

class SubscriptionForm(forms.ModelForm):
    class Meta:
        model = Subscription
        fields = '__all__'
        # fields = ['title', 'slug', 'category', 'brand', 'image', 'more_image_one', 'more_image_two', 'more_image_three', 'marked_price', 'selling_price', 'quantity', 'guarandeed', 'description', 'model_number', 'model_name', 'color', 'battery_backup', 'processor_brand', 'processor_name', 'storage', 'ram', 'size']

class WatchLaterForm(forms.ModelForm):
    class Meta:
        model = WatchLater
        fields = '__all__'

class VideoLikeForm(forms.ModelForm):
    class Meta:
        model = VideoLike
        fields = '__all__'


class VideoDislikeForm(forms.ModelForm):
    class Meta:
        model = VideoDislike
        fields = '__all__'

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["token", "received_channel", "received_video", "commented_channel", "comment"]

class ReplyForm(forms.ModelForm):
    class Meta:
        model = ReplayComment
        fields = '__all__'

class CommentLikeForm(forms.ModelForm):
    class Meta:
        model = CommentLike
        fields = '__all__'

class CommentDislikeForm(forms.ModelForm):
    class Meta:
        model = CommentDislike
        fields = '__all__'