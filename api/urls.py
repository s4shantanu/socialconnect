# api/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from api.views import (
    RegisterView, VerifyEmailView, CustomTokenObtainPairView, PasswordResetView, PasswordResetConfirmView,
    ChangePasswordView, LogoutView, ProfileMeView, ProfileDetailView, UserListView,
    PostViewSet, CommentDeleteView, FollowView, FollowersListView, FollowingListView,
    FeedView, NotificationListView, NotificationMarkReadView, NotificationMarkAllReadView,
    AdminUsersListView, AdminUserDetailView, AdminDeactivateUserView,
    AdminPostsListView, AdminDeletePostView, AdminStatsView
)

router = DefaultRouter()
router.register(r"posts", PostViewSet, basename="posts")

urlpatterns = [
    # auth (milestone1)
    path("auth/register/", RegisterView.as_view(), name="register"),
    path("auth/verify-email/", VerifyEmailView.as_view(), name="verify-email"),
    path("auth/login/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("auth/change-password/", ChangePasswordView.as_view(), name="change-password"),
    path("auth/password-reset/", PasswordResetView.as_view(), name="password-reset"),
    path("auth/password-reset-confirm/", PasswordResetConfirmView.as_view(), name="password-reset-confirm"),
    path("auth/logout/", LogoutView.as_view(), name="logout"),

    # profiles
    path("users/me/", ProfileMeView.as_view(), name="profile-me"),
    path("users/<int:pk>/", ProfileDetailView.as_view(), name="profile-by-id"),
    path("users/", UserListView.as_view(), name="user-list"),

    # follow
    path("users/<int:user_id>/follow/", FollowView.as_view(), name="follow-toggle"),
    path("users/<int:user_id>/followers/", FollowersListView.as_view(), name="user-followers"),
    path("users/<int:user_id>/following/", FollowingListView.as_view(), name="user-following"),

    # feed
    path("feed/", FeedView.as_view(), name="feed"),

    # notifications
    path("notifications/", NotificationListView.as_view(), name="notifications"),
    path("notifications/<int:notification_id>/read/", NotificationMarkReadView.as_view(), name="notif-read"),
    path("notifications/mark-all-read/", NotificationMarkAllReadView.as_view(), name="notif-mark-all"),

    # admin
    path("admin/users/", AdminUsersListView.as_view(), name="admin-users"),
    path("admin/users/<int:pk>/", AdminUserDetailView.as_view(), name="admin-user-detail"),
    path("admin/users/<int:user_id>/deactivate/", AdminDeactivateUserView.as_view(), name="admin-user-deactivate"),
    path("admin/posts/", AdminPostsListView.as_view(), name="admin-posts"),
    path("admin/posts/<int:post_id>/", AdminDeletePostView.as_view(), name="admin-post-delete"),
    path("admin/stats/", AdminStatsView.as_view(), name="admin-stats"),

    # comments delete
    path("comments/<int:comment_id>/", CommentDeleteView.as_view(), name="comment-delete"),

    # posts (router)
    path("", include(router.urls)),
]
