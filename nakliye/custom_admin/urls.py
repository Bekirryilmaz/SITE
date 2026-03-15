"""
Custom Admin Panel - URLs
Tüm admin paneli URL tanımları
"""

from django.urls import path
from . import views

app_name = 'custom_admin'

urlpatterns = [
    # Kimlik Doğrulama
    path('login/', views.admin_login, name='login'),
    path('logout/', views.admin_logout, name='logout'),
    path('change-password/', views.change_password, name='change_password'),
    
    # Dashboard
    path('', views.dashboard, name='dashboard'),
    
    # Kullanıcı Yönetimi (Superadmin)
    path('users/', views.user_list, name='user_list'),
    path('users/create/', views.user_create, name='user_create'),
    path('users/<uuid:user_id>/edit/', views.user_edit, name='user_edit'),
    path('users/<uuid:user_id>/delete/', views.user_delete, name='user_delete'),
    
    # Slider Yönetimi
    path('sliders/', views.slider_list, name='slider_list'),
    path('sliders/create/', views.slider_create, name='slider_create'),
    path('sliders/<int:pk>/edit/', views.slider_edit, name='slider_edit'),
    path('sliders/<int:pk>/delete/', views.slider_delete, name='slider_delete'),
    
    # Hizmet Yönetimi
    path('services/', views.service_list, name='service_list'),
    path('services/create/', views.service_create, name='service_create'),
    path('services/<int:pk>/edit/', views.service_edit, name='service_edit'),
    path('services/<int:pk>/delete/', views.service_delete, name='service_delete'),
    
    # Galeri Yönetimi
    path('gallery/', views.gallery_list, name='gallery_list'),
    path('gallery/create/', views.gallery_create, name='gallery_create'),
    path('gallery/upload-multi/', views.gallery_upload_multi, name='gallery_upload_multi'),
    path('gallery/<int:pk>/edit/', views.gallery_edit, name='gallery_edit'),
    path('gallery/<int:pk>/delete/', views.gallery_delete, name='gallery_delete'),
    
    # Mesaj Yönetimi
    path('messages/', views.message_list, name='message_list'),
    path('messages/<int:pk>/', views.message_detail, name='message_detail'),
    path('messages/<int:pk>/toggle-read/', views.message_toggle_read, name='message_toggle_read'),
    path('messages/<int:pk>/delete/', views.message_delete, name='message_delete'),
    
    # SSS Yönetimi
    path('faq/', views.faq_list, name='faq_list'),
    path('faq/create/', views.faq_create, name='faq_create'),
    path('faq/<int:pk>/edit/', views.faq_edit, name='faq_edit'),
    path('faq/<int:pk>/delete/', views.faq_delete, name='faq_delete'),
    
    # Hakkımızda Yönetimi
    path('about/', views.about_edit, name='about_edit'),
    
    # Toplu Dosya Yükleme API
    path('api/upload-multi/', views.api_upload_multi, name='api_upload_multi'),
]
