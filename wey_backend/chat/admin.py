from django.contrib import admin
from .models import ConversationMessage, Conversation

# Register your models here.
admin.site.register(ConversationMessage)
admin.site.register(Conversation)