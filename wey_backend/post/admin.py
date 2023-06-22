from django.contrib import admin
from .models import Post, PostAttachment, Comment, Trend, PostReport


admin.site.register(Post)
admin.site.register(PostAttachment)
admin.site.register(Comment)
admin.site.register(Trend)
admin.site.register(PostReport)
