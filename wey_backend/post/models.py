import uuid

from django.db import models
from django.utils.timesince import timesince
from django.conf import settings

from account.models import User


class Like(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_by = models.ForeignKey(User, related_name='likes', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_by = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    body = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ('created_at',)

    def created_at_formatted(self):
        return timesince(self.created_at)

    def __str__(self):
        return self.body


class PostAttachment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    image = models.ImageField(upload_to='post_attachments')
    created_by = models.ForeignKey(User, related_name='post_attachments', on_delete=models.CASCADE)

    def get_image(self):
        if self.image:
            return settings.WEBSITE_URL + self.image.url
        else:
            return ''


class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    body = models.TextField(blank=False, null=False)

    attachments = models.ManyToManyField(PostAttachment, related_name='post', blank=True)

    likes = models.ManyToManyField(Like, blank=True)
    likes_count = models.IntegerField(default=0)

    is_private = models.BooleanField(default=False)

    comments = models.ManyToManyField(Comment, blank=True)
    comments_count = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return self.body

    def created_at_formatted(self):
        return timesince(self.created_at)


class PostReport(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    post = models.ForeignKey(Post, related_name='reports', on_delete=models.CASCADE)
    reporter = models.ForeignKey(User, related_name='reported_posts', on_delete=models.CASCADE)
    reason = models.CharField(max_length=255, blank=False, null=False, default='')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.reason


class Trend(models.Model):
    hashtag = models.CharField(max_length=255)
    occurences = models.IntegerField()
