from rest_framework import serializers
from django.db import models
from .models import User, Conversation, Message, Notification

class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source='get_full_name', read_only=True)

    class Meta:
        model = User
        fields = [
            'user_id', 'email', 'first_name', 'last_name', 'full_name',
            'phone_number'
        ]
        read_only_fields = ['user_id']

class MinimalUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['user_id', 'first_name']

class MessageSerializer(serializers.ModelSerializer):
    sender = MinimalUserSerializer(read_only=True)
    receiver = MinimalUserSerializer(read_only=True)

    receiver_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), write_only=True
    )
    conversation_id = serializers.PrimaryKeyRelatedField(
        queryset=Conversation.objects.all(), write_only=True,
        allow_null=True, required=False
    )

    class Meta:
        model = Message
        fields = [
            'message_id', 'sender', 'receiver', 'receiver_id', 'conversation_id',
            'content', 'timestamp',
        ]
        read_only_fields = ['message_id', 'timestamp']

    def validate_content(self, value):
        if not value.strip():
            raise serializers.ValidationError("Message content cannot be empty.")
        return value

    def create(self, validated_data):
        receiver = validated_data.pop('receiver_id')
        conversation = validated_data.pop('conversation_id', None)
        sender = self.context['request'].user

        if conversation is None:
            conversations = Conversation.objects.filter(participants=sender).filter(participants=receiver)
            conversations = conversations.annotate(num_participants=models.Count('participants')).filter(num_participants=2)
            if conversations.exists():
                conversation = conversations.first()
            else:
                conversation = Conversation.objects.create()
                conversation.participants.set([sender, receiver])

        return Message.objects.create(
            sender=sender,
            receiver=receiver,
            conversation_id=conversation,
            **validated_data
        )

class ConversationSerializer(serializers.ModelSerializer):
    participants = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True)
    last_message = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = [
            'conversation_id', 'participants', 'created_at', 'messages',
            'last_message'
        ]
        read_only_fields = ['conversation_id', 'created_at']

    def get_last_message(self, obj):
        last_message = obj.messages.last()
        return (
            last_message.content[:30] + "..."
            if last_message else "No messages yet"
        )

class NotificationSerializer(serializers.ModelSerializer):
    user = MinimalUserSerializer(read_only=True)
    message = MessageSerializer(read_only=True)

    class Meta:
        model = Notification
        fields = ['notification_id', 'user', 'message', 'is_read', 'timestamp']
        read_only_fields = ['notification_id', 'timestamp']
    
    def create(self, validated_data):
        return Notification.objects.create(**validated_data)