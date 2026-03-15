from django.contrib import admin
from .models import SliderImage, Service, GalleryImage, ContactMessage, FAQ, AboutUs


# Admin site başlığı
admin.site.site_header = "Nakliye Yönetim Paneli"
admin.site.site_title = "Nakliye Admin"
admin.site.index_title = "Hoş Geldiniz"


@admin.register(SliderImage)
class SliderImageAdmin(admin.ModelAdmin):
    list_display = ['title', 'order', 'is_active']
    list_editable = ['order', 'is_active']
    list_filter = ['is_active']
    ordering = ['order']


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['title', 'icon', 'order', 'is_active']
    list_editable = ['order', 'is_active']
    list_filter = ['is_active']
    search_fields = ['title', 'description']
    ordering = ['order']


@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ['title', 'order', 'is_active']
    list_editable = ['order', 'is_active']
    list_filter = ['is_active']
    ordering = ['order']


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone', 'subject', 'room_count', 'created_at', 'is_read']
    list_filter = ['is_read', 'subject', 'room_count', 'created_at']
    search_fields = ['name', 'email', 'phone', 'message']
    readonly_fields = ['name', 'email', 'phone', 'subject', 'room_count', 'message', 'created_at']
    list_editable = ['is_read']
    ordering = ['-created_at']
    
    def has_add_permission(self, request):
        return False


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ['question', 'order', 'is_active']
    list_editable = ['order', 'is_active']
    list_filter = ['is_active']
    search_fields = ['question', 'answer']
    ordering = ['order']


@admin.register(AboutUs)
class AboutUsAdmin(admin.ModelAdmin):
    list_display = ['title', 'company_name', 'phone', 'email']
    
    def has_add_permission(self, request):
        # Sadece 1 kayıt olsun
        if AboutUs.objects.exists():
            return False
        return True
    
    def has_delete_permission(self, request, obj=None):
        return False
