"""
Custom Admin Panel - View Fonksiyonları
Dashboard, CRUD işlemleri, kimlik doğrulama ve dosya yükleme
"""

import json
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, Http404
from django.contrib import messages
from django.utils import timezone
from django.db.models import Max
from django.views.decorators.http import require_POST, require_http_methods
from django.views.decorators.csrf import csrf_protect
from django.conf import settings

from .models import AdminUser, LoginAttempt
from .forms import (
    AdminLoginForm, AdminUserForm, PasswordChangeForm,
    SliderForm, ServiceForm, GalleryForm, FAQForm, AboutUsForm,
)
from .decorators import admin_login_required, superadmin_required, permission_required
from .middleware import get_client_ip
from core.models import SliderImage, Service, GalleryImage, ContactMessage, FAQ, AboutUs


# ==========================================
# Yardımcı Fonksiyonlar
# ==========================================

def get_admin_base_url():
    """Admin paneli ana URL'ini döndürür"""
    return getattr(settings, 'ADMIN_PANEL_ROUTE', 'yonetim-paneli-gizli')


# ==========================================
# Kimlik Doğrulama
# ==========================================

@csrf_protect
def admin_login(request):
    """
    Admin giriş sayfası.
    Rate limiting ile brute-force koruması içerir.
    """
    # Zaten giriş yapmışsa dashboard'a yönlendir
    if request.session.get('admin_user_id'):
        return redirect('custom_admin:dashboard')

    client_ip = get_client_ip(request)
    
    # IP engel kontrolü
    max_attempts = getattr(settings, 'ADMIN_MAX_LOGIN_ATTEMPTS', 5)
    lockout_minutes = getattr(settings, 'ADMIN_LOCKOUT_MINUTES', 15)
    
    if LoginAttempt.is_ip_blocked(client_ip, max_attempts, lockout_minutes):
        messages.error(
            request,
            f'Çok fazla başarısız giriş denemesi. Lütfen {lockout_minutes} dakika sonra tekrar deneyin.'
        )
        return render(request, 'custom_admin/login.html', {'form': AdminLoginForm()})

    if request.method == 'POST':
        form = AdminLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            try:
                user = AdminUser.objects.get(username=username, is_active=True)
                if user.check_password(password):
                    # Başarılı giriş
                    request.session['admin_user_id'] = str(user.id)
                    request.session['admin_username'] = user.username
                    request.session['admin_role'] = user.role
                    request.session.set_expiry(3600)  # 1 saat oturum süresi
                    
                    # Son giriş zamanını güncelle
                    user.last_login = timezone.now()
                    user.save(update_fields=['last_login'])
                    
                    # Başarılı giriş kaydı ve eski denemeleri temizle
                    LoginAttempt.record_attempt(client_ip, username, success=True)
                    LoginAttempt.clear_attempts(client_ip)
                    
                    messages.success(request, f'Hoş geldiniz, {user.full_name}!')
                    return redirect('custom_admin:dashboard')
                else:
                    LoginAttempt.record_attempt(client_ip, username, success=False)
                    messages.error(request, 'Kullanıcı adı veya şifre hatalı.')
            except AdminUser.DoesNotExist:
                LoginAttempt.record_attempt(client_ip, username, success=False)
                messages.error(request, 'Kullanıcı adı veya şifre hatalı.')
    else:
        form = AdminLoginForm()

    return render(request, 'custom_admin/login.html', {'form': form})


@admin_login_required
def admin_logout(request):
    """Admin çıkış işlemi"""
    request.session.flush()
    messages.success(request, 'Başarıyla çıkış yaptınız.')
    base = get_admin_base_url()
    return redirect(f'/{base}/login/')


@admin_login_required
@csrf_protect
def change_password(request):
    """Şifre değiştirme"""
    if request.method == 'POST':
        form = PasswordChangeForm(request.POST)
        if form.is_valid():
            if not request.admin_user.check_password(form.cleaned_data['current_password']):
                messages.error(request, 'Mevcut şifreniz hatalı.')
            else:
                request.admin_user.set_password(form.cleaned_data['new_password'])
                request.admin_user.save()
                messages.success(request, 'Şifreniz başarıyla değiştirildi. Lütfen tekrar giriş yapın.')
                request.session.flush()
                base = get_admin_base_url()
                return redirect(f'/{base}/login/')
    else:
        form = PasswordChangeForm()

    return render(request, 'custom_admin/change_password.html', {
        'form': form,
        'admin_user': request.admin_user,
    })


# ==========================================
# Dashboard
# ==========================================

