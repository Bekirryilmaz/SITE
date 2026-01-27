from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Service


class StaticViewSitemap(Sitemap):
    """Statik sayfalar için sitemap"""
    priority = 0.8
    changefreq = 'weekly'
    protocol = 'https'

    def items(self):
        return ['home', 'services', 'about', 'gallery', 'contact', 'guide']

    def location(self, item):
        return reverse(item)
    
    def priority(self, item):
        # Anasayfa en yüksek öncelik
        if item == 'home':
            return 1.0
        elif item in ['services', 'contact']:
            return 0.9
        elif item in ['about', 'gallery']:
            return 0.8
        else:
            return 0.7


class ServiceSitemap(Sitemap):
    """Hizmetler için sitemap"""
    changefreq = 'monthly'
    priority = 0.7
    protocol = 'https'

    def items(self):
        return Service.objects.filter(is_active=True)

    def location(self, obj):
        return f'/hizmetlerimiz/?service={obj.id}'
