from django.urls import path
from . import views

urlpatterns = [
    # Authentication
    path('login/', views.admin_login, name='admin_login'),
    path('logout/', views.admin_logout, name='admin_logout'),
    path('', views.admin_dashboard, name='admin_dashboard'),  # Default admin route
    
    # Password Management
    path('change-password/', views.change_password, name='admin_change_password'),
    path('password-reset/', views.password_reset_request, name='admin_password_reset'),
    path('password-reset-confirm/<uidb64>/<token>/', views.password_reset_confirm, name='admin_password_reset_confirm'),
    
    # Content Management
    path('content/<str:content_type>/', views.content_list, name='content_list'),
    path('content/<str:content_type>/add/', views.content_form, name='content_add'),
    path('content/<str:content_type>/edit/<int:object_id>/', views.content_form, name='content_edit'),
    path('content/<str:content_type>/delete/<int:object_id>/', views.delete_content, name='content_delete'),
    path('add/<str:content_type>/', views.content_form, name='add_content'),
    path('edit/<str:content_type>/<int:object_id>/', views.content_form, name='edit_content'),
    
    
    # AJAX endpoints
    path('ajax/toggle-approval/', views.toggle_approval, name='toggle_approval'),
    path('ajax/mark-as-read/', views.mark_as_read, name='mark_as_read'),
    path('ajax/bulk-action/', views.bulk_action, name='bulk_action'),
    
    # Export functionality
    path('export/<str:content_type>/', views.export_csv, name='export_csv'),
    
    # Activity logs
    path('activity-logs/', views.activity_logs, name='activity_logs'),
    
    # Settings
    path('settings/', views.admin_settings, name='admin_settings'),
]