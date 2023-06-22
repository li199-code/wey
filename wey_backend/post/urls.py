from django.urls import path
from . import views
from . import api

urlpatterns = [
    path('', api.PostList.as_view(), name='post-list-add'),
    path('<uuid:pk>/', api.PostDetail.as_view(), name='post-detail'),
    path('<uuid:pk>/report/', api.PostReportView.as_view(), name='post-report'),
    path('comment/<uuid:pk>/', api.CommentList.as_view(), name='comment-list'),
    path('like/<uuid:pk>/', api.PostLike, name='post-like'),
    path('profile/<uuid:id>/', api.PostListProfile, name='post_list_profile'),
    path('trend/', api.TrendList.as_view(), name='TrendList'),
    # path('create/', api.PostDetail.as_view(), name='post-list'),
]