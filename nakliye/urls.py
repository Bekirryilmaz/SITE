"""
URL configuration for nakliye project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

# Admin paneli route'u settings'den okunur (güvenlik için)
ADMIN_ROUTE = getattr(settings, 'ADMIN_PANEL_ROUTE', 'gizli-yonetim-x7k9m2')

urlpatterns = [
    # Eski /admin/ rotası kaldırıldı - güvenlik için
    # Yeni admin paneli gizli, yapılandırılabilir route ile çalışır
    path(f'{ADMIN_ROUTE}/', include('custom_admin.urls')),
    path('', include('core.urls')),
    path('sitemap.xml', TemplateView.as_view(template_name='sitemap.xml', content_type='application/xml')),
    path('robots.txt', TemplateView.as_view(template_name='robots.txt', content_type='text/plain')),
]

# Media dosyaları için (hem development hem production)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Development modunda static dosyaları da Django sunar
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
