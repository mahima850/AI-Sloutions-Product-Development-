from urllib import request
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponse, Http404
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from django.db.models import Q, Count, Avg
from django.apps import apps
from django.contrib.auth.forms import PasswordChangeForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
import csv
import json
from datetime import datetime, timedelta
from django.utils import timezone

from .decorators import admin_required, superuser_required
from core.models import *
from core.forms import (
    AboutUsForm,
    SolutionForm,
    BlogPostForm,
    EventForm,
    GalleryItemForm,
    CustomUserCreationForm,
    ArticleForm,
    TeamMemberForm
)


def admin_login(request):
    """Admin login view"""
    if request.user.is_authenticated and request.user.has_admin_access():
        return redirect('admin_dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None and user.has_admin_access():
            login(request, user)
            messages.success(request, f'Welcome back, {user.first_name or user.username}!')
            
            # Log activity
            ActivityLog.objects.create(
                user=user,
                action='view',
                content_type='Admin Dashboard',
                object_id=1,
                object_repr='Admin Login',
                ip_address=get_client_ip(request)
            )
            
            next_url = request.GET.get('next', 'admin_dashboard')
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid credentials or insufficient permissions.')
    
    return render(request, 'admin/login.html')

def admin_logout(request):
    """Admin logout view"""
    if request.user.is_authenticated:
        # Log activity
        ActivityLog.objects.create(
            user=request.user,
            action='view',
            content_type='Admin Dashboard',
            object_id=1,
            object_repr='Admin Logout',
            ip_address=get_client_ip(request)
        )
    
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('admin_login')

@admin_required
def admin_dashboard(request):
    """Main admin dashboard view"""
    # Get dashboard statistics
    stats = {
        'total_inquiries': ContactInquiry.objects.count(),
        'unread_inquiries': ContactInquiry.objects.filter(is_read=False).count(),
        'total_feedback': Feedback.objects.count(),
        'pending_feedback': Feedback.objects.filter(is_approved=False).count(),
        'total_blog_posts': BlogPost.objects.count(),
        'draft_posts': BlogPost.objects.filter(status='draft').count(),
        'total_events': Event.objects.count(),
        'upcoming_events': Event.objects.filter(status='upcoming').count(),
        'newsletter_subscribers': Newsletter.objects.filter(is_active=True).count(),
        'total_users': CustomUser.objects.count(),
    }
    
    # Recent activities
    recent_activities = ActivityLog.objects.select_related('user').order_by('-timestamp')[:10]
    
    # Recent inquiries
    recent_inquiries = ContactInquiry.objects.order_by('-created_at')[:5]
    
    # Upcoming events
    upcoming_events = Event.objects.filter(
        status='upcoming',
        date__gte=timezone.now().date()
    ).order_by('date')[:5]
    
    # Monthly statistics for charts
    current_month = timezone.now().replace(day=1)
    months_data = []
    
    for i in range(6):
        month_start = current_month - timedelta(days=30*i)
        month_end = month_start + timedelta(days=30)
        
        month_stats = {
            'month': month_start.strftime('%b %Y'),
            'inquiries': ContactInquiry.objects.filter(
                created_at__gte=month_start,
                created_at__lt=month_end
            ).count(),
            'feedback': Feedback.objects.filter(
                created_at__gte=month_start,
                created_at__lt=month_end
            ).count(),
        }
        months_data.append(month_stats)
    
    months_data.reverse()
    
    context = {
        'stats': stats,
        'recent_activities': recent_activities,
        'recent_inquiries': recent_inquiries,
        'upcoming_events': upcoming_events,
        'months_data': months_data,
    }
    
    return render(request, 'admin/dashboard.html', context)

# -----------------------
# Content List View
# -----------------------
@admin_required
def content_list(request, content_type):
    """Generic content listing view"""
    model_mapping = {
        'solutions': Solution,
        'blog': BlogPost,
        'users': CustomUser,
        'events': Event,
        'gallery': GalleryItem,
        'articles': Article,
        'team': TeamMember,
        'inquiries': ContactInquiry,
        'feedback': Feedback,
        'newsletter': Newsletter,
        'about': AboutUs,
    }

    if content_type not in model_mapping:
        raise Http404("Content type not found")

    model = model_mapping[content_type]
    search_query = request.GET.get('search', '')
    queryset = model.objects.all()

    if search_query:
        if content_type == 'inquiries':
            queryset = queryset.filter(
                Q(name__icontains=search_query) |
                Q(email__icontains=search_query) |
                Q(company__icontains=search_query)
            )
        elif content_type == 'feedback':
            queryset = queryset.filter(
                Q(name__icontains=search_query) |
                Q(company__icontains=search_query)
            )
        elif content_type in ['blog', 'articles']:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(content__icontains=search_query)
            )
        elif content_type == 'users':
            queryset = queryset.filter(
                Q(username__icontains=search_query) |
                Q(email__icontains=search_query) |
                Q(first_name__icontains=search_query) |
                Q(last_name__icontains=search_query)
            )

    if hasattr(model, 'created_at'):
        queryset = queryset.order_by('-created_at')
    elif hasattr(model, 'date_joined'):
        queryset = queryset.order_by('-date_joined')

    paginator = Paginator(queryset, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'content_type': content_type,
        'page_obj': page_obj,
        'search_query': search_query,
        'total_count': queryset.count(),
    }

    return render(request, 'admin/content_list.html', context)


