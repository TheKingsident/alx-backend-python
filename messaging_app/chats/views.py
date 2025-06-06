from django.shortcuts import render
from .serializers import UserSerializer, ConversationSerializer, MessageSerializer
from rest_framework import viewsets, filters, status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from .models import User, Conversation, Message
from rest_framework.permissions import IsAuthenticated
from .permissions import IsConversationParticipant


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
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['conversation_id', 'sender_id', 'recipient_id']
    ordering_fields = ['sent_at']
    ordering = ['sent_at']
    permission_classes = [IsAuthenticated, IsConversationParticipant]

    def get_queryset(self):
        """
        Override to filter messages by the authenticated user's conversations.
        """
        user = self.request.user
        qs = Message.objects.all()
        if self.action == 'list':
            qs = qs.filter(
                conversation_id__participants=user
            ).distinct()
        return qs

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=201)
    
    def get_serializer_context(self):
        """
        Add the request user to the serializer context.
        """
        context = super().get_serializer_context()
        context.update({'request': self.request})
        return context


class ConversationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing conversations.
    """
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated, IsConversationParticipant]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]

    def get_queryset(self):
        """
        Override to filter conversations by the authenticated user.
        """
        user = self.request.user
        qs = Conversation.objects.all()
        if self.action == 'list':
            qs = qs.filter(participants=user).distinct()
        return qs
    
    def create(self, request, *args, **kwargs):
        participants = request.data.get('participants', [])
        if not isinstance(participants, list) or len(participants) < 2:
            return Response({"error": "At least two participants are required to create a conversation."}, status=400)
        
        conversation = Conversation.objects.create()
        conversation.participants.set(User.objects.filter(id__in=participants))
        conversation.save()
        
        serializer = self.get_serializer(conversation)
        return Response(serializer.data, status=201)
    
    def update(self, request, *args, **kwargs):
        conversation = self.get_object()
        if request.user not in conversation.participants.all():
            return Response({"detail": "You do not have permission to update this conversation."}, status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)
