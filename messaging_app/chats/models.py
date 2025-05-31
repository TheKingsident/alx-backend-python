from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    """
    Custom user model that extends the default Django user model.
    """
    pass

class Conversation(models.Model):
    """
    Model representing a conversation between users.
    """
    participants = models.ManyToManyField(User, related_name='conversations')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Conversation {self.id} between {self.participants.count()} users"
    
class Message(models.Model):
    """
    Model representing a message in a conversation.
    """
    conversation = models.ForeignKey(Conversation, related_name='messages', on_delete=models.CASCADE)
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message {self.id} from {self.sender.username} in Conversation {self.conversation.id}"
    class Meta:
        ordering = ['timestamp']
        verbose_name = 'Message'
        verbose_name_plural = 'Messages'

