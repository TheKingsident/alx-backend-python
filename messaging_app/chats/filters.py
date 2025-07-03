import django_filters
from .models import Message


class MessageFilter(django_filters.FilterSet):
    """
    FilterSet for Message model to filter by sender, recipient, and conversation.
    """
    sender = django_filters.CharFilter(field_name='sender_id__username', lookup_expr='icontains')
    recipient = django_filters.CharFilter(field_name='recipient_id__username', lookup_expr='icontains')
    sent_after = django_filters.DateTimeFilter(field_name='sent_at', lookup_expr='gte')
    sent_before = django_filters.DateTimeFilter(field_name='sent_at', lookup_expr='lte')

    class Meta:
        model = Message
        fields = ['sender', 'recipient', 'sent_after', 'sent_before']
