from .forms import SignupForm, ProfileForm
from django.conf import settings
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from .models import User, FriendshipRequest
from .serializers import UserSerializer, FriendshipRequestSerializer
from django.core.mail import send_mail
from notification.utils import create_notification

from rest_framework.decorators import api_view, authentication_classes, permission_classes
from django.contrib.auth.forms import PasswordChangeForm


@api_view(['POST']) ## 规定请求方式
@authentication_classes([]) #因为默认的是请求都有经过身份验证，所以注册这里要设置authentication_classes为空，表示不用验证
@permission_classes([]) # 同上
def signup(request):
    data = request.data
    message = 'success'

    form = SignupForm({
        'email': data.get('email'),
        'name': data.get('name'),
        'password1': data.get('password1'),
        'password2': data.get('password2'),
    })

    if form.is_valid():
        form.save()
        return JsonResponse({'message': 'success'})
        # user = form.save()
        # user.is_active = False
        # user.save()

        # url = f'{settings.WEBSITE_URL}/activateemail/?email={user.email}&id={user.id}'

        # send_mail(
        #     "Please verify your email",
        #     f"The url for activating your account is: {url}",
        #     "noreply@wey.com",
        #     [user.email],
        #     fail_silently=False,
        # )
    else:
        message = form.errors.as_json()

    return JsonResponse({'message': message})


@api_view(['POST'])
def editprofile(request):
    user = request.user
    email = request.data.get('email')

    if User.objects.exclude(id=user.id).filter(email=email).exists():
        return JsonResponse({'message': 'email already exists'})
    else:

        form = ProfileForm(request.POST, request.FILES, instance=user)

        if form.is_valid():
            form.save()

        user_serializer = UserSerializer(user)

        return Response({
            'message': 'information updated',
            'user': user_serializer.data
        })


@api_view(['POST'])
def editpassword(request):
    user = request.user

    form = PasswordChangeForm(data=request.POST, user=user)

    if form.is_valid():
        form.save()

        return JsonResponse({'message': 'success'})
    else:
        return JsonResponse({'message': form.errors.as_json()}, safe=False)


@api_view(['GET'])
def me(request): ## 这个函数表示服务端可以根据token中的用户信息提供用户本身有关的信息
    return JsonResponse({
        'id': request.user.id,
        'name': request.user.name,
        'email': request.user.email,
        'avatar': request.user.get_avatar(),
    })


class FriendshipRequestView(APIView):
    """
    ‘profile/<uuid>/’下的好友申请相关功能
    """
    # 查出状态
    def get(self, request, *args, **kwargs):
        user = request.user
        target = User.objects.get(pk=kwargs.get('pk'))
        friends = user.friends.all()
        if target in friends:
            return Response({'isFriend': 'true'})
        instance = FriendshipRequest.objects.filter(created_for=target).filter(created_by=user).first()

        if instance:
            status = instance.status

            if status == 'sent':
                return Response({'isSent': 'true'})

        return Response({'isSent': 'false'})


    # 发送好友申请
    def post(self, request, *args, **kwargs):
        user = request.user
        target = User.objects.get(pk=kwargs.get('pk'))

        check1 = FriendshipRequest.objects.filter(created_for=user).filter(created_by=target)
        check2 = FriendshipRequest.objects.filter(created_for=target).filter(created_by=user)

        if (not check1 and not check2) or (check2 and check2.status == 'rejected'):
            Friendship = FriendshipRequest.objects.create(created_by=user, created_for=target)

            _ = create_notification(request, type_of_notification='new_friendrequest', friendrequest_id=FriendshipRequest.id)

            return Response({'message': 'request sent successfully'})
        else:
            return Response({'message': 'request already sent'})


class FriendshipView(APIView):
    """
    ‘profile/<uuid>/friends/’下的好友申请处理和好友列表
    """
    def get(self, request, *args, **kwargs):
        user = request.user
        friends = user.friends.all()
        friends_serializer = UserSerializer(friends, many=True)

        friendshiprequest = FriendshipRequest.objects.filter(created_for=user).filter(status='sent')
        friendshiprequest_serializer = FriendshipRequestSerializer(friendshiprequest, many=True)

        return Response({
            'user': UserSerializer(user).data,
            'friends': friends_serializer.data,
            'friendshiprequest': friendshiprequest_serializer.data
        })

    ## 接受或拒绝
    def post(self, request,  *args, **kwargs):
        user = request.user
        pk = request.data.get('pk')
        status = request.data.get('status')
        # print('pk', pk)
        # print('status', status)
        friendshiprequest = FriendshipRequest.objects.get(pk=pk)
        request_user = friendshiprequest.created_by

        friendshiprequest.status = status
        friendshiprequest.save()

        # print('status', status)
        if status == 'accepted':
            user.friends.add(request_user)
            user.friends_count = user.friends_count + 1
            user.save()
            request_user.friends_count = request_user.friends_count + 1
            request_user.save()

            _ = create_notification(request, type_of_notification='accepted_friendrequest',
                                    friendrequest_id=pk)
        else:
            _ = create_notification(request, type_of_notification='rejected_friendrequest',
                                    friendrequest_id=pk)

        return Response({'message': 'friendship request updated'})


class PeopleYouMayKnowList(APIView):
    def get(self, request, *args, **kwargs):
        people_you_may_know = request.user.people_you_may_know.all()
        serializer = UserSerializer(people_you_may_know, many=True)

        return Response(serializer.data)




