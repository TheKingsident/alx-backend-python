from django.urls import path, include
from rest_framework import routers
from rest_framework_nested.routers import NestedDefaultRouter
from .views import UserViewSet, MessageViewSet, ConversationViewSet, NotificationViewSet


router = routers.DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'messages', MessageViewSet, basename='message')
router.register(r'conversations', ConversationViewSet, basename='conversation')
router.register(r'notifications', NotificationViewSet, basename='notification')


conversations_router = NestedDefaultRouter(router, r'conversations', lookup='conversation')
conversations_router.register(r'messages', MessageViewSet, basename='conversation-messages')


urlpatterns = [
    path('', include(router.urls)),
    path('', include(conversations_router.urls)),
]