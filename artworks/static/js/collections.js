(function() {
    'use strict';
    
    // Элементы карусели
    let carouselContainer, carouselTrack, slides, indicators, prevBtn, nextBtn;
    let currentSlide = 0;
    let isAnimating = false;
    let autoPlayInterval;
    const slideInterval = 5000; // 5 секунд
    
    // Инициализация карусели
    function initCarousel() {
        carouselContainer = document.getElementById('collectionsCarousel');
        if (!carouselContainer) {
            return false;
        }
        
        carouselTrack = carouselContainer.querySelector('.carousel-track');
        slides = carouselContainer.querySelectorAll('.carousel-slide');
        indicators = carouselContainer.querySelectorAll('.indicator');
        prevBtn = carouselContainer.querySelector('.carousel-nav.prev');
        nextBtn = carouselContainer.querySelector('.carousel-nav.next');
        
        if (slides.length < 2) {
            return false;
        }
        
        // Устанавливаем начальный слайд
        updateCarousel();
        
        // Настройка навигации
        setupNavigation();
        
        // Автопрокрутка
        startAutoPlay();
        
        // Пауза при наведении
        setupHoverPause();
        
        // Адаптация к изменению размера окна
        setupResizeHandler();
        
        return true;
    }
    
    // Обновление позиции карусели
    function updateCarousel() {
        if (!carouselTrack || !slides.length) return;
        
        // Обновляем позицию трека
        carouselTrack.style.transform = `translateX(-${currentSlide * 100}%)`;
        
        // Обновляем активные классы
        slides.forEach((slide, index) => {
            slide.classList.toggle('active', index === currentSlide);
        });
        
        // Обновляем индикаторы
        if (indicators.length) {
            indicators.forEach((indicator, index) => {
                indicator.classList.toggle('active', index === currentSlide);
            });
        }
        
        // Обновляем ARIA атрибуты
        updateAriaAttributes();
    }
    
    // Переход к конкретному слайду
    function goToSlide(index) {
        if (isAnimating || index < 0 || index >= slides.length) return;
        
        isAnimating = true;
        currentSlide = index;
        
        updateCarousel();
        
        // Сбрасываем таймер автопрокрутки
        resetAutoPlay();
        
        // Снимаем блокировку анимации после перехода
        setTimeout(() => {
            isAnimating = false;
        }, 800);
    }
    
    // Переход к следующему слайду
    function nextSlide() {
        const nextIndex = (currentSlide + 1) % slides.length;
        goToSlide(nextIndex);
    }
    
    // Переход к предыдущему слайду
    function prevSlide() {
        const prevIndex = (currentSlide - 1 + slides.length) % slides.length;
        goToSlide(prevIndex);
    }
    
    // Настройка навигации
    function setupNavigation() {
        // Кнопки вперед/назад
        if (prevBtn) {
            prevBtn.addEventListener('click', (e) => {
                e.preventDefault();
                prevSlide();
            });
        }
        
        if (nextBtn) {
            nextBtn.addEventListener('click', (e) => {
                e.preventDefault();
                nextSlide();
            });
        }
        
        // Индикаторы
        indicators.forEach((indicator, index) => {
            indicator.addEventListener('click', (e) => {
                e.preventDefault();
                goToSlide(index);
            });
        });
        
        // Навигация клавишами
        document.addEventListener('keydown', (e) => {
            if (!carouselContainer || document.activeElement.tagName === 'INPUT') return;
            
            switch(e.key) {
                case 'ArrowLeft':
                    e.preventDefault();
                    prevSlide();
                    break;
                case 'ArrowRight':
                    e.preventDefault();
                    nextSlide();
                    break;
                case 'Home':
                    e.preventDefault();
                    goToSlide(0);
                    break;
                case 'End':
                    e.preventDefault();
                    goToSlide(slides.length - 1);
                    break;
            }
        });
        
        // Свайпы для мобильных устройств
        setupSwipeGestures();
    }
    
    // Настройка свайпов
    function setupSwipeGestures() {
        if (!carouselTrack) return;
        
        let startX = 0;
        let endX = 0;
        const threshold = 50;
        
        carouselTrack.addEventListener('touchstart', (e) => {
            startX = e.touches[0].clientX;
        }, { passive: true });
        
        carouselTrack.addEventListener('touchmove', (e) => {
            endX = e.touches[0].clientX;
        }, { passive: true });
        
        carouselTrack.addEventListener('touchend', () => {
            const diff = startX - endX;
            
            if (Math.abs(diff) > threshold) {
                if (diff > 0) {
                    nextSlide(); // Свайп влево -> следующий
                } else {
                    prevSlide(); // Свайп вправо -> предыдущий
                }
            }
        }, { passive: true });
    }
    
    // Автопрокрутка
    function startAutoPlay() {
        if (slides.length < 2) return;
        
        autoPlayInterval = setInterval(nextSlide, slideInterval);
    }
    
    function resetAutoPlay() {
        if (autoPlayInterval) {
            clearInterval(autoPlayInterval);
            startAutoPlay();
        }
    }
    
    // Пауза при наведении
    function setupHoverPause() {
        if (!carouselContainer) return;
        
        carouselContainer.addEventListener('mouseenter', () => {
            if (autoPlayInterval) {
                clearInterval(autoPlayInterval);
                autoPlayInterval = null;
            }
        });
        
        carouselContainer.addEventListener('mouseleave', () => {
            if (!autoPlayInterval && slides.length > 1) {
                startAutoPlay();
            }
        });
    }
    
    // Обработчик изменения размера окна
    function setupResizeHandler() {
        let resizeTimeout;
        
        window.addEventListener('resize', () => {
            clearTimeout(resizeTimeout);
            resizeTimeout = setTimeout(() => {
                // Принудительное обновление позиции карусели
                carouselTrack.style.transform = `translateX(-${currentSlide * 100}%)`;
            }, 250);
        });
    }
    
    // Обновление ARIA атрибутов для доступности
    function updateAriaAttributes() {
        slides.forEach((slide, index) => {
            slide.setAttribute('aria-hidden', index !== currentSlide);
            slide.setAttribute('tabindex', index === currentSlide ? '0' : '-1');
            
            if (index === currentSlide) {
                slide.setAttribute('aria-live', 'polite');
            } else {
                slide.removeAttribute('aria-live');
            }
        });
        
        indicators.forEach((indicator, index) => {
            indicator.setAttribute('aria-current', index === currentSlide ? 'true' : 'false');
            indicator.setAttribute('aria-label', `Слайд ${index + 1} из ${slides.length}`);
        });
        
        if (prevBtn) {
            prevBtn.setAttribute('aria-label', 'Предыдущий слайд');
        }
        
        if (nextBtn) {
            nextBtn.setAttribute('aria-label', 'Следующий слайд');
        }
    }
    
    // Предзагрузка изображений для карусели
    function preloadCarouselImages() {
        const images = carouselContainer.querySelectorAll('img[data-src]');
        
        images.forEach(img => {
            const src = img.getAttribute('data-src');
            if (src) {
                const preloadImg = new Image();
                preloadImg.src = src;
                
                preloadImg.onload = () => {
                    img.src = src;
                    img.removeAttribute('data-src');
                };
            }
        });
    }
    
    // Инициализация при загрузке страницы
    function init() {
        if (initCarousel()) {
            setTimeout(preloadCarouselImages, 1000);
        }
        
        animateStats();
        
        setupLazyLoading();
    }
    
    function animateStats() {
        const statNumbers = document.querySelectorAll('.collections-stat-number');
        
        statNumbers.forEach(stat => {
            const finalValue = parseInt(stat.textContent);
            if (isNaN(finalValue)) return;
            
            let currentValue = 0;
            const increment = finalValue / 50; // 50 кадров анимации
            const duration = 1500; // 1.5 секунды
            const interval = duration / 50;
            
            const timer = setInterval(() => {
                currentValue += increment;
                if (currentValue >= finalValue) {
                    stat.textContent = finalValue.toLocaleString();
                    clearInterval(timer);
                } else {
                    stat.textContent = Math.floor(currentValue).toLocaleString();
                }
            }, interval);
        });
    }
    
    // Ленивая загрузка изображений коллекций
    function setupLazyLoading() {
        const collectionImages = document.querySelectorAll('.collection-image[data-src]');
        
        if ('IntersectionObserver' in window) {
            const imageObserver = new IntersectionObserver((entries, observer) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        const img = entry.target;
                        const src = img.getAttribute('data-src');
                        
                        if (src) {
                            img.src = src;
                            img.removeAttribute('data-src');
                            img.classList.add('loaded');
                        }
                        
                        observer.unobserve(img);
                    }
                });
            }, {
                rootMargin: '100px',
                threshold: 0.1
            });
            
            collectionImages.forEach(img => imageObserver.observe(img));
        } else {
            // Fallback для старых браузеров
            collectionImages.forEach(img => {
                const src = img.getAttribute('data-src');
                if (src) {
                    img.src = src;
                    img.removeAttribute('data-src');
                }
            });
        }
    }
    
    // Инициализация при загрузке DOM
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
    
    // Экспорт функций для глобального доступа (если нужно)
    window.CollectionsCarousel = {
        nextSlide,
        prevSlide,
        goToSlide,
        resetAutoPlay
    };
    
})();