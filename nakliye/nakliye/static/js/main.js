/**
 * NAKLIYE FİRMASI - ANA JAVASCRIPT DOSYASI
 */

document.addEventListener('DOMContentLoaded', function() {
    
    // =====================
    // MOBILE MENU TOGGLE (Animated Hamburger)
    // =====================
    const mobileMenuBtn = document.getElementById('mobileMenuBtn');
    const mainNav = document.getElementById('mainNav');
    
    if (mobileMenuBtn && mainNav) {
        mobileMenuBtn.addEventListener('click', function() {
            this.classList.toggle('active');
            mainNav.classList.toggle('active');
        });
        
        // Menü dışına tıklayınca kapat
        document.addEventListener('click', function(e) {
            if (!mainNav.contains(e.target) && !mobileMenuBtn.contains(e.target)) {
                mainNav.classList.remove('active');
                mobileMenuBtn.classList.remove('active');
            }
        });
    }
    
    // =====================
    // MOBILE DROPDOWN - SWIPE TO TOGGLE
    // =====================
    const dropdownItems = document.querySelectorAll('.has-dropdown');
    let touchStartY = 0;
    let touchEndY = 0;
    
    dropdownItems.forEach(item => {
        const link = item.querySelector('a');
        const dropdown = item.querySelector('.dropdown-menu');
        
        // Desktop hover efekti zaten CSS ile çalışıyor
        
        // Mobile için touch events
        if (dropdown) {
            let startY = 0;
            
            link.addEventListener('touchstart', function(e) {
                startY = e.touches[0].clientY;
            }, { passive: true });
            
            link.addEventListener('touchend', function(e) {
                if (window.innerWidth <= 768) {
                    const endY = e.changedTouches[0].clientY;
                    const diff = startY - endY;
                    
                    // Yukarı kaydırma (swipe up) - dropdown aç
                    if (diff > 30) {
                        e.preventDefault();
                        item.classList.add('active');
                    }
                    // Aşağı kaydırma (swipe down) - dropdown kapat
                    else if (diff < -30) {
                        e.preventDefault();
                        item.classList.remove('active');
                    }
                    // Normal tıklama
                    else {
                        e.preventDefault();
                        item.classList.toggle('active');
                    }
                }
            });
        }
        
        // Desktop için click
        link.addEventListener('click', function(e) {
            if (window.innerWidth <= 768) {
                e.preventDefault();
                item.classList.toggle('active');
            }
        });
    });
    
    // =====================
    // SLIDER
    // =====================
    const sliderWrapper = document.getElementById('sliderWrapper');
    const sliderDots = document.getElementById('sliderDots');
    const prevBtn = document.getElementById('sliderPrev');
    const nextBtn = document.getElementById('sliderNext');
    
    if (sliderWrapper) {
        const slides = sliderWrapper.querySelectorAll('.slide');
        const dots = sliderDots ? sliderDots.querySelectorAll('.slider-dot') : [];
        let currentSlide = 0;
        let slideInterval;
        const slideCount = slides.length;
        
        // Slider'ı güncelle
        function updateSlider() {
            sliderWrapper.style.transform = `translateX(-${currentSlide * 100}%)`;
            
            // Dot'ları güncelle
            dots.forEach((dot, index) => {
                dot.classList.toggle('active', index === currentSlide);
            });
        }
        
        // Sonraki slide
        function nextSlide() {
            currentSlide = (currentSlide + 1) % slideCount;
            updateSlider();
        }
        
        // Önceki slide
        function prevSlide() {
            currentSlide = (currentSlide - 1 + slideCount) % slideCount;
            updateSlider();
        }
        
        // Otomatik slider
        function startAutoSlide() {
            slideInterval = setInterval(nextSlide, 5000);
        }
        
        function stopAutoSlide() {
            clearInterval(slideInterval);
        }
        
        // Event listeners
        if (nextBtn) {
            nextBtn.addEventListener('click', function() {
                stopAutoSlide();
                nextSlide();
                startAutoSlide();
            });
        }
        
        if (prevBtn) {
            prevBtn.addEventListener('click', function() {
                stopAutoSlide();
                prevSlide();
                startAutoSlide();
            });
        }
        
        // Dot'lara tıklama
        dots.forEach((dot, index) => {
            dot.addEventListener('click', function() {
                stopAutoSlide();
                currentSlide = index;
                updateSlider();
                startAutoSlide();
            });
        });
        
        // Touch/Swipe desteği
        let touchStartX = 0;
        let touchEndX = 0;
        
        sliderWrapper.addEventListener('touchstart', function(e) {
            touchStartX = e.changedTouches[0].screenX;
        }, { passive: true });
        
        sliderWrapper.addEventListener('touchend', function(e) {
            touchEndX = e.changedTouches[0].screenX;
            handleSwipe();
        }, { passive: true });
        
        function handleSwipe() {
            const swipeThreshold = 50;
            const diff = touchStartX - touchEndX;
            
            if (Math.abs(diff) > swipeThreshold) {
                stopAutoSlide();
                if (diff > 0) {
                    nextSlide();
                } else {
                    prevSlide();
                }
                startAutoSlide();
            }
        }
        
        // Slider başlat
        startAutoSlide();
        
        // Sayfa görünürlüğü değiştiğinde
        document.addEventListener('visibilitychange', function() {
            if (document.hidden) {
                stopAutoSlide();
            } else {
                startAutoSlide();
            }
        });
    }
    
    // =====================
    // SERVICES CAROUSEL
    // =====================
    const servicesWrapper = document.getElementById('servicesWrapper');
    const servicesPrev = document.getElementById('servicesPrev');
    const servicesNext = document.getElementById('servicesNext');
    
    if (servicesWrapper && servicesPrev && servicesNext) {
        const serviceCards = servicesWrapper.querySelectorAll('.service-card');
        let currentServiceIndex = 0;
        const totalServices = serviceCards.length;
        
        function updateServicesCarousel() {
            // Mobilde tek tek, masaüstünde çoklu göster
            const isMobile = window.innerWidth <= 768;
            
            if (isMobile) {
                // Mobilde tek kart göster
                servicesWrapper.style.transform = `translateX(-${currentServiceIndex * 100}%)`;
            } else {
                // Masaüstünde kaydırmalı (her kart 340px)
                const cardWidth = 340;
                const containerWidth = servicesWrapper.parentElement.offsetWidth;
                const visibleCards = Math.floor(containerWidth / cardWidth);
                const maxIndex = Math.max(0, totalServices - visibleCards);
                
                currentServiceIndex = Math.min(currentServiceIndex, maxIndex);
                servicesWrapper.style.transform = `translateX(-${currentServiceIndex * cardWidth}px)`;
            }
        }
        
        servicesNext.addEventListener('click', function() {
            const isMobile = window.innerWidth <= 768;
            if (isMobile) {
                currentServiceIndex = (currentServiceIndex + 1) % totalServices;
            } else {
                const cardWidth = 340;
                const containerWidth = servicesWrapper.parentElement.offsetWidth;
                const visibleCards = Math.floor(containerWidth / cardWidth);
                const maxIndex = Math.max(0, totalServices - visibleCards);
                currentServiceIndex = Math.min(currentServiceIndex + 1, maxIndex);
            }
            updateServicesCarousel();
        });
        
        servicesPrev.addEventListener('click', function() {
            const isMobile = window.innerWidth <= 768;
            if (isMobile) {
                currentServiceIndex = (currentServiceIndex - 1 + totalServices) % totalServices;
            } else {
                currentServiceIndex = Math.max(0, currentServiceIndex - 1);
            }
            updateServicesCarousel();
        });
        
        // Pencere boyutu değiştiğinde güncelle
        window.addEventListener('resize', function() {
            currentServiceIndex = 0;
            updateServicesCarousel();
        });
        
        // Touch swipe desteği (mobil)
        let touchStartX = 0;
        let touchEndX = 0;
        
        servicesWrapper.addEventListener('touchstart', function(e) {
            touchStartX = e.changedTouches[0].screenX;
        }, { passive: true });
        
        servicesWrapper.addEventListener('touchend', function(e) {
            touchEndX = e.changedTouches[0].screenX;
            const diff = touchStartX - touchEndX;
            
            if (Math.abs(diff) > 50) {
                if (diff > 0) {
                    servicesNext.click();
                } else {
                    servicesPrev.click();
                }
            }
        }, { passive: true });
        
        // Başlangıçta güncelle
        updateServicesCarousel();
    }
    
    // =====================
    // ALERT CLOSE
    // =====================
    document.querySelectorAll('.alert-close').forEach(button => {
        button.addEventListener('click', function() {
            this.closest('.alert').remove();
        });
    });
    
    // =====================
    // SCROLL TO TOP (HEADER FIX)
    // =====================
    const header = document.querySelector('.header');
    const footer = document.querySelector('.footer');
    let lastScrollY = window.scrollY;
    
    if (header) {
        window.addEventListener('scroll', function() {
            if (window.scrollY > 100) {
                header.style.boxShadow = '0 4px 20px rgba(0, 0, 0, 0.15)';
            } else {
                header.style.boxShadow = '0 4px 6px -1px rgba(0, 0, 0, 0.1)';
            }
            
            lastScrollY = window.scrollY;
        });
    }
    
    // =====================
    // SMOOTH SCROLL
    // =====================
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            const href = this.getAttribute('href');
            if (href !== '#' && href.length > 1) {
                e.preventDefault();
                const target = document.querySelector(href);
                if (target) {
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            }
        });
    });
    
    // =====================
    // FORM VALIDATION (İsteğe bağlı ekstra)
    // =====================
    const contactForm = document.querySelector('.contact-form-wrapper form');
    if (contactForm) {
        contactForm.addEventListener('submit', function(e) {
            const name = this.querySelector('[name="name"]');
            const message = this.querySelector('[name="message"]');
            const roomCount = this.querySelector('[name="room_count"]');
            
            let isValid = true;
            
            // Ad kontrolü
            if (name && name.value.trim() === '') {
                isValid = false;
                name.style.borderColor = 'red';
            } else if (name) {
                name.style.borderColor = '';
            }
            
            // Mesaj kontrolü
            if (message && message.value.trim() === '') {
                isValid = false;
                message.style.borderColor = 'red';
            } else if (message) {
                message.style.borderColor = '';
            }
            
            // Oda sayısı kontrolü
            if (roomCount && roomCount.value === '') {
                isValid = false;
                roomCount.style.borderColor = 'red';
            } else if (roomCount) {
                roomCount.style.borderColor = '';
            }
            
            if (!isValid) {
                e.preventDefault();
                alert('Lütfen zorunlu alanları doldurunuz.');
            }
        });
    }
    
    // =====================
    // ANIMATION ON SCROLL (Basit)
    // =====================
    function animateOnScroll() {
        const elements = document.querySelectorAll('.service-card, .faq-item, .about-content');
        
        elements.forEach(el => {
            const rect = el.getBoundingClientRect();
            const isVisible = rect.top < window.innerHeight - 100;
            
            if (isVisible) {
                el.style.opacity = '1';
                el.style.transform = 'translateY(0)';
            }
        });
    }
    
    // İlk yükleme için stil ayarla
    document.querySelectorAll('.service-card, .faq-item').forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(20px)';
        el.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
    });
    
    // Scroll event
    window.addEventListener('scroll', animateOnScroll);
    // İlk yüklemede de çalıştır
    setTimeout(animateOnScroll, 100);
    
});

