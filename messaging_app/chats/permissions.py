from rest_framework import permissions

class IsConversationParticipant(permissions.BasePermission):
    """
    Custom permission to only allow participants of a conversation to access it.
    """

    def has_permission(self, request, view):
        # Allow access if the user is authenticated
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Check if the user is a participant in the conversation
        return request.user in obj.participants.all()