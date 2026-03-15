"""
Custom Admin Panel - Form Tanımları
Tüm admin paneli formları burada tanımlıdır.
"""

from django import forms
from .models import AdminUser
from core.models import SliderImage, Service, GalleryImage, ContactMessage, FAQ, AboutUs


# ==========================================
# Kimlik Doğrulama Formları
# ==========================================

class AdminLoginForm(forms.Form):
    """Admin giriş formu"""
    username = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Kullanıcı Adı',
            'autocomplete': 'username',
            'autofocus': True,
        }),
        label='Kullanıcı Adı'
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Şifre',
            'autocomplete': 'current-password',
        }),
        label='Şifre'
    )


class AdminUserForm(forms.ModelForm):
    """Admin kullanıcı oluşturma/düzenleme formu"""
    password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Şifre (boş bırakılırsa değişmez)',
        }),
        label='Şifre',
        help_text='Yeni kullanıcı için zorunlu. Düzenlemede boş bırakılırsa mevcut şifre korunur.'
    )
    password_confirm = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Şifre Tekrar',
        }),
        label='Şifre Tekrar'
    )

    class Meta:
        model = AdminUser
        fields = [
            'username', 'email', 'first_name', 'last_name', 'role', 'is_active',
            'can_manage_sliders', 'can_manage_services', 'can_manage_gallery',
            'can_manage_messages', 'can_manage_faq', 'can_manage_about',
        ]
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'role': forms.Select(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'can_manage_sliders': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'can_manage_services': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'can_manage_gallery': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'can_manage_messages': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'can_manage_faq': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'can_manage_about': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')

        # Yeni kullanıcıda şifre zorunlu
        if not self.instance.pk and not password:
            raise forms.ValidationError('Yeni kullanıcı için şifre zorunludur.')

        # Şifre girilmişse eşleşme kontrolü
        if password and password != password_confirm:
            raise forms.ValidationError('Şifreler eşleşmiyor.')

        # Şifre uzunluk kontrolü
        if password and len(password) < 8:
            raise forms.ValidationError('Şifre en az 8 karakter olmalıdır.')

        return cleaned_data


class PasswordChangeForm(forms.Form):
    """Şifre değiştirme formu"""
    current_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Mevcut Şifre',
        }),
        label='Mevcut Şifre'
    )
    new_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Yeni Şifre',
        }),
        label='Yeni Şifre',
        min_length=8,
    )
    new_password_confirm = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Yeni Şifre Tekrar',
        }),
        label='Yeni Şifre Tekrar'
    )

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password')
        new_password_confirm = cleaned_data.get('new_password_confirm')
        if new_password and new_password != new_password_confirm:
            raise forms.ValidationError('Yeni şifreler eşleşmiyor.')
        return cleaned_data


# ==========================================
# İçerik Yönetim Formları
# ==========================================

class SliderForm(forms.ModelForm):
    """Slider resmi formu"""
    class Meta:
        model = SliderImage
        fields = ['title', 'image', 'order', 'is_active']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Slider Başlığı'}),
            'image': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'order': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['image'].required = False

    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.instance.pk and not self.files.get('image'):
            instance.image = self.Meta.model.objects.get(pk=instance.pk).image
        if commit:
            instance.save()
        return instance


class ServiceForm(forms.ModelForm):
    """Hizmet formu"""
    class Meta:
        model = Service
        fields = ['title', 'short_description', 'description', 'image', 'icon', 'order', 'is_active']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Hizmet Adı'}),
            'short_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Kısa Açıklama'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 6, 'placeholder': 'Detaylı Açıklama'}),
            'image': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'icon': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'fa-truck'}),
            'order': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['image'].required = False

    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.instance.pk and not self.files.get('image'):
            instance.image = self.Meta.model.objects.get(pk=instance.pk).image
        if commit:
            instance.save()
        return instance


class GalleryForm(forms.ModelForm):
    """Galeri resmi formu"""
    class Meta:
        model = GalleryImage
        fields = ['title', 'image', 'order', 'is_active']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Resim Başlığı'}),
            'image': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'order': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['image'].required = False

    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.instance.pk and not self.files.get('image'):
            instance.image = self.Meta.model.objects.get(pk=instance.pk).image
        if commit:
            instance.save()
        return instance


class FAQForm(forms.ModelForm):
    """SSS formu"""
    class Meta:
        model = FAQ
        fields = ['question', 'answer', 'order', 'is_active']
        widgets = {
            'question': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Soru'}),
            'answer': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Cevap'}),
            'order': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class AboutUsForm(forms.ModelForm):
    """Hakkımızda formu"""
    class Meta:
        model = AboutUs
        fields = '__all__'
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'short_content': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'full_content': forms.Textarea(attrs={'class': 'form-control', 'rows': 6}),
            'image': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'logo': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'company_name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'working_hours': forms.TextInput(attrs={'class': 'form-control'}),
            'facebook': forms.URLInput(attrs={'class': 'form-control'}),
            'instagram': forms.URLInput(attrs={'class': 'form-control'}),
            'twitter': forms.URLInput(attrs={'class': 'form-control'}),
            'whatsapp': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['image'].required = False
            self.fields['logo'].required = False

    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.instance.pk:
            original = AboutUs.objects.get(pk=instance.pk)
            if not self.files.get('image') and original.image:
                instance.image = original.image
            if not self.files.get('logo') and original.logo:
                instance.logo = original.logo
        if commit:
            instance.save()
        return instance
