from .models import Conversation, ConversationMessage
from rest_framework import serializers
from account.serializers import UserSerializer


class ConversationSerializer(serializers.ModelSerializer):
    users = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Conversation
        fields = ('id', 'users', 'created_at', 'modified_at_formatted',)


class ConversationMessageSerializer(serializers.ModelSerializer):
    conversation = ConversationSerializer(read_only=True)
    created_by = UserSerializer(read_only=True)

    class Meta:
        model = ConversationMessage
        fields = ('id', 'conversation', 'body', 'sent_to', 'created_by', 'created_at_formatted',)
