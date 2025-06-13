from django.db import models

class UnreadMessagesManager(models.Manager):
    def unread_for_user(self, user):
        # Only fetch unread messages where the user is the receiver
        return self.get_queryset().filter(receiver=user, read=False).only('message_id', 'sender', 'content', 'timestamp')