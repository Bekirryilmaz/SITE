"""
Custom Admin Panel - Güvenlik Middleware'leri
IP kısıtlama ve admin route maskeleme
"""

from django.http import Http404
from django.conf import settings


def get_client_ip(request):
    """
    İstemcinin gerçek IP adresini döndürür.
    Proxy arkasındaysa X-Forwarded-For header'ından alır.
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR', '0.0.0.0')


class AdminIPRestrictionMiddleware:
    """
    Admin paneline IP bazlı erişim kısıtlaması.
    
    settings.py'de ADMIN_ALLOWED_IPS listesi tanımlıysa,
    sadece bu IP'lerden gelen isteklere izin verir.
    Liste boşsa veya tanımlı değilse tüm IP'lere izin verir.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        admin_route = getattr(settings, 'ADMIN_PANEL_ROUTE', 'yonetim-paneli-gizli')
        allowed_ips = getattr(settings, 'ADMIN_ALLOWED_IPS', [])
        
        # Sadece admin route'unda ve IP listesi tanımlıysa kontrol et
        if request.path.startswith(f'/{admin_route}/') and allowed_ips:
            client_ip = get_client_ip(request)
            if client_ip not in allowed_ips:
                # 404 maskesi - admin panelinin varlığını gizle
                raise Http404
        
        return self.get_response(request)


class AdminRouteMaskMiddleware:
    """
    /admin/ gibi bilinen admin rotalarını 404 ile maskeler.
    Saldırganların standart admin URL'lerini denemesini engeller.
    """
    
    # Maskelenecek bilinen admin rotaları
    BLOCKED_ROUTES = [
        '/admin/',
        '/admin/login/',
        '/wp-admin/',
        '/wp-login.php',
        '/administrator/',
        '/panel/',
        '/dashboard/',
        '/login/',
        '/yonetici/',
    ]

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path.lower()
        for route in self.BLOCKED_ROUTES:
            if path.startswith(route):
                raise Http404
        
        return self.get_response(request)
