from .models import SiteSettings, ContactInquiry, Feedback

def site_settings(request):
    """Add site settings to all templates"""
    return {
        'settings': SiteSettings.load()
    }

def admin_notifications(request):
    """Add admin notifications to templates"""
    if request.user.is_authenticated and hasattr(request.user, 'has_admin_access') and request.user.has_admin_access():
        return {
            'stats': {
                'unread_inquiries': ContactInquiry.objects.filter(is_read=False).count(),
                'pending_feedback': Feedback.objects.filter(is_approved=False).count(),
            }
        }
    return {}