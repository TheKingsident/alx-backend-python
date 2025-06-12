from .models import Message, Notification, MessageHistory
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

@receiver(post_save, sender=Message)
def create_notification(sender, instance, created, **kwargs):
    """
    Signal to create a notification when a new message is saved.
    """
    if created:
        Notification.objects.create(
            user=instance.receiver,
            message=instance,
            is_read=False
        )
        print(f"Notification created for {instance.receiver.username} for message {instance.message_id}")

@receiver(pre_save, sender=Message)
def update_message_history(sender, instance, **kwargs):
    """
    Signal to create a message history entry before a message is updated.
    """
    if instance.pk:
        try:
            original_message = Message.objects.get(pk=instance.pk)
            if original_message.content != instance.content:
                MessageHistory.objects.create(
                    message = original_message,
                    previous_content = {
                        'content': original_message.content,
                        'edited': original_message.edited
                    },
                    action = 'updated',
                    timestamp = original_message.timestamp
                )
                instance.edited = True
        except Message.DoesNotExist:
            pass