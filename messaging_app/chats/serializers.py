from rest_framework import serializers
from django.db import models
from .models import User, Conversation, Message

class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source='get_full_name', read_only=True)

    class Meta:
        model = User
        fields = [
            'user_id', 'username', 'email', 'first_name', 'last_name', 'full_name',
            'phone_number'
        ]
        read_only_fields = ['user_id']

class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True, source='sender_id')
    recipient = UserSerializer(read_only=True, source='recipient_id')

    recipient_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), write_only=True
    )
    conversation_id = serializers.PrimaryKeyRelatedField(
        queryset=Conversation.objects.all(), write_only=True,
        allow_null=True, required=False
    )

    class Meta:
        model = Message
        fields = [
            'message_id', 'sender', 'recipient', 'recipient_id', 'conversation_id',
            'message_body', 'sent_at',
        ]
        read_only_fields = ['message_id', 'sent_at']

    def validate_message_body(self, value):
        if not value.strip():
            raise serializers.ValidationError("Message body cannot be empty.")
        return value

    def create(self, validated_data):
        recipient = validated_data.pop('recipient_id')
        conversation = validated_data.pop('conversation_id')
        sender = self.context['request'].user

        if conversation is None:
            conversations = Conversation.objects.filter(participants=sender).filter(participants=recipient)
            conversations = conversations.annotate(num_participants=models.Count('participants')).filter(num_participants=2)
            if conversations.exists():
                conversation = conversations.first()
            else:
                conversation = Conversation.objects.create()
                conversation.participants.set([sender, recipient])

        return Message.objects.create(
            sender_id=sender,
            recipient_id=recipient,
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
            last_message.message_body[:30] + "..."
            if last_message else "No messages yet"
        )
