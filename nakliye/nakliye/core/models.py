from django.db import models

# Slider Resimleri
class SliderImage(models.Model):
    title = models.CharField(max_length=200, verbose_name="Başlık", blank=True)
    image = models.FileField(upload_to='slider/', verbose_name="Resim")
    order = models.PositiveIntegerField(default=0, verbose_name="Sıra")
    is_active = models.BooleanField(default=True, verbose_name="Aktif")

    class Meta:
        verbose_name = "Slider Resmi"
        verbose_name_plural = "Slider Resimleri"
        ordering = ['order']

    def __str__(self):
        return self.title or f"Slider {self.id}"


# Hizmetler
class Service(models.Model):
    title = models.CharField(max_length=200, verbose_name="Hizmet Adı")
    short_description = models.TextField(verbose_name="Kısa Açıklama", max_length=300)
    description = models.TextField(verbose_name="Detaylı Açıklama")
    image = models.FileField(upload_to='services/', verbose_name="Resim")
    icon = models.CharField(max_length=50, verbose_name="İkon (Font Awesome)", default="fa-truck")
    order = models.PositiveIntegerField(default=0, verbose_name="Sıra")
    is_active = models.BooleanField(default=True, verbose_name="Aktif")

    class Meta:
        verbose_name = "Hizmet"
        verbose_name_plural = "Hizmetler"
        ordering = ['order']

    def __str__(self):
        return self.title


# Galeri
class GalleryImage(models.Model):
    title = models.CharField(max_length=200, verbose_name="Başlık", blank=True)
    image = models.FileField(upload_to='gallery/', verbose_name="Resim")
    order = models.PositiveIntegerField(default=0, verbose_name="Sıra")
    is_active = models.BooleanField(default=True, verbose_name="Aktif")

    class Meta:
        verbose_name = "Galeri Resmi"
        verbose_name_plural = "Galeri Resimleri"
        ordering = ['order']

    def __str__(self):
        return self.title or f"Galeri {self.id}"


# İletişim Mesajları
class ContactMessage(models.Model):
    ROOM_CHOICES = [
        ('1+0', '1+0 (Stüdyo)'),
        ('1+1', '1+1'),
        ('2+1', '2+1'),
        ('3+1', '3+1'),
        ('4+1', '4+1'),
        ('5+1', '5+1 ve üzeri'),
        ('villa', 'Villa'),
        ('ofis', 'Ofis'),
    ]
    
    SUBJECT_CHOICES = [
        ('evden_eve', 'Evden Eve Nakliyat'),
        ('sehirler_arasi', 'Şehirler Arası Nakliyat'),
        ('ofis', 'Ofis Taşımacılığı'),
        ('paketleme', 'Paketleme Hizmeti'),
        ('mobilya', 'Mobilya Montajı'),
    ]

    name = models.CharField(max_length=100, verbose_name="Ad Soyad")
    email = models.EmailField(verbose_name="E-Mail", blank=True)
    phone = models.CharField(max_length=20, verbose_name="Telefon", blank=True)
    subject = models.CharField(max_length=50, choices=SUBJECT_CHOICES, verbose_name="Konu", default='evden_eve')
    room_count = models.CharField(max_length=20, choices=ROOM_CHOICES, verbose_name="Oda Sayısı")
    message = models.TextField(verbose_name="Mesaj")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Gönderim Tarihi")
    is_read = models.BooleanField(default=False, verbose_name="Okundu")

    class Meta:
        verbose_name = "İletişim Mesajı"
        verbose_name_plural = "İletişim Mesajları"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.subject}"


# Sıkça Sorulan Sorular (Taşınma Rehberi)
class FAQ(models.Model):
    question = models.CharField(max_length=500, verbose_name="Soru")
    answer = models.TextField(verbose_name="Cevap")
    order = models.PositiveIntegerField(default=0, verbose_name="Sıra")
    is_active = models.BooleanField(default=True, verbose_name="Aktif")

    class Meta:
        verbose_name = "Sık Sorulan Soru"
        verbose_name_plural = "Sık Sorulan Sorular"
        ordering = ['order']

    def __str__(self):
        return self.question[:50]


# Hakkımızda
class AboutUs(models.Model):
    title = models.CharField(max_length=200, verbose_name="Başlık")
    short_content = models.TextField(verbose_name="Kısa İçerik (Anasayfa için)", max_length=500)
    full_content = models.TextField(verbose_name="Tam İçerik")
    image = models.FileField(upload_to='about/', verbose_name="Resim", blank=True, null=True)
    logo = models.FileField(upload_to='logo/', verbose_name="Logo", blank=True, null=True)
    
    # Firma Bilgileri
    company_name = models.CharField(max_length=200, verbose_name="Firma Adı", default="Nakliye Firması")
    phone = models.CharField(max_length=20, verbose_name="Telefon", blank=True)
    email = models.EmailField(verbose_name="E-Mail", blank=True)
    address = models.TextField(verbose_name="Adres", blank=True)
    working_hours = models.CharField(max_length=100, verbose_name="Çalışma Saatleri", blank=True)
    
    # Sosyal Medya
    facebook = models.URLField(blank=True, verbose_name="Facebook")
    instagram = models.URLField(blank=True, verbose_name="Instagram")
    twitter = models.URLField(blank=True, verbose_name="Twitter")
    whatsapp = models.CharField(max_length=20, blank=True, verbose_name="WhatsApp")

    class Meta:
        verbose_name = "Hakkımızda"
        verbose_name_plural = "Hakkımızda"

    def __str__(self):
        return self.title
