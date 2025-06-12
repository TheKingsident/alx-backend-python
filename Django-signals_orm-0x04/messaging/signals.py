from .models import Message
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=Message)
def create_notification(sender, instance, created, **kwargs):
    """
    Signal to create a notification when a new message is saved.
    """
    if created:
        from .models import Notification
        Notification.objects.create(
            user=instance.receiver,
            message=instance,
            is_read=False
        )
        print(f"Notification created for {instance.receiver.username} for message {instance.message_id}")
