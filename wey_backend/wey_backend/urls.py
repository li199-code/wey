from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from account.views import activateemail

urlpatterns = [
    path('api/', include('account.urls')),
    path('api/post/', include('post.urls')),
    path('api/search/', include('search.urls')),
    path('api/chat/', include('chat.urls')),
    path('grappelli/', include('grappelli.urls')), # grappelli URLS
    path('admin/', admin.site.urls),
    path('activateemail/', activateemail, name='activateemail'),
    path('api/notification/', include('notification.urls'), name='notification'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