@admin_login_required
def dashboard(request):
    """Ana dashboard sayfası - özet bilgiler"""
    context = {
        'admin_user': request.admin_user,
        'slider_count': SliderImage.objects.count(),
        'service_count': Service.objects.count(),
        'gallery_count': GalleryImage.objects.count(),
        'message_count': ContactMessage.objects.count(),
        'unread_messages': ContactMessage.objects.filter(is_read=False).count(),
        'faq_count': FAQ.objects.count(),
        'recent_messages': ContactMessage.objects.order_by('-created_at')[:5],
    }
    return render(request, 'custom_admin/dashboard.html', context)


# ==========================================
# Kullanıcı Yönetimi (Superadmin)
# ==========================================

@superadmin_required
def user_list(request):
    """Admin kullanıcı listesi"""
    users = AdminUser.objects.all()
    return render(request, 'custom_admin/users/list.html', {
        'users': users,
        'admin_user': request.admin_user,
    })


@superadmin_required
@csrf_protect
def user_create(request):
    """Yeni admin kullanıcı oluşturma"""
    if request.method == 'POST':
        form = AdminUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, f'{user.username} kullanıcısı başarıyla oluşturuldu.')
            return redirect('custom_admin:user_list')
    else:
        form = AdminUserForm()

    return render(request, 'custom_admin/users/form.html', {
        'form': form,
        'title': 'Yeni Kullanıcı Oluştur',
        'admin_user': request.admin_user,
    })


@superadmin_required
@csrf_protect
def user_edit(request, user_id):
    """Admin kullanıcı düzenleme"""
    user = get_object_or_404(AdminUser, id=user_id)

    if request.method == 'POST':
        form = AdminUserForm(request.POST, instance=user)
        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data.get('password')
            if password:
                user.set_password(password)
            user.save()
            messages.success(request, f'{user.username} kullanıcısı güncellendi.')
            return redirect('custom_admin:user_list')
    else:
        form = AdminUserForm(instance=user)

    return render(request, 'custom_admin/users/form.html', {
        'form': form,
        'title': f'{user.username} Düzenle',
        'edit_mode': True,
        'admin_user': request.admin_user,
    })


@superadmin_required
@require_POST
@csrf_protect
def user_delete(request, user_id):
    """Admin kullanıcı silme"""
    user = get_object_or_404(AdminUser, id=user_id)
    
    # Kendini silemez
    if str(user.id) == str(request.admin_user.id):
        messages.error(request, 'Kendinizi silemezsiniz.')
        return redirect('custom_admin:user_list')
    
    username = user.username
    user.delete()
    messages.success(request, f'{username} kullanıcısı silindi.')
    return redirect('custom_admin:user_list')


# ==========================================
# Slider Yönetimi
# ==========================================

@admin_login_required
@permission_required('can_manage_sliders')
def slider_list(request):
    """Slider listesi"""
    sliders = SliderImage.objects.all()
    return render(request, 'custom_admin/sliders/list.html', {
        'sliders': sliders,
        'admin_user': request.admin_user,
    })


@admin_login_required
@permission_required('can_manage_sliders')
@csrf_protect
def slider_create(request):
    """Yeni slider oluşturma"""
    if request.method == 'POST':
        form = SliderForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Slider başarıyla eklendi.')
            return redirect('custom_admin:slider_list')
    else:
        form = SliderForm()

    return render(request, 'custom_admin/sliders/form.html', {
        'form': form,
        'title': 'Yeni Slider Ekle',
        'admin_user': request.admin_user,
    })


@admin_login_required
@permission_required('can_manage_sliders')
@csrf_protect
def slider_edit(request, pk):
    """Slider düzenleme"""
    slider = get_object_or_404(SliderImage, pk=pk)
    if request.method == 'POST':
        form = SliderForm(request.POST, request.FILES, instance=slider)
        if form.is_valid():
            form.save()
            messages.success(request, 'Slider güncellendi.')
            return redirect('custom_admin:slider_list')
    else:
        form = SliderForm(instance=slider)

    return render(request, 'custom_admin/sliders/form.html', {
        'form': form,
        'title': 'Slider Düzenle',
        'edit_mode': True,
        'obj': slider,
        'admin_user': request.admin_user,
    })


@admin_login_required
@permission_required('can_manage_sliders')
@require_POST
@csrf_protect
def slider_delete(request, pk):
    """Slider silme"""
    slider = get_object_or_404(SliderImage, pk=pk)
    slider.delete()
    messages.success(request, 'Slider silindi.')
    return redirect('custom_admin:slider_list')


# ==========================================
# Hizmet Yönetimi
# ==========================================

@admin_login_required
@permission_required('can_manage_services')
def service_list(request):
    """Hizmet listesi"""
    services = Service.objects.all()
    return render(request, 'custom_admin/services/list.html', {
        'services': services,
        'admin_user': request.admin_user,
    })


