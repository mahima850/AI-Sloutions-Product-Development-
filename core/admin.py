from django.contrib import admin
from django.contrib.auth import get_user_model
from import_export.admin import ImportExportModelAdmin
from django.contrib.auth.admin import UserAdmin
from .models import *
from .forms import SolutionForm
from django.utils.html import format_html

# Ensure the custom user model is referenced correctly
CustomUser = get_user_model()

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'is_active', 'date_joined')
    list_filter = ('role', 'is_active', 'is_staff', 'date_joined')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('-date_joined',)
    
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('role', 'phone', 'profile_image')}), 
    )


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ('site_name', 'contact_email', 'updated_by', 'updated_at')
    readonly_fields = ('updated_at',)
    
    def save_model(self, request, obj, form, change):
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)
    
    def has_add_permission(self, request):
        return not SiteSettings.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(AboutUs)
class AboutUsAdmin(admin.ModelAdmin):
    list_display = ('title', 'updated_by', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')
    
    def save_model(self, request, obj, form, change):
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(Solution)
class SolutionAdmin(admin.ModelAdmin):
    form = SolutionForm  

    list_display = ('title', 'category', 'is_featured', 'is_active', 'order', 'created_at', 'preview_image')
    list_filter = ('category', 'is_featured', 'is_active')
    search_fields = ('title', 'description', 'detailed_content')
    list_editable = ('is_featured', 'is_active', 'order')
    ordering = ('order', 'title')
    readonly_fields = ('created_at', 'updated_at', 'preview_image')

    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'detailed_content', 'category', 'icon', 'image', 'preview_image')
        }),
        ('Additional Info', {
            'fields': ('features', 'benefits', 'use_cases', 'faqs')
        }),
        ('Status & Order', {
            'fields': ('is_active', 'is_featured', 'order')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )

    def preview_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width: 100px; height:auto;"/>', obj.image.url)
        return "-"
    preview_image.short_description = "Preview Image"

@admin.register(ContactInquiry)
class ContactInquiryAdmin(ImportExportModelAdmin):
    list_display = ('name', 'email', 'company', 'country', 'is_read', 'is_responded', 'created_at')
    list_filter = ('is_read', 'is_responded', 'country', 'job_title', 'created_at')
    search_fields = ('name', 'email', 'company', 'message')
    readonly_fields = ('created_at', 'updated_at')
    list_editable = ('is_read', 'is_responded')
    ordering = ('-created_at',)

    def get_queryset(self, request):
        return super().get_queryset(request).select_related()


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('name', 'company', 'rating', 'is_approved', 'is_featured', 'created_at')
    list_filter = ('rating', 'is_approved', 'is_featured', 'created_at')
    search_fields = ('name', 'email', 'company', 'comment')
    list_editable = ('is_approved', 'is_featured')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')
    
    def save_model(self, request, obj, form, change):
        if obj.is_approved and not obj.approved_by:
            obj.approved_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'status', 'is_featured', 'views_count', 'published_at')
    list_filter = ('status', 'category', 'is_featured', 'published_at')
    search_fields = ('title', 'excerpt', 'content')
    list_editable = ('status', 'is_featured')
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('views_count', 'created_at', 'updated_at', 'published_at')
    ordering = ('-created_at',)

    def save_model(self, request, obj, form, change):
        if not obj.author_id:
            obj.author = request.user
        super().save_model(request, obj, form, change)


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'article_type', 'author', 'is_featured', 'download_count', 'published_at')
    list_filter = ('article_type', 'is_featured', 'published_at')
    search_fields = ('title', 'description')
    list_editable = ('is_featured',)
    readonly_fields = ('download_count', 'created_at', 'updated_at')
    ordering = ('-published_at',)


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'event_type', 'date', 'location', 'status', 'capacity', 'is_featured')
    list_filter = ('event_type', 'status', 'is_featured', 'date')
    search_fields = ('title', 'description', 'location')
    list_editable = ('status', 'is_featured')
    ordering = ('date', 'time')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(GalleryItem)
class GalleryItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'event_date', 'location', 'is_featured', 'order')
    list_filter = ('category', 'is_featured', 'event_date')
    search_fields = ('title', 'description', 'event_name', 'location')
    list_editable = ('is_featured', 'order')
    ordering = ('-event_date', 'order')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(EventRegistration)
class EventRegistrationAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'event', 'registration_date', 'is_confirmed', 'attended')
    list_filter = ('is_confirmed', 'attended', 'registration_date', 'event')
    search_fields = ('name', 'email', 'company')
    list_editable = ('is_confirmed', 'attended')
    ordering = ('-registration_date',)


@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ('email', 'name', 'is_active', 'subscribed_at')
    list_filter = ('is_active', 'subscribed_at')
    search_fields = ('email', 'name')
    list_editable = ('is_active',)
    ordering = ('-subscribed_at',)


@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'action', 'content_type', 'object_repr', 'timestamp', 'ip_address')
    list_filter = ('action', 'content_type', 'timestamp')
    search_fields = ('user__username', 'object_repr')
    readonly_fields = ('user', 'action', 'content_type', 'object_id', 'object_repr', 'timestamp', 'ip_address')
    ordering = ('-timestamp',)
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False

