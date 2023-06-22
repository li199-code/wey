from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics, status

from .models import ConversationMessage, Conversation
from .serializers import ConversationSerializer, ConversationMessageSerializer
from account.models import User


class ConversationListCreateView(APIView):
    def get(self, request, *args, **kwargs):
        conversations = Conversation.objects.filter(users__in=list([request.user]))
        conversations_serializer = ConversationSerializer(conversations, many=True)

        return Response({'conversations': conversations_serializer.data})

    def post(self, request, *args, **kwargs):
        user = User.objects.get(pk=request.data.get('send_to'))

        conversations = Conversation.objects.filter(users__in=list([request.user])).filter(users__in=list([user]))

        if conversations.exists():
            conversation = conversations.first()
        else:
            conversation = Conversation.objects.create()
            conversation.users.add(user, request.user)
            conversation.save()

        serializer = ConversationSerializer(conversation)

        return Response({'conversation': serializer.data})



class ConversationDetailView(APIView):
    def get(self, request, *args, **kwargs):
        messages = ConversationMessage.objects.filter(conversation_id=kwargs.get('pk'))
        messages_serializer = ConversationMessageSerializer(messages, many=True)

        return Response({'messages': messages_serializer.data})

    def post(self, request, *args, **kwargs):
        body = request.data.get('body')
        created_by = request.user
        conversation = Conversation.objects.get(pk=kwargs.get('pk'))
        for user in conversation.users.all():
            if user != request.user:
                sent_to = user
        message = ConversationMessage.objects.create(conversation=conversation, body=body, sent_to=sent_to, created_by=created_by)
        message_serializer = ConversationMessageSerializer(message, read_only=True)
        return Response({'message': message_serializer.data})

