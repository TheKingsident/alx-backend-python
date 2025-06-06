from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

class User(AbstractUser):
    """
    Custom user model that extends the default Django user model.
    """
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128, blank=True)
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    @property
    def id(self):
        """
        Returns the user_id as the unique identifier.
        """
        return self.user_id

class Conversation(models.Model):
    """
    Model representing a conversation between users.
    """
    conversation_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    participants = models.ManyToManyField(User, related_name='conversations')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Conversation {self.conversation_id} between {self.participants.count()} users"

class Message(models.Model):
    """
    Model representing a message in a conversation.
    """
    message_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    conversation_id = models.ForeignKey(Conversation, related_name='messages', on_delete=models.CASCADE)
    sender_id = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    recipient_id = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    message_body = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message {self.message_id} from {self.sender_id.username} to {self.recipient_id.username}"
    class Meta:
        ordering = ['sent_at']
        verbose_name = 'Message'
        verbose_name_plural = 'Messages'

