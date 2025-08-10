# api/views.py
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth import password_validation
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.urls import reverse
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from django.db import transaction
from django.db.models import F, Q

from rest_framework import generics, permissions, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import NotFound, PermissionDenied

from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .serializers import (
    RegisterSerializer, UserSerializer, ProfileSerializer,
    PostSerializer, CommentSerializer, NotificationSerializer,
    AdminUserSerializer, AdminPostSerializer
)
from .models import Profile, Post, Follow, Like, Comment, Notification

User = get_user_model()

# --- Authentication Views ---

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Create profile for the user
        Profile.objects.get_or_create(user=user)
        
        # Send verification email (simplified version)
        # In production, you'd want to use proper email verification
        token = urlsafe_base64_encode(force_bytes(user.pk))
        verification_url = f"{settings.FRONTEND_URL}/verify-email?token={token}"
        
        try:
            send_mail(
                'Verify your email',
                f'Click here to verify your email: {verification_url}',
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=True,
            )
        except Exception:
            pass  # Email sending failed, but user is still created
        
        return Response({
            'user': RegisterSerializer(user).data,
            'message': 'User created successfully. Please check your email for verification.'
        }, status=status.HTTP_201_CREATED)


class VerifyEmailView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        token = request.data.get('token')
        if not token:
            return Response({'error': 'Token is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user_id = force_str(urlsafe_base64_decode(token))
            user = User.objects.get(pk=user_id)
            user.is_email_verified = True
            user.is_active = True
            user.save()
            return Response({'message': 'Email verified successfully'})
        except (User.DoesNotExist, ValueError):
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        email = request.data.get('email')
        if not email:
            return Response({'error': 'Email is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = User.objects.get(email=email)
            # Generate password reset token
            token = urlsafe_base64_encode(force_bytes(user.pk))
            
            # In production, you'd want to add timestamp and security checks
            reset_url = f"{settings.FRONTEND_URL}/reset-password?token={token}"
            
            try:
                send_mail(
                    'Password Reset Request',
                    f'Click here to reset your password: {reset_url}',
                    settings.DEFAULT_FROM_EMAIL,
                    [user.email],
                    fail_silently=False,
                )
                return Response({'message': 'Password reset email sent successfully'})
            except Exception:
                return Response({
                    'error': 'Failed to send email. Please try again later.'
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                
        except User.DoesNotExist:
            # Don't reveal if email exists or not for security
            return Response({'message': 'Password reset email sent successfully'})


class PasswordResetConfirmView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        token = request.data.get('token')
        new_password = request.data.get('new_password')
        
        if not token or not new_password:
            return Response({
                'error': 'Both token and new_password are required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user_id = force_str(urlsafe_base64_decode(token))
            user = User.objects.get(pk=user_id)
            
            # Validate password
            try:
                password_validation.validate_password(new_password, user)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
            
            user.set_password(new_password)
            user.save()
            
            return Response({'message': 'Password reset successfully'})
            
        except (User.DoesNotExist, ValueError):
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)


class VerifyEmailView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        token = request.data.get('token')
        if not token:
            return Response({'error': 'Token is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user_id = force_str(urlsafe_base64_decode(token))
            user = User.objects.get(pk=user_id)
            user.is_email_verified = True
            user.is_active = True
            user.save()
            return Response({'message': 'Email verified successfully'})
        except (User.DoesNotExist, ValueError):
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)


class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        # Support login with email or username
        identifier = request.data.get('username') or request.data.get('email')
        password = request.data.get('password')
        
        if not identifier or not password:
            return Response({
                'error': 'Username/email and password are required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Try to find user by username or email
        user = None
        if '@' in identifier:
            # Looks like email
            try:
                user = User.objects.get(email=identifier)
                request.data['username'] = user.username
            except User.DoesNotExist:
                pass
        else:
            # Looks like username
            try:
                user = User.objects.get(username=identifier)
            except User.DoesNotExist:
                pass
        
        if not user:
            return Response({
                'error': 'Invalid credentials'
            }, status=status.HTTP_401_UNAUTHORIZED)
        
        # Check if user is active and email verified
        if not user.is_active:
            return Response({
                'error': 'Account is not active. Please verify your email.'
            }, status=status.HTTP_401_UNAUTHORIZED)
        
        response = super().post(request, *args, **kwargs)
        
        if response.status_code == 200:
            # Update last login and add user info to response
            user.last_login = timezone.now()
            user.save(update_fields=['last_login'])
            
            response.data['user'] = UserSerializer(user).data
            
        return response


class ChangePasswordView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user = request.user
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')
        
        if not old_password or not new_password:
            return Response({
                'error': 'Both old_password and new_password are required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        if not user.check_password(old_password):
            return Response({
                'error': 'Invalid old password'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            password_validation.validate_password(new_password, user)
        except Exception as e:
            return Response({
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
        
        user.set_password(new_password)
        user.save()
        
        return Response({'message': 'Password changed successfully'})


class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get('refresh_token')
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()
            return Response({'message': 'Logged out successfully'})
        except Exception:
            return Response({'message': 'Logged out successfully'})


# --- Profile Views ---

class ProfileMeView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        profile, created = Profile.objects.get_or_create(user=self.request.user)
        return profile


class ProfileDetailView(generics.RetrieveAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'pk'

    def get_object(self):
        user_id = self.kwargs.get('pk')
        try:
            user = User.objects.get(pk=user_id)
            profile, created = Profile.objects.get_or_create(user=user)
            return profile
        except User.DoesNotExist:
            raise NotFound('User not found')


class UserListView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]
    queryset = User.objects.filter(is_active=True)

    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(
                Q(username__icontains=search) | 
                Q(first_name__icontains=search) | 
                Q(last_name__icontains=search)
            )
        return queryset


# --- Posts & Engagement ---

class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Post.objects.filter(is_active=True).select_related("author")

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx["request"] = self.request
        return ctx

    def perform_create(self, serializer):
        # handle image upload (local) then set image_url to absolute URL if present
        post = serializer.save(author=self.request.user)
        if post.image and not post.image_url:
            # build absolute url for dev (local media)
            try:
                post.image_url = self.request.build_absolute_uri(post.image.url)
                post.save(update_fields=["image_url"])
            except Exception:
                pass

    def perform_update(self, serializer):
        # Only allow users to edit their own posts
        if serializer.instance.author != self.request.user:
            raise PermissionDenied("You can only edit your own posts")
        serializer.save()

    def perform_destroy(self, instance):
        # Only allow users to delete their own posts (or admins)
        if instance.author != self.request.user and not self.request.user.is_staff:
            raise PermissionDenied("You can only delete your own posts")
        # soft-delete
        instance.is_active = False
        instance.save(update_fields=["is_active"])

    @action(detail=True, methods=["post"], permission_classes=[permissions.IsAuthenticated])
    def like(self, request, pk=None):
        post = self.get_object()
        created = False
        with transaction.atomic():
            like, created = Like.objects.get_or_create(user=request.user, post=post)
            if created:
                Post.objects.filter(pk=post.pk).update(like_count=F("like_count") + 1)
                # Notification is created automatically via signals
                return Response({"liked": True}, status=status.HTTP_201_CREATED)
            else:
                return Response({"liked": True, "detail": "already liked"}, status=status.HTTP_200_OK)

    @like.mapping.delete
    def unlike(self, request, pk=None):
        post = self.get_object()
        with transaction.atomic():
            deleted, _ = Like.objects.filter(user=request.user, post=post).delete()
            if deleted:
                Post.objects.filter(pk=post.pk).update(like_count=F("like_count") - 1)
            return Response({"liked": False})

    @action(detail=True, methods=["get"], permission_classes=[permissions.IsAuthenticatedOrReadOnly])
    def like_status(self, request, pk=None):
        post = self.get_object()
        liked = False
        if not request.user.is_anonymous:
            liked = Like.objects.filter(user=request.user, post=post).exists()
        return Response({"liked": liked})

    @action(detail=True, methods=["get","post"], permission_classes=[permissions.IsAuthenticatedOrReadOnly])
    def comments(self, request, pk=None):
        post = self.get_object()
        if request.method == "GET":
            qs = post.comments.filter(is_active=True).select_related("author").order_by("created_at")
            serializer = CommentSerializer(qs, many=True)
            return Response(serializer.data)
        # POST
        if not request.user.is_authenticated:
            raise PermissionDenied("Authentication required")
        text = request.data.get("content") or request.data.get("text")
        if not text:
            return Response({"detail":"content required"}, status=status.HTTP_400_BAD_REQUEST)
        with transaction.atomic():
            c = Comment.objects.create(content=text, author=request.user, post=post)
            Post.objects.filter(pk=post.pk).update(comment_count=F("comment_count") + 1)
            # Notification is created automatically via signals
            return Response(CommentSerializer(c).data, status=status.HTTP_201_CREATED)

class CommentDeleteView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def delete(self, request, comment_id):
        try:
            c = Comment.objects.get(pk=comment_id, is_active=True)
        except Comment.DoesNotExist:
            raise NotFound("Comment not found")
        if c.author != request.user and not request.user.is_staff:
            raise PermissionDenied("Cannot delete other user's comment")
        # soft delete
        c.is_active = False
        c.save(update_fields=["is_active"])
        Post.objects.filter(pk=c.post.pk).update(comment_count=F("comment_count") - 1)
        return Response({"detail":"Comment deleted"})

# Follow system
class FollowView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id):
        if request.user.pk == int(user_id):
            return Response({"detail":"Cannot follow yourself"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            target = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            raise NotFound("User not found")
        follow_obj, created = Follow.objects.get_or_create(follower=request.user, following=target)
        if created:
            # Notification is created automatically via signals
            return Response({"following": True}, status=status.HTTP_201_CREATED)
        return Response({"following": True, "detail": "already following"})

    def delete(self, request, user_id):
        try:
            target = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            raise NotFound("User not found")
        deleted, _ = Follow.objects.filter(follower=request.user, following=target).delete()
        return Response({"following": False, "deleted": bool(deleted)})

class FollowersListView(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = UserSerializer

    def get_queryset(self):
        uid = self.kwargs.get("user_id")
        try:
            user = User.objects.get(pk=uid)
        except User.DoesNotExist:
            raise NotFound("User not found")
        follower_ids = Follow.objects.filter(following=user).values_list("follower_id", flat=True)
        return User.objects.filter(pk__in=follower_ids)

class FollowingListView(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = UserSerializer

    def get_queryset(self):
        uid = self.kwargs.get("user_id")
        try:
            user = User.objects.get(pk=uid)
        except User.DoesNotExist:
            raise NotFound("User not found")
        following_ids = Follow.objects.filter(follower=user).values_list("following_id", flat=True)
        return User.objects.filter(pk__in=following_ids)

# Feed
from rest_framework.pagination import PageNumberPagination

class FeedPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 50

class FeedView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = FeedPagination

    def get_queryset(self):
        user = self.request.user
        following_ids = Follow.objects.filter(follower=user).values_list("following_id", flat=True)
        # Include posts from followed users AND own posts
        queryset = Post.objects.filter(
            Q(author__in=following_ids) | Q(author=user), 
            is_active=True
        ).select_related("author").prefetch_related("likes").order_by("-created_at")
        return queryset
        
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

# Notifications
class NotificationListView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(recipient=self.request.user)

class NotificationMarkReadView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, notification_id):
        try:
            n = Notification.objects.get(pk=notification_id, recipient=request.user)
        except Notification.DoesNotExist:
            raise NotFound("Notification not found")
        n.is_read = True
        n.save(update_fields=["is_read"])
        return Response({"detail":"Marked as read"})

class NotificationMarkAllReadView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request):
        Notification.objects.filter(recipient=request.user, is_read=False).update(is_read=True)
        return Response({"detail":"All marked read"})

# Admin endpoints
class AdminUsersListView(generics.ListAPIView):
    permission_classes = [permissions.IsAdminUser]
    serializer_class = AdminUserSerializer
    queryset = User.objects.all()

class AdminUserDetailView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAdminUser]
    serializer_class = AdminUserSerializer
    queryset = User.objects.all()
    lookup_field = "pk"

class AdminDeactivateUserView(APIView):
    permission_classes = [permissions.IsAdminUser]
    def post(self, request, user_id):
        try:
            u = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            raise NotFound("User not found")
        u.is_active = False
        u.save(update_fields=["is_active"])
        return Response({"detail":"User deactivated"})

class AdminPostsListView(generics.ListAPIView):
    permission_classes = [permissions.IsAdminUser]
    serializer_class = AdminPostSerializer
    queryset = Post.objects.all()

class AdminDeletePostView(APIView):
    permission_classes = [permissions.IsAdminUser]
    def delete(self, request, post_id):
        try:
            p = Post.objects.get(pk=post_id)
        except Post.DoesNotExist:
            raise NotFound("Post not found")
        # soft-delete
        p.is_active = False
        p.save(update_fields=["is_active"])
        return Response({"detail":"Post deleted"})

class AdminStatsView(APIView):
    permission_classes = [permissions.IsAdminUser]
    def get(self, request):
        total_users = User.objects.count()
        total_posts = Post.objects.count()
        # active today = users whose last_login is today
        today = timezone.now().date()
        active_today = User.objects.filter(last_login__date=today).count()
        return Response({"total_users": total_users, "total_posts": total_posts, "active_today": active_today})