# -----------------------
# Content Form View
# -----------------------
@admin_required
def content_form(request, content_type, object_id=None):
    """Generic content form view for adding/editing content"""
    # Correct model/form mapping
    model_mapping = {
        'solutions': Solution,
        'blog': BlogPost,
        'users': CustomUser,
        'events': Event,
        'gallery': GalleryItem,
        'articles': Article,
        'team': TeamMember,
        'inquiries': ContactInquiry,
        'feedback': Feedback,
        'newsletter': Newsletter,
        'about': AboutUs,
    }

    form_mapping = {
        'solutions': SolutionForm,
        'blog': BlogPostForm,
        'users': CustomUserCreationForm,
        'events': EventForm,
        'gallery': GalleryItemForm,
        'articles': ArticleForm,
        'team': TeamMemberForm,
        'inquiries': None,  # Typically inquiries are not created via form
        'feedback': None,   # Feedback usually comes from users, not admin creation
        'newsletter': None, # Newsletter subscriptions are user-driven
        'about': AboutUsForm,
    }  

    if content_type not in model_mapping:
        raise Http404(f"Content type '{content_type}' not found.")

    ModelClass = model_mapping[content_type]
    FormClass = form_mapping[content_type]
    instance = get_object_or_404(ModelClass, id=object_id) if object_id else None

    if request.method == 'POST':
        form = FormClass(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            obj = form.save(commit=False)

            # Special fields
            if content_type == 'blog' and request.user.is_authenticated:
                obj.author = request.user
            if content_type == 'gallery':
                obj.uploaded_by = request.user
            if content_type == 'events':
                obj.created_by = request.user

            obj.save()
            messages.success(
                request,
                f"{content_type.capitalize()} {'updated' if instance else 'created'} successfully."
            )
            return redirect('content_list', content_type=content_type)
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = FormClass(instance=instance)

    context = {
        'content_type': content_type,
        'instance': instance,
        'form': form,
        'is_edit': bool(instance),
    }
    return render(request, 'admin/content_form.html', context)


# -----------------------
# Delete Content
# -----------------------
@admin_required
def delete_content(request, content_type, object_id):
    model_mapping = {
        'solutions': Solution,
        'blog': BlogPost,
        'users': CustomUser,
        'events': Event,
        'gallery': GalleryItem,
        'articles': Article,
        'team': TeamMember,
        'inquiries': ContactInquiry,
        'feedback': Feedback,
        'newsletter': Newsletter,
        'about': AboutUs,
    }

    if content_type not in model_mapping:
        raise Http404("Content type not found")

    model = model_mapping[content_type]
    instance = get_object_or_404(model, id=object_id)

    if request.method == 'POST':
        instance.delete()
        messages.success(request, f"{content_type.capitalize()} deleted successfully.")
        return redirect('content_list', content_type=content_type)

    return render(request, 'admin/confirm_delete.html', {
        'content_type': content_type,
        'instance': instance
    })

# -----------------------
# Export CSV
# -----------------------
@admin_required
def export_csv(request, content_type):
    model_mapping = {
        'inquiries': ContactInquiry,
        'feedback': Feedback,
        'blog': BlogPost,
        'articles': Article,
        'events': Event,
        'gallery': GalleryItem,
        'solutions': Solution,
        'users': CustomUser,
        'team': TeamMember,
        'newsletter': Newsletter,
        'about': AboutUs,
    }

    if content_type not in model_mapping:
        raise Http404("Content type not found")

    model = model_mapping[content_type]
    queryset = model.objects.all()

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{content_type}_{datetime.now().strftime("%Y%m%d")}.csv"'

    writer = csv.writer(response)
    fields = [field.name for field in model._meta.fields if not field.name.endswith('_ptr')]
    writer.writerow(fields)

    for obj in queryset:
        row = [str(getattr(obj, field)) if getattr(obj, field) is not None else '' for field in fields]
        writer.writerow(row)

    return response

@admin_required
@require_http_methods(["POST"])
def toggle_approval(request):
    """Toggle approval status for feedback"""
    try:
        data = json.loads(request.body)
        feedback_id = data.get('id')
        
        feedback = get_object_or_404(Feedback, id=feedback_id)
        feedback.is_approved = not feedback.is_approved
        
        if feedback.is_approved:
            feedback.approved_by = request.user
        
        feedback.save()
        
        return JsonResponse({
            'success': True,
            'is_approved': feedback.is_approved
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

@admin_required
@require_http_methods(["POST"])
def mark_as_read(request):
    """Mark inquiry as read"""
    try:
        data = json.loads(request.body)
        inquiry_id = data.get('id')
        
        inquiry = get_object_or_404(ContactInquiry, id=inquiry_id)
        inquiry.is_read = True
        inquiry.save()
        
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

@admin_required
def change_password(request):
    """Change admin password"""
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('admin_dashboard')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = PasswordChangeForm(request.user)
    
    return render(request, 'admin/change_password.html', {'form': form})

def password_reset_request(request):
    """Password reset request view"""
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = CustomUser.objects.get(email=email)
                if user.has_admin_access():
                    # Generate token
                    token = default_token_generator.make_token(user)
                    uid = urlsafe_base64_encode(force_bytes(user.pk))
                    
                    # Create reset URL
                    reset_url = request.build_absolute_uri(
                        reverse('admin_password_reset_confirm', kwargs={'uidb64': uid, 'token': token})
                    )
                    
                    # Send email
                    subject = 'AI-Solution Admin Password Reset'
                    message = render_to_string('admin/password_reset_email.html', {
                        'user': user,
                        'reset_url': reset_url,
                        'site_name': 'AI-Solution Admin'
                    })
                    
                    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email])
                    messages.success(request, 'Password reset email has been sent.')
                    return redirect('admin_login')
                else:
                    messages.error(request, 'This email is not associated with an admin account.')
            except CustomUser.DoesNotExist:
                messages.error(request, 'No admin account found with this email address.')
    else:
        form = PasswordResetForm()
    
    return render(request, 'admin/password_reset.html', {'form': form})

def password_reset_confirm(request, uidb64, token):
    """Password reset confirmation view"""
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None
    
    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Your password has been reset successfully. You can now log in.')
                return redirect('admin_login')
        else:
            form = SetPasswordForm(user)
        
        return render(request, 'admin/password_reset_confirm.html', {'form': form})
    else:
        messages.error(request, 'The password reset link is invalid or has expired.')
        return redirect('admin_login')

@admin_required
def bulk_action(request):
    """Handle bulk actions on content"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            action = data.get('action')
            content_type = data.get('content_type')
            object_ids = data.get('object_ids', [])
            
            model_mapping = {
                'inquiries': ContactInquiry,
                'feedback': Feedback,
                'blog': BlogPost,
                'articles': Article,
                'events': Event,
                'gallery': GalleryItem,
                'solutions': Solution,
                'users': CustomUser,
                'newsletter': Newsletter,
                'team': TeamMemberForm,
                'about': AboutUs,
            }
            
            if content_type not in model_mapping:
                return JsonResponse({'success': False, 'error': 'Invalid content type'})
            
            model = model_mapping[content_type]
            queryset = model.objects.filter(id__in=object_ids)
            
            if action == 'delete':
                count = queryset.count()
                queryset.delete()
                messages.success(request, f'{count} items deleted successfully.')
            elif action == 'approve' and content_type == 'feedback':
                queryset.update(is_approved=True, approved_by=request.user)
                messages.success(request, f'{queryset.count()} feedback items approved.')
            elif action == 'mark_read' and content_type == 'inquiries':
                queryset.update(is_read=True)
                messages.success(request, f'{queryset.count()} inquiries marked as read.')
            
            # Log bulk action
            ActivityLog.objects.create(
                user=request.user,
                action='bulk_' + action,
                content_type=content_type.capitalize(),
                object_id=0,
                object_repr=f'Bulk action on {len(object_ids)} items',
                ip_address=get_client_ip(request)
            )
            
            return JsonResponse({'success': True})
            
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

@admin_required
def activity_logs(request):
    """View activity logs"""
    logs = ActivityLog.objects.select_related('user').order_by('-timestamp')
    
    # Filter by user if specified
    user_filter = request.GET.get('user')
    if user_filter:
        logs = logs.filter(user__username__icontains=user_filter)
    
    # Filter by action if specified
    action_filter = request.GET.get('action')
    if action_filter:
        logs = logs.filter(action=action_filter)
    
    # Filter by date range if specified
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    if date_from:
        logs = logs.filter(timestamp__date__gte=date_from)
    if date_to:
        logs = logs.filter(timestamp__date__lte=date_to)
    
    # Pagination
    paginator = Paginator(logs, 50)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get unique actions for filter
    actions = ActivityLog.objects.values_list('action', flat=True).distinct()
    
    context = {
        'page_obj': page_obj,
        'actions': actions,
        'user_filter': user_filter,
        'action_filter': action_filter,
        'date_from': date_from,
        'date_to': date_to,
    }
    
    return render(request, 'admin/activity_logs.html', context)

@admin_required
def admin_settings(request):
    """Admin settings view"""
    site_settings = SiteSettings.load()
    
    if request.method == 'POST':
        # Update site settings
        site_settings.site_name = request.POST.get('site_name', '')
        site_settings.site_description = request.POST.get('site_description', '')
        site_settings.contact_email = request.POST.get('contact_email', '')
        site_settings.contact_phone = request.POST.get('contact_phone', '')
        site_settings.address = request.POST.get('address', '')
        site_settings.social_facebook = request.POST.get('social_facebook', '')
        site_settings.social_twitter = request.POST.get('social_twitter', '')
        site_settings.social_linkedin = request.POST.get('social_linkedin', '')
        site_settings.google_analytics_id = request.POST.get('google_analytics_id', '')
        site_settings.maintenance_mode = request.POST.get('maintenance_mode') == 'on'
        site_settings.save()
        
        messages.success(request, 'Settings updated successfully.')
        return redirect('admin_settings')
    
    context = {
        'site_settings': site_settings,
    }
    
    return render(request, 'admin/settings.html', context)

def get_client_ip(request):
    """Get client IP address"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
# Content List View
@admin_required
def content_list(request, content_type):
    """Generic content listing view"""
    model_mapping = {
        'inquiries': ContactInquiry,
        'feedback': Feedback,
        'blog': BlogPost,
        'articles': Article,
        'events': Event,
        'gallery': GalleryItem,
        'solutions': Solution,
        'users': CustomUser,
        'newsletter': Newsletter,
        'team': TeamMember,
        'about': AboutUs,
    }
    
    if content_type not in model_mapping:
        raise Http404("Content type not found")
    
    model = model_mapping[content_type]
    
    search_query = request.GET.get('search', '')
    queryset = model.objects.all()
    
    if search_query:
        if content_type == 'inquiries':
            queryset = queryset.filter(
                Q(name__icontains=search_query) |
                Q(email__icontains=search_query) |
                Q(company__icontains=search_query)
            )
        elif content_type == 'feedback':
            queryset = queryset.filter(
                Q(name__icontains=search_query) |
                Q(company__icontains=search_query)
            )
        elif content_type == 'blog':
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(content__icontains=search_query)
            )
        elif content_type == 'users':
            queryset = queryset.filter(
                Q(username__icontains=search_query) |
                Q(email__icontains=search_query) |
                Q(first_name__icontains=search_query) |
                Q(last_name__icontains=search_query)
            )
    
    if hasattr(model, 'created_at'):
        queryset = queryset.order_by('-created_at')
    elif hasattr(model, 'date_joined'):
        queryset = queryset.order_by('-date_joined')
    
    paginator = Paginator(queryset, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'content_type': content_type,
        'page_obj': page_obj,
        'search_query': search_query,
        'total_count': queryset.count(),
    }
    
    return render(request, 'admin/content_list.html', context)

