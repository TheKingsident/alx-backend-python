from rest_framework import permissions


class IsConversationParticipant(permissions.BasePermission):
    """
    Custom permission to only allow participants of a conversation to access it.
    Allows PUT, PATCH, DELETE only for participants.
    """

    def has_permission(self, request, view):
        # Allow access if the user is authenticated
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Only allow PUT, PATCH, DELETE for participants
        if request.method in ["PUT", "PATCH", "DELETE"]:
            if hasattr(obj, 'participants'):
                return request.user in obj.participants.all()
            elif hasattr(obj, 'conversation_id'):
                return request.user in obj.conversation_id.participants.all()
            return False
        # For other methods (GET, POST), use the same logic
        if hasattr(obj, 'participants'):
            return request.user in obj.participants.all()
        elif hasattr(obj, 'conversation_id'):
            return request.user in obj.conversation_id.participants.all()
        return False