@admin_login_required
@permission_required('can_manage_services')
@csrf_protect
def service_create(request):
    """Yeni hizmet oluşturma"""
    if request.method == 'POST':
        form = ServiceForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Hizmet başarıyla eklendi.')
            return redirect('custom_admin:service_list')
    else:
        form = ServiceForm()

    return render(request, 'custom_admin/services/form.html', {
        'form': form,
        'title': 'Yeni Hizmet Ekle',
        'admin_user': request.admin_user,
    })


@admin_login_required
@permission_required('can_manage_services')
@csrf_protect
def service_edit(request, pk):
    """Hizmet düzenleme"""
    service = get_object_or_404(Service, pk=pk)
    if request.method == 'POST':
        form = ServiceForm(request.POST, request.FILES, instance=service)
        if form.is_valid():
            form.save()
            messages.success(request, 'Hizmet güncellendi.')
            return redirect('custom_admin:service_list')
    else:
        form = ServiceForm(instance=service)

    return render(request, 'custom_admin/services/form.html', {
        'form': form,
        'title': 'Hizmet Düzenle',
        'edit_mode': True,
        'obj': service,
        'admin_user': request.admin_user,
    })


@admin_login_required
@permission_required('can_manage_services')
@require_POST
@csrf_protect
def service_delete(request, pk):
    """Hizmet silme"""
    service = get_object_or_404(Service, pk=pk)
    service.delete()
    messages.success(request, 'Hizmet silindi.')
    return redirect('custom_admin:service_list')


# ==========================================
# Galeri Yönetimi
# ==========================================

@admin_login_required
@permission_required('can_manage_gallery')
def gallery_list(request):
    """Galeri listesi"""
    images = GalleryImage.objects.all()
    return render(request, 'custom_admin/gallery/list.html', {
        'images': images,
        'admin_user': request.admin_user,
    })


@admin_login_required
@permission_required('can_manage_gallery')
@csrf_protect
def gallery_create(request):
    """Tek galeri resmi ekleme"""
    if request.method == 'POST':
        form = GalleryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Resim başarıyla eklendi.')
            return redirect('custom_admin:gallery_list')
    else:
        form = GalleryForm()

    return render(request, 'custom_admin/gallery/form.html', {
        'form': form,
        'title': 'Yeni Resim Ekle',
        'admin_user': request.admin_user,
    })


@admin_login_required
@permission_required('can_manage_gallery')
@csrf_protect
def gallery_upload_multi(request):
    """Toplu galeri resmi yükleme sayfası (drag & drop)"""
    return render(request, 'custom_admin/gallery/upload_multi.html', {
        'admin_user': request.admin_user,
    })


@admin_login_required
@permission_required('can_manage_gallery')
@csrf_protect
def gallery_edit(request, pk):
    """Galeri resmi düzenleme"""
    image = get_object_or_404(GalleryImage, pk=pk)
    if request.method == 'POST':
        form = GalleryForm(request.POST, request.FILES, instance=image)
        if form.is_valid():
            form.save()
            messages.success(request, 'Resim güncellendi.')
            return redirect('custom_admin:gallery_list')
    else:
        form = GalleryForm(instance=image)

    return render(request, 'custom_admin/gallery/form.html', {
        'form': form,
        'title': 'Resim Düzenle',
        'edit_mode': True,
        'obj': image,
        'admin_user': request.admin_user,
    })


@admin_login_required
@permission_required('can_manage_gallery')
@require_POST
@csrf_protect
def gallery_delete(request, pk):
    """Galeri resmi silme"""
    image = get_object_or_404(GalleryImage, pk=pk)
    image.delete()
    messages.success(request, 'Resim silindi.')
    return redirect('custom_admin:gallery_list')


# ==========================================
# Toplu Dosya Yükleme API
# ==========================================

@admin_login_required
@permission_required('can_manage_gallery')
@require_POST
@csrf_protect
def api_upload_multi(request):
    """
    Toplu dosya yükleme API endpoint'i.
    AJAX ile çoklu dosya alır ve kaydeder.
    JSON response döndürür.
    """
    files = request.FILES.getlist('files')
    if not files:
        return JsonResponse({'success': False, 'error': 'Dosya seçilmedi.'}, status=400)

    uploaded = []
    errors = []
    max_order = GalleryImage.objects.aggregate(
        max_order=Max('order')
    )['max_order'] or 0

    for i, file in enumerate(files):
        # Dosya tipi kontrolü
        allowed_types = ['image/jpeg', 'image/png', 'image/webp', 'image/avif', 'image/gif']
        if file.content_type not in allowed_types:
            errors.append(f'{file.name}: Desteklenmeyen dosya tipi.')
            continue
        
        # Dosya boyutu kontrolü (max 10MB)
        if file.size > 10 * 1024 * 1024:
            errors.append(f'{file.name}: Dosya boyutu 10MB\'dan büyük.')
            continue

        try:
            img = GalleryImage(
                title=file.name.rsplit('.', 1)[0],
                image=file,
                order=max_order + i + 1,
                is_active=True,
            )
            img.save()
            uploaded.append({
                'id': img.id,
                'title': img.title,
                'url': img.image.url,
            })
        except Exception as e:
            errors.append(f'{file.name}: Yükleme hatası.')

    return JsonResponse({
        'success': True,
        'uploaded': uploaded,
        'errors': errors,
        'total_uploaded': len(uploaded),
    })


