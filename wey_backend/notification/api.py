from .models import Notification
from .serializers import NotificationSerializer
from rest_framework.views import APIView
from rest_framework.response import Response


class NotificationList(APIView):

    def get(self, request):
        notifications = Notification.objects.filter(created_for=request.user)
        serializer = NotificationSerializer(notifications, many=True)

        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        notification = Notification.objects.filter(created_for=request.user).get(pk=request.GET.get('pk'))
        notification.is_read = True
        notification.save()

        return Response({'message': 'notification read'})