"""
Superadmin oluşturma management command'ı.

Kullanım:
    python manage.py create_superadmin

İlk kurulumda superadmin hesabı oluşturmak için kullanılır.
"""

from django.core.management.base import BaseCommand
from custom_admin.models import AdminUser
import getpass


class Command(BaseCommand):
    help = 'İlk superadmin kullanıcısını oluşturur'

    def add_arguments(self, parser):
        parser.add_argument('--username', type=str, help='Kullanıcı adı')
        parser.add_argument('--email', type=str, help='E-posta adresi', default='')
        parser.add_argument('--noinput', action='store_true', help='Etkileşimsiz mod')

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING('\n=== Süper Admin Oluşturma ===\n'))

        # Mevcut superadmin kontrolü
        existing = AdminUser.objects.filter(role='superadmin').count()
        if existing > 0:
            self.stdout.write(
                self.style.WARNING(f'Dikkat: Zaten {existing} süper admin hesabı mevcut.')
            )
            if not options['noinput']:
                confirm = input('Yine de yeni bir süper admin oluşturmak istiyor musunuz? (e/h): ')
                if confirm.lower() != 'e':
                    self.stdout.write(self.style.ERROR('İptal edildi.'))
                    return

        # Kullanıcı bilgilerini al
        if options['noinput']:
            username = options['username']
            if not username:
                self.stdout.write(self.style.ERROR('--noinput modunda --username zorunludur.'))
                return
            password = 'admin123456'  # Varsayılan şifre (hemen değiştirilmeli)
            email = options['email']
        else:
            username = options['username'] or input('Kullanıcı adı: ').strip()
            
            if not username:
                self.stdout.write(self.style.ERROR('Kullanıcı adı boş olamaz.'))
                return

            # Kullanıcı adı benzersizlik kontrolü
            if AdminUser.objects.filter(username=username).exists():
                self.stdout.write(self.style.ERROR(f'"{username}" kullanıcı adı zaten kullanılıyor.'))
                return

            email = options['email'] or input('E-posta (isteğe bağlı): ').strip()

            # Şifre al
            while True:
                password = getpass.getpass('Şifre (min 8 karakter): ')
                if len(password) < 8:
                    self.stdout.write(self.style.ERROR('Şifre en az 8 karakter olmalıdır.'))
                    continue
                password_confirm = getpass.getpass('Şifre tekrar: ')
                if password != password_confirm:
                    self.stdout.write(self.style.ERROR('Şifreler eşleşmiyor.'))
                    continue
                break

        # Superadmin oluştur
        try:
            admin_user = AdminUser(
                username=username,
                email=email,
                role='superadmin',
                is_active=True,
                first_name='Süper',
                last_name='Admin',
            )
            admin_user.set_password(password)
            admin_user.save()

            self.stdout.write(self.style.SUCCESS(
                f'\n✓ Süper admin başarıyla oluşturuldu!'
            ))
            self.stdout.write(f'  Kullanıcı adı: {username}')
            self.stdout.write(f'  Rol: Süper Admin')
            self.stdout.write(f'  E-posta: {email or "Belirtilmedi"}')
            
            from django.conf import settings
            admin_route = getattr(settings, 'ADMIN_PANEL_ROUTE', 'gizli-yonetim-x7k9m2')
            self.stdout.write(self.style.WARNING(
                f'\n  Giriş adresi: /{admin_route}/login/'
            ))
            self.stdout.write('')

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Hata: {str(e)}'))
