from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Q

from account.models import User
from post.models import Post, PostAttachment
from account.serializers import UserSerializer
from post.serializers import PostSerializer

class Search(APIView):
    def get(self, request, format=None):
        query = request.GET.get('query')

        posts = Post.objects.filter(
            body__icontains=query
        ).exclude(
            Q(is_private=True) & ~Q(created_by=request.user)
        )

        posts_serializer = PostSerializer(posts, many=True)

        users = User.objects.filter(name__icontains=query)
        users_serializer = UserSerializer(users, many=True)

        return Response({
            'users': users_serializer.data,
            'posts': posts_serializer.data
        })


