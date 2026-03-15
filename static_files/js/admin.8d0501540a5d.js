/**
 * NAKLIYE ADMIN PANELİ - JAVASCRIPT
 * Sidebar toggle ve mobil menü işlevselliği
 */

document.addEventListener('DOMContentLoaded', function() {
    
    // === SIDEBAR TOGGLE ===
    const sidebar = document.getElementById('adminSidebar');
    const sidebarToggle = document.getElementById('sidebarToggle');
    const sidebarOverlay = document.getElementById('sidebarOverlay');
    const branding = document.querySelector('.admin-branding');
    
    // Toggle fonksiyonu
    function toggleSidebar() {
        if (sidebar) {
            sidebar.classList.toggle('active');
        }
        if (sidebarOverlay) {
            sidebarOverlay.classList.toggle('active');
        }
    }
    
    // Sidebar toggle butonu
    if (sidebarToggle) {
        sidebarToggle.addEventListener('click', toggleSidebar);
    }
    
    // Overlay'e tıklayınca kapat
    if (sidebarOverlay) {
        sidebarOverlay.addEventListener('click', toggleSidebar);
    }
    
    // Branding'e tıklayınca mobilde sidebar aç (hamburger menu gibi)
    if (branding && window.innerWidth <= 992) {
        branding.addEventListener('click', function(e) {
            if (window.innerWidth <= 992) {
                e.preventDefault();
                toggleSidebar();
            }
        });
    }
    
    // === AKTİF MENÜ ÖĞESİNİ VURGULA ===
    const currentPath = window.location.pathname;
    const menuLinks = document.querySelectorAll('.menu-link');
    
    menuLinks.forEach(link => {
        const href = link.getAttribute('href');
        if (href && currentPath.includes(href) && href !== '/admin/') {
            link.classList.add('active');
        } else if (href === '/admin/' && currentPath === '/admin/') {
            link.classList.add('active');
        }
    });
    
    // === PENCERE BOYUTU DEĞİŞİMİNDE ===
    window.addEventListener('resize', function() {
        if (window.innerWidth > 992) {
            // Masaüstünde sidebar'ı her zaman göster
            if (sidebar) {
                sidebar.classList.remove('active');
            }
            if (sidebarOverlay) {
                sidebarOverlay.classList.remove('active');
            }
        }
    });
    
    // === TABLO SATIRLARINI TIKLANABİLİR YAP ===
    const tableRows = document.querySelectorAll('#result_list tbody tr');
    tableRows.forEach(row => {
        const link = row.querySelector('th a, td a');
        if (link) {
            row.style.cursor = 'pointer';
            row.addEventListener('click', function(e) {
                // Checkbox'a tıklandıysa yoksay
                if (e.target.type === 'checkbox') return;
                
                // Eğer tıklanan bir link değilse ilk linki aç
                if (e.target.tagName !== 'A') {
                    window.location.href = link.href;
                }
            });
        }
    });
    
    // === MESAJLARI OTOMATİK GİZLE ===
    const messages = document.querySelectorAll('.messagelist li');
    messages.forEach(msg => {
        setTimeout(() => {
            msg.style.opacity = '0';
            msg.style.transform = 'translateY(-10px)';
            setTimeout(() => {
                msg.remove();
            }, 300);
        }, 5000); // 5 saniye sonra gizle
    });
    
    // === FORM VALIDATION UYARILARI ===
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const requiredFields = form.querySelectorAll('[required]');
            let hasError = false;
            
            requiredFields.forEach(field => {
                if (!field.value.trim()) {
                    hasError = true;
                    field.style.borderColor = 'var(--admin-danger)';
                    field.style.boxShadow = '0 0 0 3px rgba(239, 68, 68, 0.1)';
                } else {
                    field.style.borderColor = '';
                    field.style.boxShadow = '';
                }
            });
            
            if (hasError) {
                e.preventDefault();
                alert('Lütfen zorunlu alanları doldurun.');
            }
        });
    });
    
    // === KEYBOARD SHORTCUTS ===
    document.addEventListener('keydown', function(e) {
        // Ctrl+S ile kaydet
        if ((e.ctrlKey || e.metaKey) && e.key === 's') {
            const saveBtn = document.querySelector('input[name="_save"]');
            if (saveBtn) {
                e.preventDefault();
                saveBtn.click();
            }
        }
        
        // ESC ile sidebar'ı kapat (mobilde)
        if (e.key === 'Escape' && sidebar && sidebar.classList.contains('active')) {
            toggleSidebar();
        }
    });
    
    // === CONFIRM DELETE ===
    const deleteLinks = document.querySelectorAll('.deletelink, a[href*="delete"]');
    deleteLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            if (!confirm('Bu öğeyi silmek istediğinizden emin misiniz?')) {
                e.preventDefault();
            }
        });
    });
    
    console.log('Admin Panel JS yüklendi.');
});
