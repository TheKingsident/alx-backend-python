from rest_framework import serializers
from .models import User, Conversation, Message

class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField()
    class Meta:
        model = User
        fields = ['user_id', 'username', 'email', 'first_name', 'last_name', 'full_name', 'phone_number']
        read_only_fields = ['user_id']

class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True, source='sender_id')
    recipient = UserSerializer(read_only=True, source='recipient_id')
    
    class Meta:
        model = Message
        fields = ['message_id', 'sender', 'recipient', 'message_body', 'sent_at']
        read_only_fields = ['message_id', 'sent_at']
    
    def validate_message_body(self, value):
        if not value.strip():
            raise serializers.ValidationError("Message body cannot be empty.")
        return value

class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True)
    last_message = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants', 'created_at', 'messages', 'last_message']
        read_only_fields = ['conversation_id', 'created_at']

    def get_last_message(self, obj):
        last_message = obj.message.last()
        return last_message.message_body[:30] + "..." if last_message else "No messages yet"
