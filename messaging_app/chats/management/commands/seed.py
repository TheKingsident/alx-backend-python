from chats.models import User, Conversation, Message
from django.contrib.auth.hashers import make_password
import uuid
from django.utils import timezone

# --- Create Users ---
users = []
for i in range(1, 6):
    user, created = User.objects.get_or_create(
        username=f"user{i}",
        email=f"user{i}@example.com",
        password=make_password("password123"),
        first_name=f"First{i}",
        last_name=f"Last{i}",
        phone_number=f"555-000{i}",
    )
    users.append(user)
print(f"Created {len(users)} users.")

# --- Create Conversations ---
conversations = []
for i in range(2):
    conv = Conversation.objects.create()
    # Add 2-3 participants per conversation
    conv.participants.set(users[i:i+3])
    conversations.append(conv)
print(f"Created {len(conversations)} conversations.")

# --- Create Messages ---
messages = []
for conv in conversations:
    participants = list(conv.participants.all())
    for j in range(3):
        sender = participants[j % len(participants)]
        recipient = participants[(j + 1) % len(participants)]
        msg = Message.objects.create(
            sender_id=sender,
            recipient_id=recipient,
            conversation_id=conv,
            message_body=f"Hello from {sender.username} to {recipient.username} in conversation {conv.conversation_id}",
            sent_at=timezone.now(),
        )
        messages.append(msg)
print(f"Created {len(messages)} messages.")