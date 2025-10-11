from django.http import HttpResponseForbidden
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from functools import wraps

def admin_required(view_func):
    """
    Decorator for views that checks that the user is logged in and has admin access.
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('admin_login')
        
        if not request.user.has_admin_access():
            return HttpResponseForbidden("You don't have permission to access this page.")
        
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def superuser_required(view_func):
    """
    Decorator for views that checks that the user is a superuser.
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('admin_login')
        
        if not (request.user.is_superuser or request.user.role == 'admin'):
            return HttpResponseForbidden("You don't have permission to access this page.")
        
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def editor_required(view_func):
    """
    Decorator for views that checks that the user has editor or higher permissions.
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('admin_login')
        
        if not request.user.has_editor_access():
            return HttpResponseForbidden("You don't have permission to access this page.")
        
        return view_func(request, *args, **kwargs)
    return _wrapped_view