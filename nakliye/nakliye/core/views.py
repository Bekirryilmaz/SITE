from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .models import SliderImage, Service, GalleryImage, FAQ, AboutUs, ContactMessage
from .forms import ContactForm


def get_about_info():
    """Tüm sayfalarda kullanılacak firma bilgilerini döndürür"""
    return AboutUs.objects.first()


def home(request):
    """Anasayfa"""
    context = {
        'sliders': SliderImage.objects.filter(is_active=True)[:10],
        'services': Service.objects.filter(is_active=True)[:6],
        'about': get_about_info(),
    }
    return render(request, 'home.html', context)


def services(request):
    """Hizmetlerimiz Sayfası"""
    all_services = Service.objects.filter(is_active=True)
    
    # Seçili hizmet (varsayılan olarak ilk hizmet)
    service_id = request.GET.get('service')
    if service_id:
        selected_service = get_object_or_404(Service, id=service_id, is_active=True)
    else:
        selected_service = all_services.first()
    
    context = {
        'services': all_services,
        'selected_service': selected_service,
        'about': get_about_info(),
    }
    return render(request, 'services.html', context)


def about(request):
    """Hakkımızda Sayfası"""
    context = {
        'about': get_about_info(),
    }
    return render(request, 'about.html', context)


def gallery(request):
    """Galeri Sayfası"""
    context = {
        'images': GalleryImage.objects.filter(is_active=True),
        'about': get_about_info(),
    }
    return render(request, 'gallery.html', context)


def contact(request):
    """İletişim Sayfası"""
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact_message = form.save()
            
            # E-posta bildirimi gönder
            try:
                subject_display = dict(ContactMessage.SUBJECT_CHOICES).get(contact_message.subject, contact_message.subject)
                
                email_subject = f'Yeni İletişim Formu: {contact_message.name}'
                email_body = f"""Yeni bir iletişim formu dolduruldu:

👤 Ad Soyad: {contact_message.name}
📞 Telefon: {contact_message.phone}
📧 E-Mail: {contact_message.email or 'Belirtilmedi'}
📝 Konu: {subject_display}
🏠 Oda Sayısı: {contact_message.room_count}

💬 Mesaj:
{contact_message.message}

---
Bu mesaj Ay Yıldız Nakliyat web sitesinden gönderilmiştir.
Gönderim Tarihi: {contact_message.created_at.strftime('%d.%m.%Y %H:%M')}
"""
                
                send_mail(
                    subject=email_subject,
                    message=email_body,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[settings.NOTIFICATION_EMAIL],
                    fail_silently=True,
                )
            except Exception as e:
                # E-posta gönderilemezse bile form kaydedilsin
                pass
            
            messages.success(request, 'Mesajınız başarıyla gönderildi. En kısa sürede size dönüş yapacağız.')
            return redirect('contact')
        else:
            messages.error(request, 'Lütfen formu doğru şekilde doldurunuz.')
    else:
        form = ContactForm()
    
    context = {
        'form': form,
        'about': get_about_info(),
    }
    return render(request, 'contact.html', context)


def guide(request):
    """Taşınma Rehberi (SSS) Sayfası"""
    context = {
        'faqs': FAQ.objects.filter(is_active=True),
        'about': get_about_info(),
    }
    return render(request, 'guide.html', context)
