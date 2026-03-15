"""
Custom Admin Panel - Kullanıcı ve Yetki Modelleri
Rol tabanlı erişim kontrolü (RBAC) sistemi
"""

from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from django.utils import timezone
import uuid


class AdminUser(models.Model):
    """
    Özel admin kullanıcı modeli.
    Django'nun built-in User modelinden bağımsız çalışır.
    Şifreler Django'nun hasher sistemi ile güvenli saklanır.
    """
    ROLE_CHOICES = [
        ('superadmin', 'Süper Admin'),
        ('admin', 'Admin'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=50, unique=True, verbose_name="Kullanıcı Adı")
    password_hash = models.CharField(max_length=256, verbose_name="Şifre Hash")
    email = models.EmailField(blank=True, verbose_name="E-posta")
    first_name = models.CharField(max_length=100, blank=True, verbose_name="Ad")
    last_name = models.CharField(max_length=100, blank=True, verbose_name="Soyad")
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='admin', verbose_name="Rol")
    is_active = models.BooleanField(default=True, verbose_name="Aktif")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Oluşturulma Tarihi")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Güncellenme Tarihi")
    last_login = models.DateTimeField(null=True, blank=True, verbose_name="Son Giriş")

    # Yetkiler - her biri ayrı kontrol edilebilir
    can_manage_sliders = models.BooleanField(default=True, verbose_name="Slider Yönetimi")
    can_manage_services = models.BooleanField(default=True, verbose_name="Hizmet Yönetimi")
    can_manage_gallery = models.BooleanField(default=True, verbose_name="Galeri Yönetimi")
    can_manage_messages = models.BooleanField(default=True, verbose_name="Mesaj Yönetimi")
    can_manage_faq = models.BooleanField(default=True, verbose_name="SSS Yönetimi")
    can_manage_about = models.BooleanField(default=True, verbose_name="Hakkımızda Yönetimi")

    class Meta:
        verbose_name = "Admin Kullanıcı"
        verbose_name_plural = "Admin Kullanıcılar"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"

    def set_password(self, raw_password):
        """Şifreyi hashleyerek saklar"""
        self.password_hash = make_password(raw_password)

    def check_password(self, raw_password):
        """Girilen şifreyi hash ile karşılaştırır"""
        return check_password(raw_password, self.password_hash)

    @property
    def is_superadmin(self):
        return self.role == 'superadmin'

    @property
    def full_name(self):
        name = f"{self.first_name} {self.last_name}".strip()
        return name or self.username

    def has_permission(self, permission_name):
        """Belirli bir yetkiyi kontrol eder. Superadmin tüm yetkilere sahiptir."""
        if self.is_superadmin:
            return True
        return getattr(self, permission_name, False)


class LoginAttempt(models.Model):
    """
    Brute-force saldırılarına karşı giriş denemelerini takip eder.
    Belirli sayıda başarısız denemeden sonra IP geçici olarak engellenir.
    """
    ip_address = models.GenericIPAddressField(verbose_name="IP Adresi")
    username = models.CharField(max_length=50, blank=True, verbose_name="Denenen Kullanıcı Adı")
    success = models.BooleanField(default=False, verbose_name="Başarılı")
    attempted_at = models.DateTimeField(auto_now_add=True, verbose_name="Deneme Zamanı")

    class Meta:
        verbose_name = "Giriş Denemesi"
        verbose_name_plural = "Giriş Denemeleri"
        ordering = ['-attempted_at']
        indexes = [
            models.Index(fields=['ip_address', 'attempted_at']),
        ]

    def __str__(self):
        status = "✓" if self.success else "✗"
        return f"{status} {self.ip_address} - {self.username} ({self.attempted_at})"

    @classmethod
    def is_ip_blocked(cls, ip_address, max_attempts=5, lockout_minutes=15):
        """
        IP adresinin engellenip engellenmediğini kontrol eder.
        Son lockout_minutes dakikada max_attempts'ten fazla başarısız deneme varsa True döner.
        """
        cutoff_time = timezone.now() - timezone.timedelta(minutes=lockout_minutes)
        failed_attempts = cls.objects.filter(
            ip_address=ip_address,
            success=False,
            attempted_at__gte=cutoff_time
        ).count()
        return failed_attempts >= max_attempts

    @classmethod
    def record_attempt(cls, ip_address, username='', success=False):
        """Giriş denemesini kayıt altına alır"""
        cls.objects.create(
            ip_address=ip_address,
            username=username,
            success=success
        )

    @classmethod
    def clear_attempts(cls, ip_address):
        """Başarılı girişten sonra IP'nin başarısız denemelerini temizler"""
        cutoff_time = timezone.now() - timezone.timedelta(minutes=30)
        cls.objects.filter(
            ip_address=ip_address,
            success=False,
            attempted_at__gte=cutoff_time
        ).delete()
