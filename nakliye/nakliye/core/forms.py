from django import forms
from .models import ContactMessage, Service


# Sabit konu seçenekleri
SUBJECT_CHOICES = [
    ('', 'Konu Seçiniz *'),
    ('evden_eve', 'Evden Eve Nakliyat'),
    ('sehirler_arasi', 'Şehirler Arası Nakliyat'),
    ('ofis', 'Ofis Taşımacılığı'),
    ('paketleme', 'Paketleme Hizmeti'),
    ('mobilya', 'Mobilya Montajı'),
]


class ContactForm(forms.ModelForm):
    subject = forms.ChoiceField(
        choices=SUBJECT_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-select',
            'required': True
        })
    )
    
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'phone', 'subject', 'room_count', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Adınız Soyadınız *',
                'required': True
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-input',
                'placeholder': 'E-Mail Adresiniz'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Telefon Numaranız *',
                'required': True
            }),
            'room_count': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-textarea',
                'placeholder': 'Mesajınız *',
                'rows': 5,
                'required': True
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['room_count'].choices = [('', 'Oda Sayısı Seçiniz *')] + list(ContactMessage.ROOM_CHOICES)
        self.fields['phone'].required = True