# Content Form View
@admin_required
def content_form(request, content_type, object_id=None):
    """
    Generic content form view for adding/editing content.
    Supports: solutions, blog, users, events, gallery, articles.
    """
    # Model and form mapping
    model_mapping = {
        'solutions': Solution,
        'blog': BlogPost,
        'users': CustomUser,
        'events': Event,
        'gallery': GalleryItem,
        'articles': Article,
        'team': TeamMember,
        'about': AboutUs,
    }

    form_mapping = {
        'solutions': SolutionForm,
        'blog': BlogPostForm,
        'users': CustomUserCreationForm,
        'events': EventForm,
        'gallery': GalleryItemForm,
        'articles': ArticleForm,
        'team': TeamMemberForm,
        'about': AboutUsForm,  # Typically AboutUs is a single instance managed differently
    }

    if content_type not in model_mapping:
        raise Http404(f"Content type '{content_type}' not found.")

    ModelClass = model_mapping[content_type]
    FormClass = form_mapping[content_type]

    instance = None
    if object_id:
        instance = get_object_or_404(ModelClass, id=object_id)

    if request.method == 'POST':
        form = FormClass(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            obj = form.save(commit=False)
            # For gallery, set uploaded_by automatically
            if content_type == 'gallery' and not obj.uploaded_by:
                obj.uploaded_by = request.user
            # For event, set created_by automatically if needed
            if content_type == 'events' and not obj.created_by:
                obj.created_by = request.user
            obj.save()
            messages.success(request, f"{content_type.capitalize()} {'updated' if instance else 'created'} successfully.")
            return redirect('content_list', content_type=content_type)
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = FormClass(instance=instance)

    context = {
        'content_type': content_type,
        'instance': instance,
        'form': form,
        'is_edit': bool(instance),
    }
    return render(request, 'admin/content_form.html', context)

# Delete Content View
@admin_required
def delete_content(request, content_type, object_id):
    """Delete content object"""
    model_mapping = {
        'inquiries': ContactInquiry,
        'feedback': Feedback,
        'blog': BlogPost,
        'articles': Article,
        'events': Event,
        'gallery': GalleryItem,
        'solutions': Solution,
        'users': CustomUser,
        'team': TeamMember,
        'newsletter': Newsletter,
        'about': AboutUs,
    }
    
    if content_type not in model_mapping:
        raise Http404("Content type not found")
    
    model = model_mapping[content_type]
    instance = get_object_or_404(model, id=object_id)
    
    if request.method == 'POST':
        instance.delete()
        messages.success(request, f'{content_type.capitalize()} deleted successfully.')
        return redirect('content_list', content_type=content_type)
    
    return render(request, 'admin/confirm_delete.html', {
        'content_type': content_type,
        'instance': instance
    })

# Export Content to CSV
@admin_required
def export_csv(request, content_type):
    """Export content to CSV"""
    model_mapping = {
        'inquiries': ContactInquiry,
        'feedback': Feedback,
        'blog': BlogPost,
        'solutions': Solution,
        'users': CustomUser,
    }
    
    if content_type not in model_mapping:
        raise Http404("Content type not found")
    
    model = model_mapping[content_type]
    queryset = model.objects.all()

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{content_type}_{datetime.now().strftime("%Y%m%d")}.csv"'

    writer = csv.writer(response)
    
    fields = [field.name for field in model._meta.fields if not field.name.endswith('_ptr')]
    writer.writerow(fields)

    for obj in queryset:
        row = [str(getattr(obj, field)) if getattr(obj, field) is not None else '' for field in fields]
        writer.writerow(row)

    return response

# Helper function to get client IP address
def get_client_ip(request):
    """Get client IP address"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
