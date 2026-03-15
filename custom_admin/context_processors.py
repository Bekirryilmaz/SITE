"""
Custom Admin Panel - Context Processors
Tüm admin template'lerinde kullanılacak global değişkenler
"""

from core.models import ContactMessage


def admin_context(request):
    """
    Admin panelinde okunmamış mesaj sayısını 
    tüm template'lere otomatik olarak aktarır.
    """
    context = {}
    
    # Sadece admin paneli sayfalarında çalıştır
    if hasattr(request, 'admin_user'):
        context['unread_count'] = ContactMessage.objects.filter(is_read=False).count()
    
    return context
