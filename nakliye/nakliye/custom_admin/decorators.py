"""
Custom Admin Panel - Güvenlik Dekoratörleri
Session tabanlı kimlik doğrulama ve yetki kontrol dekoratörleri
"""

from functools import wraps
from django.shortcuts import redirect
from django.http import Http404
from django.conf import settings
from .models import AdminUser


def get_admin_login_url():
    """Config'den admin login URL'ini döndürür"""
    base = getattr(settings, 'ADMIN_PANEL_ROUTE', 'yonetim-paneli-gizli')
    return f'/{base}/login/'


def admin_login_required(view_func):
    """
    Admin girişi zorunlu kılan dekoratör.
    Session'da admin_user_id yoksa login sayfasına yönlendirir.
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        admin_user_id = request.session.get('admin_user_id')
        if not admin_user_id:
            return redirect(get_admin_login_url())
        
        try:
            admin_user = AdminUser.objects.get(id=admin_user_id, is_active=True)
            request.admin_user = admin_user
        except AdminUser.DoesNotExist:
            # Geçersiz session - temizle
            request.session.flush()
            return redirect(get_admin_login_url())
        
        return view_func(request, *args, **kwargs)
    return wrapper


def superadmin_required(view_func):
    """
    Superadmin yetkisi zorunlu kılan dekoratör.
    Sadece superadmin rolündeki kullanıcılar erişebilir.
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        admin_user_id = request.session.get('admin_user_id')
        if not admin_user_id:
            return redirect(get_admin_login_url())
        
        try:
            admin_user = AdminUser.objects.get(id=admin_user_id, is_active=True)
            if not admin_user.is_superadmin:
                from django.contrib import messages
                messages.error(request, 'Bu işlem için süper admin yetkisi gereklidir.')
                base = getattr(settings, 'ADMIN_PANEL_ROUTE', 'yonetim-paneli-gizli')
                return redirect(f'/{base}/')
            request.admin_user = admin_user
        except AdminUser.DoesNotExist:
            request.session.flush()
            return redirect(get_admin_login_url())
        
        return view_func(request, *args, **kwargs)
    return wrapper


def permission_required(permission_name):
    """
    Belirli bir yetki zorunlu kılan dekoratör.
    Kullanım: @permission_required('can_manage_gallery')
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            admin_user_id = request.session.get('admin_user_id')
            if not admin_user_id:
                return redirect(get_admin_login_url())
            
            try:
                admin_user = AdminUser.objects.get(id=admin_user_id, is_active=True)
                if not admin_user.has_permission(permission_name):
                    from django.contrib import messages
                    messages.error(request, 'Bu işlem için yetkiniz bulunmamaktadır.')
                    base = getattr(settings, 'ADMIN_PANEL_ROUTE', 'yonetim-paneli-gizli')
                    return redirect(f'/{base}/')
                request.admin_user = admin_user
            except AdminUser.DoesNotExist:
                request.session.flush()
                return redirect(get_admin_login_url())
            
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator
