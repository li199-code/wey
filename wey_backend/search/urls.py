from django.urls import path
from . import api

urlpatterns = [
    path('', api.Search.as_view(), name='search'),
]