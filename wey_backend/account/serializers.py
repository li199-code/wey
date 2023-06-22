from rest_framework import serializers
from . import models


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ('id', 'name', 'email', 'friends_count', 'posts_count','get_avatar',)


class FriendshipRequestSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)

    class Meta:
        model = models.FriendshipRequest
        fields = ('id', 'created_by',)
