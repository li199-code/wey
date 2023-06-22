from rest_framework import serializers
from . import models
from account.serializers import UserSerializer


class CommentSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)

    class Meta:
        model = models.Comment
        fields = ('id', 'body', 'created_by', 'created_at_formatted', )


class PostAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PostAttachment
        fields = ('id', 'get_image',)


class PostSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    comments = CommentSerializer(read_only=True, many=True)
    attachments = PostAttachmentSerializer(read_only=True, many=True)

    class Meta:
        model = models.Post
        fields = ('id', 'body', 'created_by', 'is_private', 'created_at_formatted', 'likes_count', 'comments', 'comments_count', 'attachments',)


class TrendSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Trend
        fields = ('hashtag', 'occurences',)


class PostReportSerializer(serializers.ModelSerializer):
    post = PostSerializer(read_only=True)
    reporter = UserSerializer(read_only=True)

    class Meta:
        model = models.PostReport
        fields = ('id', 'post', 'reporter', 'reason', 'created_at',)
