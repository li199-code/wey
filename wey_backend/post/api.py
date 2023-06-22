from .models import Post, PostAttachment, Like, Comment, Trend, PostReport
from django.db.models import Q
from .forms import PostForm, AttachmentForm
from account.models import User
from account.serializers import UserSerializer
from .serializers import PostSerializer, CommentSerializer, TrendSerializer, PostAttachmentSerializer, PostReportSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from notification.utils import create_notification

from django.http import JsonResponse


class PostList(generics.ListCreateAPIView):
    """
    url=/feed/ 显示自己和好友推文
    """

    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        user_ids = [user.id for user in request.user.friends.all()]
        user_ids.append(request.user.id)

        queryset = queryset.filter(
            created_by_id__in=user_ids
        ).exclude(
            Q(is_private=True) & ~Q(created_by=request.user)
        )

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = PostSerializer(data=request.data)
        user = request.user

        if serializer.is_valid():
            post = serializer.save(created_by=request.user)

            user.posts_count = Post.objects.filter(created_by=user).count() + 1
            user.save()

            image = request.data.get('image')
            if image != 'undefined':
                attachment = PostAttachment.objects.create(image=image, created_by=request.user)
                post.attachments.add(attachment)

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class PostReportView(APIView):
    def post(self, request, *args, **kwargs):

        postitem = Post.objects.get(pk=kwargs.get('pk'))

        serializer = PostReportSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(reporter=request.user, post=postitem)

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def PostListProfile(request, id):
    """
    url=/feed/ 显示单个用户的推文
    """
    posts = Post.objects.filter(created_by_id=id)
    user = User.objects.get(pk=id)

    if user != request.user:
        posts = posts.exclude(is_private=True)

    posts_serializer = PostSerializer(posts, many=True)
    user_serializer = UserSerializer(user)

    return JsonResponse({
        'posts': posts_serializer.data,
        'user': user_serializer.data
    }, safe=False)


@api_view(['POST'])
def PostLike(request, pk):
    post = Post.objects.get(pk=pk)
    if not post.likes.filter(created_by=request.user):
        like = Like.objects.create(created_by=request.user)
        post.likes.add(like)
        post.likes_count += 1
        post.save()

        _ = create_notification(request, type_of_notification='post_like', post_id=pk)

        return Response({
            'message': 'like created successfully'
        })

    return Response({
        'message': 'like already created'
    })


class CommentList(APIView):
    def post(self, request, *args, **kwargs):
        comment = Comment.objects.create(created_by=request.user, body=request.data.get('body'))

        post = Post.objects.get(pk=kwargs.get('pk'))
        post.comments.add(comment)
        post.comments_count += 1
        post.save()

        _ = create_notification(request, type_of_notification='post_comment', post_id=kwargs.get('pk'))

        comment_serializer = CommentSerializer(comment)

        return Response({'comment': comment_serializer.data})


class TrendList(generics.ListAPIView):
    queryset = Trend.objects.all()
    serializer_class = TrendSerializer
