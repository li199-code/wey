from django.forms import ModelForm

from .models import Post, PostAttachment, PostReport


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ('body', 'is_private')


class AttachmentForm(ModelForm):
    class Meta:
        model = PostAttachment
        fields = ('image',)


class PostReportForm(ModelForm):
    class Meta:
        model = PostReport
        fields = ('reason',)