from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.conf import settings
from .models import Profile, Follow, Like, Comment, Notification
from django.contrib.auth import get_user_model

User = get_user_model()

@receiver(post_save, sender=User)
def create_profile_for_new_user(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=Follow)
def create_follow_notification(sender, instance, created, **kwargs):
    """Create notification when user follows another user"""
    if created:
        Notification.objects.create(
            recipient=instance.following,
            sender=instance.follower,
            notification_type="follow",
            message=f"{instance.follower.username} started following you",
        )


@receiver(post_save, sender=Like)
def create_like_notification(sender, instance, created, **kwargs):
    """Create notification when user likes a post"""
    if created and instance.post.author != instance.user:
        Notification.objects.create(
            recipient=instance.post.author,
            sender=instance.user,
            notification_type="like",
            post=instance.post,
            message=f"{instance.user.username} liked your post",
        )


@receiver(post_save, sender=Comment)
def create_comment_notification(sender, instance, created, **kwargs):
    """Create notification when user comments on a post"""
    if created and instance.post.author != instance.author:
        Notification.objects.create(
            recipient=instance.post.author,
            sender=instance.author,
            notification_type="comment",
            post=instance.post,
            message=f"{instance.author.username} commented on your post",
        )
