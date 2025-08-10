# api/admin.py
from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import Profile, Follow, Post, Like, Comment, Notification

User = get_user_model()
admin.site.register(User)
admin.site.register(Profile)
admin.site.register(Follow)
admin.site.register(Post)
admin.site.register(Like)
admin.site.register(Comment)
admin.site.register(Notification)



# Username: root@123
# Email: rshantanu73@gmail.com
# Password: Pass@123