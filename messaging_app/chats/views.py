from django.shortcuts import render
from .serializers import UserSerializer, ConversationSerializer, MessageSerializer
from rest_framework import viewsets
from rest_framework.response import Response
from .models import User, Conversation, Message


class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing users.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

class MessageViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing messages.
    """
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    def get_queryset(self):
        """
        Optionally restricts the returned messages to those sent or received by the authenticated user.
        """
        user = self.request.user
        if user.is_authenticated:
            return Message.objects.filter(sender_id=user) | Message.objects.filter(recipient_id=user)
        return Message.objects.none()
    
    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        data['sender_id'] = request.user.id
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=201)


class ConversationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing conversations.
    """
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    
    def get_queryset(self):
        """
        Optionally restricts the returned conversations to those involving the authenticated user.
        """
        user = self.request.user
        if user.is_authenticated:
            return Conversation.objects.filter(participants=user)
        return Conversation.objects.none()
    
    def create(self, request, *args, **kwargs):
        participants = request.data.get('participants', [])
        if not isinstance(participants, list) or len(participants) < 2:
            return Response({"error": "At least two participants are required to create a conversation."}, status=400)
        
        conversation = Conversation.objects.create()
        conversation.participants.set(User.objects.filter(id__in=participants))
        conversation.save()
        
        serializer = self.get_serializer(conversation)
        return Response(serializer.data, status=201)
