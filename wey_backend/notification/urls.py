from django.urls import path
from .api import NotificationList

urlpatterns = [
    path('', NotificationList.as_view(), name='NotificationList'),
]