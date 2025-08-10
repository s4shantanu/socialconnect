# api/serializers.py
from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.contrib.auth import password_validation
from .models import Profile, Post, Like, Comment, Notification, Follow

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "email", "first_name", "last_name", "is_email_verified", "is_staff")

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    class Meta:
        model = User
        fields = ("username", "email", "password", "first_name", "last_name")
    def create(self, validated):
        pwd = validated.pop("password")
        user = User(**validated)
        user.set_password(pwd)
        user.is_active = False
        user.save()
        return user

class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    followers_count = serializers.IntegerField(source="followers_count", read_only=True)
    following_count = serializers.IntegerField(source="following_count", read_only=True)
    posts_count = serializers.IntegerField(source="posts_count", read_only=True)
    avatar_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Profile
        fields = (
            "user", "bio", "avatar", "avatar_url", "website", "location", 
            "visibility", "followers_count", "following_count", "posts_count"
        )
        
    def get_avatar_url(self, obj):
        if obj.avatar:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.avatar.url)
        return None
        
    def validate_bio(self, value):
        if len(value) > 160:
            raise serializers.ValidationError("Bio cannot exceed 160 characters.")
        return value

class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    liked_by_user = serializers.SerializerMethodField()
    
    class Meta:
        model = Post
        fields = (
            "id", "content", "author", "created_at", "updated_at", "image", 
            "image_url", "category", "is_active", "like_count", "comment_count", 
            "liked_by_user"
        )
        read_only_fields = (
            "like_count", "comment_count", "created_at", "updated_at", 
            "author", "is_active", "liked_by_user"
        )

    def get_liked_by_user(self, obj):
        user = self.context.get("request").user
        if user.is_anonymous:
            return False
        return obj.likes.filter(user=user).exists()
        
    def validate_content(self, value):
        if len(value) > 280:
            raise serializers.ValidationError("Content cannot exceed 280 characters.")
        return value
    
    def validate_image(self, value):
        if value:
            # Validate file size (2MB = 2 * 1024 * 1024 bytes)
            if value.size > 2 * 1024 * 1024:
                raise serializers.ValidationError("Image file size cannot exceed 2MB.")
            
            # Validate file type
            allowed_types = ['image/jpeg', 'image/png', 'image/jpg']
            if value.content_type not in allowed_types:
                raise serializers.ValidationError("Only JPEG and PNG image formats are allowed.")
                
        return value

class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    class Meta:
        model = Comment
        fields = ("id","content","author","post","created_at","is_active")
        read_only_fields = ("author","created_at","is_active")

class NotificationSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    class Meta:
        model = Notification
        fields = ("id","recipient","sender","notification_type","post","message","is_read","created_at")

# Admin serializers
class AdminUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id","username","email","is_active","is_staff","is_email_verified","last_login","date_joined")

class AdminPostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    class Meta:
        model = Post
        fields = ("id","content","author","created_at","is_active","like_count","comment_count")
