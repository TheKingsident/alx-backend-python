from django.shortcuts import render
from .serializers import UserSerializer, ConversationSerializer, MessageSerializer, NotificationSerializer
from rest_framework import viewsets, filters, status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from .models import User, Conversation, Message, Notification
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.decorators import action
from .permissions import IsConversationParticipant
from .pagination import CustomPagination
from .filters import MessageFilter
from django.db.models import Q

class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing users.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=False, methods=['delete'], permission_classes=[IsAuthenticated])
    def delete_user(self, request):
        """
        Endpoint to delete the authenticated user's account.
        """
        user = request.user
        user.delete()
        return Response({"detail": "User account deleted successfully."}, status=status.HTTP_204_NO_CONTENT)

class MessageViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing messages.
    """
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['conversation_id', 'sender_id', 'recipient_id']
    ordering_fields = ['timestamp']
    ordering = ['timestamp']
    permission_classes = [IsAuthenticated, IsConversationParticipant]
    pagination_class = CustomPagination
    filterset_class = MessageFilter

    def get_queryset(self):
        """
        Override to filter messages by the authenticated user's conversations.
        """
        user = self.request.user
        # ["sender=request.user"]
        if user.is_authenticated:

            return (
                Message.objects.filter(
                    Q(sender=user) | Q(receiver=user)
                ).select_related(
                    'sender', 'receiver', 'parent_message'
                ).prefetch_related(
                    'replies'
                ).order_by(
                    'timestamp'
                )
            )
        return Message.objects.none()
    
    @staticmethod
    def get_thread(message):
        """
        Fetch replies to a message
        """
        thread = {
            'message_id': message.message_id,
            'content': message.content,
            'sender': message.sender.username,
            'timestamp': message.timestamp,
            'replies': []
        }

        for reply in message.replies.all().order_by('timestamp'):
            thread['replies'].append(MessageViewSet.get_thread(reply))

        return thread
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def unread(self, request):
        user = request.user
        unread_messages = Message.unread.unread_for_user(user)
        serializer = self.get_serializer(unread_messages, many=True)
        return Response(serializer.data)

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

class NotificationViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for managing notifications.
    """
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Override to filter notifications by the authenticated user.
        """
        user = self.request.user
        return Notification.objects.filter(user=user).order_by('-timestamp')
    
    def mark_as_read(self, request, *args, **kwargs):
        notification = self.get_object()
        if notification.user != request.user:
            return Response({"detail": "You do not have permission to mark this notification as read."}, status=status.HTTP_403_FORBIDDEN)
        
        notification.is_read = True
        notification.save()
        return Response({"detail": "Notification marked as read."}, status=status.HTTP_200_OK)
