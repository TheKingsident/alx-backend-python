from django.urls import path, include
from rest_framework import routers as router
from .views import UserViewSet, MessageViewSet, ConversationViewSet


router = router.DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'messages', MessageViewSet, basename='message')
router.register(r'conversations', ConversationViewSet, basename='conversation')

urlpatterns = [
    path('', include(router.urls)),
]