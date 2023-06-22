from django.urls import path
from . import views
from . import api

urlpatterns = [
    path('', api.ConversationListCreateView.as_view(), name='ConversationListCreateView'),
    path('<uuid:pk>/', api.ConversationDetailView.as_view(), name='ConversationDetailView'),
]