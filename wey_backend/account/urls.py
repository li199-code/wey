from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import api, views

urlpatterns = [
    path('login/', TokenObtainPairView.as_view(), name='token_obtain'),
    path('me/', api.me, name='me'),
    path('signup/', api.signup, name='signup'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('friend/<uuid:pk>/', api.FriendshipView.as_view(), name='friendship'),
    path('friend/request/<uuid:pk>/', api.FriendshipRequestView.as_view(), name='friendshiprequest'),
    path('editprofile/', api.editprofile, name='editprofile'),
    path('editpassword/', api.editpassword, name='editpassword'),
    path('people_you_may_know/', api.PeopleYouMayKnowList.as_view(), name='people_you_may_know'),
]