// =====================
// WHATSAPP FORM GÖNDERİM FONKSİYONU
// Anasayfa ve İletişim sayfası formları için ortak fonksiyon
// =====================
function sendWhatsAppMessage(event, formType) {
    event.preventDefault();
    
    // WhatsApp hedef numarası
    const whatsappNumber = '905438092323';
    
    let name, phone, email, subject, roomCount, message;
    
    // Form tipine göre elemanları seç
    if (formType === 'home') {
        name = document.getElementById('home_name').value.trim();
        phone = document.getElementById('home_phone').value.trim();
        email = document.getElementById('home_email').value.trim();
        subject = document.getElementById('home_subject').value;
        roomCount = document.getElementById('home_room_count').value;
        message = document.getElementById('home_message').value.trim();
    } else if (formType === 'contact') {
        name = document.getElementById('contact_name').value.trim();
        phone = document.getElementById('contact_phone').value.trim();
        email = document.getElementById('contact_email').value.trim();
        subject = document.getElementById('contact_subject').value;
        roomCount = document.getElementById('contact_room_count').value;
        message = document.getElementById('contact_message').value.trim();
    }
    
    // Zorunlu alan kontrolü
    let errors = [];
    if (!name) errors.push('Ad Soyad');
    if (!phone) errors.push('Telefon');
    if (!subject) errors.push('Konu');
    if (!roomCount) errors.push('Oda Sayısı');
    if (!message) errors.push('Mesaj');
    
    if (errors.length > 0) {
        alert('Lütfen şu alanları doldurun:\n• ' + errors.join('\n• '));
        return false;
    }
    
    // WhatsApp mesaj metnini oluştur
    let whatsappMessage = `🏠 *YENİ NAKLİYAT TALEBİ*\n\n`;
    whatsappMessage += `👤 *Ad Soyad:* ${name}\n`;
    whatsappMessage += `📱 *Telefon:* ${phone}\n`;
    if (email) {
        whatsappMessage += `📧 *E-Mail:* ${email}\n`;
    }
    whatsappMessage += `📋 *Konu:* ${subject}\n`;
    whatsappMessage += `🚪 *Oda Sayısı:* ${roomCount}\n`;
    whatsappMessage += `\n💬 *Mesaj:*\n${message}`;
    
    // URL encode
    const encodedMessage = encodeURIComponent(whatsappMessage);
    
    // WhatsApp linkini oluştur ve aç
    const whatsappUrl = `https://wa.me/${whatsappNumber}?text=${encodedMessage}`;
    
    // Yeni sekmede WhatsApp'ı aç
    window.open(whatsappUrl, '_blank');
    
    // Başarı mesajı
    alert('WhatsApp açılıyor... Mesajınızı göndermek için "Gönder" butonuna tıklayın.');
    
    return false;
}
