/**
 * Custom Admin Panel - JavaScript
 * Sidebar toggle, dropdown, alert otomatik kapanma
 */

document.addEventListener('DOMContentLoaded', function() {
    // ==========================================
    // Sidebar Toggle (Mobile)
    // ==========================================
    const menuToggle = document.getElementById('menuToggle');
    const sidebar = document.getElementById('sidebar');
    const sidebarClose = document.getElementById('sidebarClose');
    const sidebarOverlay = document.getElementById('sidebarOverlay');

    function openSidebar() {
        sidebar?.classList.add('open');
        sidebarOverlay?.classList.add('show');
        document.body.style.overflow = 'hidden';
    }

    function closeSidebar() {
        sidebar?.classList.remove('open');
        sidebarOverlay?.classList.remove('show');
        document.body.style.overflow = '';
    }

    menuToggle?.addEventListener('click', openSidebar);
    sidebarClose?.addEventListener('click', closeSidebar);
    sidebarOverlay?.addEventListener('click', closeSidebar);

    // ESC ile sidebar kapat
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') {
            closeSidebar();
            closeDropdown();
        }
    });

    // ==========================================
    // User Dropdown
    // ==========================================
    const userDropdown = document.getElementById('userDropdown');
    const dropdownToggle = userDropdown?.querySelector('.user-dropdown-toggle');
    const dropdownMenu = userDropdown?.querySelector('.user-dropdown-menu');

    function closeDropdown() {
        dropdownMenu?.classList.remove('show');
    }

    dropdownToggle?.addEventListener('click', function(e) {
        e.stopPropagation();
        dropdownMenu?.classList.toggle('show');
    });

    document.addEventListener('click', function(e) {
        if (!userDropdown?.contains(e.target)) {
            closeDropdown();
        }
    });

    // ==========================================
    // Alert Auto-dismiss (5 saniye sonra kapat)
    // ==========================================
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(function(alert) {
        setTimeout(function() {
            alert.style.opacity = '0';
            alert.style.transform = 'translateY(-10px)';
            setTimeout(function() {
                alert.remove();
            }, 300);
        }, 5000);
    });

    // ==========================================
    // Confirm Dialogs
    // ==========================================
    // Delete butonları için onsubmit zaten HTML'de tanımlı

    // ==========================================
    // File Input Enhancement
    // ==========================================
    const fileInputs = document.querySelectorAll('input[type="file"]:not([id="fileInput"])');
    fileInputs.forEach(function(input) {
        input.addEventListener('change', function() {
            const preview = this.closest('.form-group')?.querySelector('.file-preview');
            if (preview && this.files[0]) {
                const file = this.files[0];
                if (file.type.startsWith('image/')) {
                    preview.innerHTML = '';
                    const img = document.createElement('img');
                    img.src = URL.createObjectURL(file);
                    img.className = 'preview-image';
                    img.onload = function() { URL.revokeObjectURL(this.src); };
                    preview.appendChild(img);
                }
            }
        });
    });
});
