(function() {
    'use strict';
    
    // Элементы карусели
    let carouselContainer, carouselTrack, slides, indicators, prevBtn, nextBtn;
    let currentSlide = 0;
    let isAnimating = false;
    let autoPlayInterval;
    const slideInterval = 5000; // 5 секунд
    
    // Инициализация карусели коллекции
    function initCarousel() {
        carouselContainer = document.getElementById('collectionCarousel');
        if (!carouselContainer) {
            return false;
        }
        
        carouselTrack = carouselContainer.querySelector('.carousel-track');
        slides = carouselContainer.querySelectorAll('.carousel-slide');
        indicators = carouselContainer.querySelectorAll('.indicator');
        prevBtn = carouselContainer.querySelector('.carousel-nav.prev');
        nextBtn = carouselContainer.querySelector('.carousel-nav.next');
        
        if (slides.length < 2) {
            hideNavigation();
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
        
        return true;
    }
    
    // Скрыть навигацию если всего 1 слайд
    function hideNavigation() {
        if (prevBtn) prevBtn.style.display = 'none';
        if (nextBtn) nextBtn.style.display = 'none';
        const indicatorsContainer = carouselContainer.querySelector('.carousel-indicators');
        if (indicatorsContainer) indicatorsContainer.style.display = 'none';
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
                e.stopPropagation();
                prevSlide();
            });
        }
        
        if (nextBtn) {
            nextBtn.addEventListener('click', (e) => {
                e.preventDefault();
                e.stopPropagation();
                nextSlide();
            });
        }
        
        // Индикаторы
        indicators.forEach((indicator, index) => {
            indicator.addEventListener('click', (e) => {
                e.preventDefault();
                e.stopPropagation();
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
            indicator.setAttribute('aria-label', `Изображение ${index + 1} из ${slides.length}`);
        });
        
        if (prevBtn) {
            prevBtn.setAttribute('aria-label', 'Предыдущее изображение');
        }
        
        if (nextBtn) {
            nextBtn.setAttribute('aria-label', 'Следующее изображение');
        }
    }
    
    // Предзагрузка изображений для карусели
    function preloadCarouselImages() {
        const slides = document.querySelectorAll('.carousel-slide');
        const images = [];
        
        slides.forEach(slide => {
            const background = slide.style.backgroundImage;
            if (background) {
                const url = background.replace(/url\(['"]?(.*?)['"]?\)/, '$1');
                images.push(url);
            }
        });
        
        images.forEach(url => {
            const img = new Image();
            img.src = url;
        });
    }
    
    // Анимация появления статистики
    function animateStats() {
        const statNumbers = document.querySelectorAll('.stat-number');
        
        statNumbers.forEach(stat => {
            const text = stat.textContent;
            const numberMatch = text.match(/\d+/);
            
            if (numberMatch) {
                const finalValue = parseInt(numberMatch[0]);
                if (isNaN(finalValue)) return;
                
                let currentValue = 0;
                const increment = finalValue / 30; // 30 кадров анимации
                const duration = 1000; // 1 секунда
                const interval = duration / 30;
                
                const originalText = text;
                
                const timer = setInterval(() => {
                    currentValue += increment;
                    if (currentValue >= finalValue) {
                        stat.textContent = originalText.replace(numberMatch[0], finalValue);
                        clearInterval(timer);
                    } else {
                        stat.textContent = originalText.replace(numberMatch[0], Math.floor(currentValue));
                    }
                }, interval);
            }
        });
    }
    
    // Ленивая загрузка изображений картин
    function setupLazyLoading() {
        const artworkImages = document.querySelectorAll('.collection-artwork-image[data-src]');
        
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
            
            artworkImages.forEach(img => imageObserver.observe(img));
        } else {
            // Fallback для старых браузеров
            artworkImages.forEach(img => {
                const src = img.getAttribute('data-src');
                if (src) {
                    img.src = src;
                    img.removeAttribute('data-src');
                }
            });
        }
    }
    
    // Инициализация при загрузке страницы
    function init() {
        
        // Инициализация карусели
        if (initCarousel()) {
            // Предзагрузка изображений карусели
            setTimeout(preloadCarouselImages, 1000);
        }
        
        // Анимация статистики
        animateStats();
        
        // Ленивая загрузка изображений картин
        setupLazyLoading();
        
        // Добавление эффектов для карточек при скролле
        setupScrollAnimations();
    }
    
    // Анимация карточек при скролле
    function setupScrollAnimations() {
        const artworkCards = document.querySelectorAll('.collection-artwork-card');
        
        if ('IntersectionObserver' in window) {
            const observer = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        entry.target.style.opacity = '1';
                        entry.target.style.transform = 'translateY(0)';
                    }
                });
            }, {
                threshold: 0.1,
                rootMargin: '50px'
            });
            
            artworkCards.forEach((card, index) => {
                card.style.opacity = '0';
                card.style.transform = 'translateY(30px)';
                card.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
                card.style.transitionDelay = (index * 0.1) + 's';
                
                setTimeout(() => {
                    observer.observe(card);
                }, 100);
            });
        }
    }
    
    // Инициализация при загрузке DOM
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
    
    // Экспорт функций для глобального доступа
    window.CollectionCarousel = {
        nextSlide,
        prevSlide,
        goToSlide,
        resetAutoPlay
    };
    
})();