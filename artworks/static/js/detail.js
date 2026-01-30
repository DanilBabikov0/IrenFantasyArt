(function() {
    'use strict';
    
    // Элементы DOM
    let mainImage, modalImage, thumbnails, shareButton;
    let currentImageIndex = 0;
    
    // Предзагрузка изображений
    function preloadImages() {
        // Проверяем, есть ли миниатюры
        const thumbnailsCollection = document.querySelectorAll('.thumbnail');
        if (!thumbnailsCollection || thumbnailsCollection.length === 0) {
            return;
        }
        
        thumbnailsCollection.forEach(thumbnail => {
            const imageUrl = thumbnail.getAttribute('data-image-url');
            if (imageUrl) {
                const img = new Image();
                img.src = imageUrl;
            }
        });
    }
    
    // Настройка галереи изображений
    function setupImageGallery() {
        // Получаем элементы после загрузки DOM
        mainImage = document.getElementById('mainImage');
        modalImage = document.getElementById('modalImage');
        thumbnails = document.querySelectorAll('.thumbnail');
        
        if (!thumbnails || thumbnails.length === 0) {
            return;
        }
        
        // Устанавливаем обработчики для миниатюр
        thumbnails.forEach((thumbnail, index) => {
            thumbnail.addEventListener('click', function() {
                changeImage(index);
            });
            
            // Предзагрузка при наведении
            thumbnail.addEventListener('mouseenter', function() {
                const imageUrl = this.getAttribute('data-image-url');
                if (imageUrl) {
                    const img = new Image();
                    img.src = imageUrl;
                }
            });
        });
        
        // Инициализируем текущий индекс
        const activeThumbnail = document.querySelector('.thumbnail.active');
        if (activeThumbnail) {
            currentImageIndex = Array.from(thumbnails).indexOf(activeThumbnail);
        }
        
        // Навигация клавишами
        document.addEventListener('keydown', function(e) {
            if (document.activeElement.tagName === 'INPUT' || 
                document.activeElement.tagName === 'TEXTAREA' ||
                document.activeElement.tagName === 'SELECT') {
                return;
            }
            
            switch(e.key) {
                case 'ArrowLeft':
                    e.preventDefault();
                    navigateImages(-1);
                    break;
                case 'ArrowRight':
                    e.preventDefault();
                    navigateImages(1);
                    break;
                case 'Escape':
                    // Закрыть модальное окно, если оно открыто
                    const openModal = document.querySelector('.modal.show');
                    if (openModal) {
                        const modalInstance = bootstrap.Modal.getInstance(openModal);
                        if (modalInstance) {
                            modalInstance.hide();
                        }
                    }
                    break;
            }
        });
        
        // Настраиваем свайпы для мобильных
        setupSwipe();
    }
    
    // Смена изображения
    function changeImage(index) {
        if (!thumbnails || index < 0 || index >= thumbnails.length) {
            return;
        }
        
        const thumbnail = thumbnails[index];
        const imageUrl = thumbnail.getAttribute('data-image-url');
        
        if (!imageUrl) {
            return;
        }
        
        // Обновляем основное изображение
        if (mainImage) {
            mainImage.src = imageUrl;
            mainImage.alt = thumbnail.alt || 'Изображение картины';
            
            // Добавляем эффект перехода
            mainImage.style.opacity = '0.7';
            setTimeout(() => {
                mainImage.style.opacity = '1';
            }, 150);
        }
        
        // Обновляем изображение в модальном окне
        if (modalImage) {
            modalImage.src = imageUrl;
            modalImage.alt = thumbnail.alt || 'Изображение картины';
        }
        
        // Обновляем активный класс
        thumbnails.forEach(img => img.classList.remove('active'));
        thumbnail.classList.add('active');
        
        currentImageIndex = index;
    }
    
    // Навигация по изображениям
    function navigateImages(direction) {
        if (!thumbnails || thumbnails.length === 0) return;
        
        let newIndex = currentImageIndex + direction;
        
        if (newIndex < 0) newIndex = thumbnails.length - 1;
        if (newIndex >= thumbnails.length) newIndex = 0;
        
        changeImage(newIndex);
    }
    
    // Настройка свайпов для мобильных устройств
    function setupSwipe() {
        if (!mainImage) return;
        
        let startX = 0;
        let endX = 0;
        const threshold = 50;
        
        mainImage.addEventListener('touchstart', function(e) {
            if (e.touches.length === 1) {
                startX = e.touches[0].clientX;
            }
        }, { passive: true });
        
        mainImage.addEventListener('touchend', function(e) {
            if (e.changedTouches.length === 1) {
                endX = e.changedTouches[0].clientX;
                const diff = startX - endX;
                
                if (Math.abs(diff) > threshold) {
                    if (diff > 0) {
                        navigateImages(1); // Свайп влево -> следующее
                    } else {
                        navigateImages(-1); // Свайп вправо -> предыдущее
                    }
                }
            }
        }, { passive: true });
    }
    
    // Настройка кнопки "Поделиться"
    function setupShareButton() {
        shareButton = document.getElementById('shareButton');
        if (!shareButton) {
            return;
        }
        
        shareButton.addEventListener('click', function(e) {
            e.preventDefault();
            shareArtwork();
        });
    }
    
    // Функция расшаривания
    function shareArtwork() {
        const shareData = {
            title: document.title,
            text: 'Посмотрите эту картину на IrenFantasyArt',
            url: window.location.href,
        };
        
        // Используем Web Share API, если поддерживается
        if (navigator.share) {
            navigator.share(shareData)
                .then(() => console.log('Успешно поделились'))
                .catch((error) => {
                    // Если пользователь отменил - это нормально
                    if (error.name !== 'AbortError') {
                        console.log('Ошибка при расшаривании:', error);
                        showShareModal();
                    }
                });
        } else {
            // Fallback: показываем модальное окно
            showShareModal();
        }
    }
    
    // Показать модальное окно расшаривания
    function showShareModal() {
        const shareModalElement = document.getElementById('shareModal');
        if (!shareModalElement) {
            return;
        }
        
        const shareModal = new bootstrap.Modal(shareModalElement);
        shareModal.show();
    }
    
    // Копирование ссылки в буфер обмена
    window.copyToClipboard = function() {
        const shareUrl = document.getElementById('shareUrl');
        if (!shareUrl) return;
        
        shareUrl.select();
        shareUrl.setSelectionRange(0, 99999);
        
        try {
            const successful = document.execCommand('copy');
            if (successful) {
                // Визуальный фидбэк
                const copyBtn = shareUrl.nextElementSibling;
                if (copyBtn) {
                    const originalHTML = copyBtn.innerHTML;
                    copyBtn.innerHTML = '<i class="bi bi-check"></i>';
                    copyBtn.classList.remove('btn-outline-secondary');
                    copyBtn.classList.add('btn-success');
                    
                    setTimeout(() => {
                        copyBtn.innerHTML = originalHTML;
                        copyBtn.classList.remove('btn-success');
                        copyBtn.classList.add('btn-outline-secondary');
                    }, 2000);
                }
            }
        } catch (err) {
            // Альтернативный способ для современных браузеров
            if (navigator.clipboard && navigator.clipboard.writeText) {
                navigator.clipboard.writeText(shareUrl.value)
                    .then(() => {
                        const copyBtn = shareUrl.nextElementSibling;
                        if (copyBtn) {
                            const originalHTML = copyBtn.innerHTML;
                            copyBtn.innerHTML = '<i class="bi bi-check"></i>';
                            copyBtn.classList.remove('btn-outline-secondary');
                            copyBtn.classList.add('btn-success');
                            
                            setTimeout(() => {
                                copyBtn.innerHTML = originalHTML;
                                copyBtn.classList.remove('btn-success');
                                copyBtn.classList.add('btn-outline-secondary');
                            }, 2000);
                        }
                    })
                    .catch(err => console.error('Ошибка копирования через Clipboard API:', err));
            }
        }
    };
    
    // Настройка модального окна для увеличенного изображения
    function setupImageModal() {
        const imageModalElement = document.getElementById('imageModal');
        if (!imageModalElement) {
            return;
        }
        
        const modal = new bootstrap.Modal(imageModalElement);
        const modalImage = document.getElementById('modalImage');
        
        // При открытии модального окна обновляем изображение
        imageModalElement.addEventListener('show.bs.modal', function() {
            if (modalImage && mainImage) {
                modalImage.src = mainImage.src;
                modalImage.alt = mainImage.alt;
                
                // Подгоняем размер модального окна под изображение
                adjustModalSize();
            }
            
            // Настройка свайпов в модальном окне
            setupModalSwipe();
            
            // Навигация стрелками в модальном окне
            document.addEventListener('keydown', handleModalKeydown);
        });
        
        // При закрытии убираем обработчики
        imageModalElement.addEventListener('hidden.bs.modal', function() {
            document.removeEventListener('keydown', handleModalKeydown);
            
            // Возвращаем фокус на кнопку зума
            const zoomBtn = document.querySelector('.zoom-btn');
            if (zoomBtn) {
                setTimeout(() => zoomBtn.focus(), 100);
            }
        });
        
        // Обработчик нажатия клавиш в модальном окне
        function handleModalKeydown(e) {
            if (e.key === 'ArrowLeft') {
                e.preventDefault();
                navigateImages(-1);
            } else if (e.key === 'ArrowRight') {
                e.preventDefault();
                navigateImages(1);
            }
        }
    }
    
    // Подгонка размера модального окна под изображение
    function adjustModalSize() {
        const modalImage = document.getElementById('modalImage');
        const modalDialog = document.querySelector('#imageModal .modal-dialog');
        
        if (!modalImage || !modalDialog) return;
        
        // Сброс стилей
        modalDialog.style.maxWidth = '';
        modalDialog.style.margin = '';
        
        // Ждем загрузки изображения
        if (modalImage.complete) {
            updateModalSize();
        } else {
            modalImage.onload = updateModalSize;
        }
        
        function updateModalSize() {
            const imgWidth = modalImage.naturalWidth;
            const imgHeight = modalImage.naturalHeight;
            const windowWidth = window.innerWidth;
            const windowHeight = window.innerHeight;
            
            // Ограничиваем максимальный размер
            const maxWidth = Math.min(imgWidth, windowWidth * 0.9);
            const maxHeight = Math.min(imgHeight, windowHeight * 0.8);
            
            // Вычисляем соотношение сторон
            const aspectRatio = imgWidth / imgHeight;
            
            let finalWidth, finalHeight;
            
            if (imgWidth > maxWidth || imgHeight > maxHeight) {
                if (maxWidth / aspectRatio <= maxHeight) {
                    finalWidth = maxWidth;
                    finalHeight = maxWidth / aspectRatio;
                } else {
                    finalHeight = maxHeight;
                    finalWidth = maxHeight * aspectRatio;
                }
            } else {
                finalWidth = imgWidth;
                finalHeight = imgHeight;
            }
            
            // Устанавливаем размеры
            modalDialog.style.maxWidth = finalWidth + 'px';
            modalDialog.style.margin = 'auto';
        }
    }
    
    // Настройка свайпов в модальном окне
    function setupModalSwipe() {
        const modalBody = document.querySelector('#imageModal .modal-body');
        if (!modalBody) return;
        
        let startX = 0;
        let endX = 0;
        const threshold = 50;
        
        modalBody.addEventListener('touchstart', function(e) {
            if (e.touches.length === 1) {
                startX = e.touches[0].clientX;
            }
        }, { passive: true });
        
        modalBody.addEventListener('touchend', function(e) {
            if (e.changedTouches.length === 1) {
                endX = e.changedTouches[0].clientX;
                const diff = startX - endX;
                
                if (Math.abs(diff) > threshold) {
                    if (diff > 0) {
                        navigateImages(1); // Свайп влево -> следующее
                    } else {
                        navigateImages(-1); // Свайп вправо -> предыдущее
                    }
                }
            }
        }, { passive: true });
    }
    
    // Инициализация всех функций
    function init() {
        // Настройка галереи
        setupImageGallery();
        
        // Настройка кнопки "Поделиться"
        setupShareButton();
        
        // Настройка модального окна
        setupImageModal();
        
        // Предзагрузка изображений (после настройки галереи)
        setTimeout(preloadImages, 500);
    }
    
    // Инициализация при загрузке DOM
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        // DOM уже загружен
        init();
    }
    
})();