# ==========================================
# Mesaj Yönetimi
# ==========================================

@admin_login_required
@permission_required('can_manage_messages')
def message_list(request):
    """Mesaj listesi"""
    msgs = ContactMessage.objects.all()
    filter_type = request.GET.get('filter', 'all')
    if filter_type == 'unread':
        msgs = msgs.filter(is_read=False)
    elif filter_type == 'read':
        msgs = msgs.filter(is_read=True)

    return render(request, 'custom_admin/messages/list.html', {
        'messages_list': msgs,
        'filter_type': filter_type,
        'admin_user': request.admin_user,
    })


@admin_login_required
@permission_required('can_manage_messages')
def message_detail(request, pk):
    """Mesaj detayı"""
    msg = get_object_or_404(ContactMessage, pk=pk)
    # Otomatik okundu olarak işaretle
    if not msg.is_read:
        msg.is_read = True
        msg.save(update_fields=['is_read'])

    return render(request, 'custom_admin/messages/detail.html', {
        'msg': msg,
        'admin_user': request.admin_user,
    })


@admin_login_required
@permission_required('can_manage_messages')
@require_POST
@csrf_protect
def message_toggle_read(request, pk):
    """Mesaj okundu/okunmadı durumunu değiştir"""
    msg = get_object_or_404(ContactMessage, pk=pk)
    msg.is_read = not msg.is_read
    msg.save(update_fields=['is_read'])
    return redirect('custom_admin:message_list')


@admin_login_required
@permission_required('can_manage_messages')
@require_POST
@csrf_protect
def message_delete(request, pk):
    """Mesaj silme"""
    msg = get_object_or_404(ContactMessage, pk=pk)
    msg.delete()
    messages.success(request, 'Mesaj silindi.')
    return redirect('custom_admin:message_list')


# ==========================================
# SSS Yönetimi
# ==========================================

@admin_login_required
@permission_required('can_manage_faq')
def faq_list(request):
    """SSS listesi"""
    faqs = FAQ.objects.all()
    return render(request, 'custom_admin/faq/list.html', {
        'faqs': faqs,
        'admin_user': request.admin_user,
    })


@admin_login_required
@permission_required('can_manage_faq')
@csrf_protect
def faq_create(request):
    """Yeni SSS oluşturma"""
    if request.method == 'POST':
        form = FAQForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Soru başarıyla eklendi.')
            return redirect('custom_admin:faq_list')
    else:
        form = FAQForm()

    return render(request, 'custom_admin/faq/form.html', {
        'form': form,
        'title': 'Yeni Soru Ekle',
        'admin_user': request.admin_user,
    })


@admin_login_required
@permission_required('can_manage_faq')
@csrf_protect
def faq_edit(request, pk):
    """SSS düzenleme"""
    faq = get_object_or_404(FAQ, pk=pk)
    if request.method == 'POST':
        form = FAQForm(request.POST, instance=faq)
        if form.is_valid():
            form.save()
            messages.success(request, 'Soru güncellendi.')
            return redirect('custom_admin:faq_list')
    else:
        form = FAQForm(instance=faq)

    return render(request, 'custom_admin/faq/form.html', {
        'form': form,
        'title': 'Soru Düzenle',
        'edit_mode': True,
        'admin_user': request.admin_user,
    })


@admin_login_required
@permission_required('can_manage_faq')
@require_POST
@csrf_protect
def faq_delete(request, pk):
    """SSS silme"""
    faq = get_object_or_404(FAQ, pk=pk)
    faq.delete()
    messages.success(request, 'Soru silindi.')
    return redirect('custom_admin:faq_list')


# ==========================================
# Hakkımızda Yönetimi
# ==========================================

@admin_login_required
@permission_required('can_manage_about')
@csrf_protect
def about_edit(request):
    """Hakkımızda sayfası düzenleme (tek kayıt)"""
    about = AboutUs.objects.first()

    if request.method == 'POST':
        if about:
            form = AboutUsForm(request.POST, request.FILES, instance=about)
        else:
            form = AboutUsForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            messages.success(request, 'Hakkımızda bilgileri güncellendi.')
            return redirect('custom_admin:about_edit')
    else:
        form = AboutUsForm(instance=about) if about else AboutUsForm()

    return render(request, 'custom_admin/about/form.html', {
        'form': form,
        'about': about,
        'admin_user': request.admin_user,
    })
