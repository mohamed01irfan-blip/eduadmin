from contact.models import Message

def unread_count(request):
    """Inject unread message count into every template context."""
    if request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser):
        count = Message.objects.filter(is_read=False).count()
        return {'unread_count': count}
    return {'unread_count': 0}
