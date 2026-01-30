document.addEventListener('DOMContentLoaded', function() {
    const filterForm = document.getElementById('filter-form');
    const sortSelect = document.getElementById('sort-select');
    const perPageSelect = document.getElementById('per-page-select');
    const orderField = document.getElementById('order-field');
    const perPageField = document.getElementById('per-page-field');
    const viewGridBtn = document.getElementById('view-grid-btn');
    const viewListBtn = document.getElementById('view-list-btn');
    const artworksGrid = document.getElementById('artworks-grid-view');
    const resetFiltersBtn = document.getElementById('reset-filters');
    const clearAllFiltersBtn = document.getElementById('clear-all-filters');
    const resetFiltersNoResults = document.getElementById('reset-filters-no-results');
    const filterToggleBtn = document.getElementById('filter-toggle');
    const filterCard = document.querySelector('.filter-card');
    const showAvailableOnlyCheckbox = document.getElementById('show_available_only');

    if (!filterForm) return;
    
    // Переключение вида (сетка/список)
    if (viewGridBtn && viewListBtn && artworksGrid) {
        viewGridBtn.addEventListener('click', function() {
            this.classList.add('active');
            viewListBtn.classList.remove('active');
            artworksGrid.className = 'row row-cols-1 row-cols-sm-2 row-cols-lg-3 g-4';
        });
        
        viewListBtn.addEventListener('click', function() {
            this.classList.add('active');
            viewGridBtn.classList.remove('active');
            artworksGrid.className = 'row row-cols-1 g-4';
        });
    }
    
    // Обработка чекбокса "Только доступные"
    if (showAvailableOnlyCheckbox) {
        showAvailableOnlyCheckbox.addEventListener('change', function() {
            const statusCheckboxes = filterForm.querySelectorAll('input[name="status"]');
            
            if (this.checked) {
                // Отмечаем только "available" и снимаем остальные
                statusCheckboxes.forEach(checkbox => {
                    if (checkbox.value === 'available') {
                        checkbox.checked = true;
                    } else {
                        checkbox.checked = false;
                    }
                });
            } else {
                // Если сняли галочку "Только доступные", снимаем все статусы
                statusCheckboxes.forEach(checkbox => {
                    checkbox.checked = false;
                });
            }
            
            updateFilterCount();
        });
    }
    
    // При изменении статусов проверяем состояние галочки "Только доступные"
    const statusCheckboxes = filterForm.querySelectorAll('input[name="status"]');
    if (statusCheckboxes.length > 0) {
        statusCheckboxes.forEach(checkbox => {
            checkbox.addEventListener('change', function() {
                updateAvailableOnlyCheckbox();
                updateFilterCount();
            });
        });
    }
    
    // Функция для обновления состояния галочки "Только доступные"
    function updateAvailableOnlyCheckbox() {
        if (!showAvailableOnlyCheckbox) return;
        
        const checkedStatuses = Array.from(statusCheckboxes)
            .filter(cb => cb.checked)
            .map(cb => cb.value);
        
        // Галочка отмечена, если выбран только статус 'available'
        showAvailableOnlyCheckbox.checked = 
            checkedStatuses.length === 1 && checkedStatuses[0] === 'available';
    }
    
    // Сортировка - обновляем скрытое поле и отправляем форму
    if (sortSelect && orderField) {
        sortSelect.addEventListener('change', function() {
            orderField.value = this.value;
            // Сбрасываем страницу на первую при изменении сортировки
            const pageField = filterForm.querySelector('input[name="page"]');
            if (pageField) {
                pageField.value = '1';
            }
            filterForm.submit();
        });
    }
    
    // Количество на странице - обновляем скрытое поле и отправляем форму
    if (perPageSelect && perPageField) {
        perPageSelect.addEventListener('change', function() {
            perPageField.value = this.value;
            // Сбрасываем страницу на первую при изменении количества
            const pageField = filterForm.querySelector('input[name="page"]');
            if (pageField) {
                pageField.value = '1';
            }
            filterForm.submit();
        });
    }
    
    // Удаление отдельных фильтров
    document.querySelectorAll('.remove-filter').forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const key = this.getAttribute('data-key');
            const value = this.getAttribute('data-value');
            
            // Находим соответствующий чекбокс или поле и снимаем выделение
            if (key === 'category' || key === 'theme' || key === 'collection' || key === 'size' || key === 'status') {
                // Для чекбоксов
                const checkbox = document.querySelector(`input[name="${key}"][value="${value}"]`);
                if (checkbox) {
                    checkbox.checked = false;
                }
            } else if (key === 'price_min' || key === 'price_max') {
                // Для полей цены
                const input = document.querySelector(`input[name="${key}"]`);
                if (input) {
                    input.value = '';
                }
            }
            
            // Обновляем состояние галочки "Только доступные"
            updateAvailableOnlyCheckbox();
            
            // Сбрасываем страницу на первую
            const pageField = filterForm.querySelector('input[name="page"]');
            if (pageField) {
                pageField.value = '1';
            }

            filterForm.submit();
        });
    });
    
    // Сброс всех фильтров
    function resetAllFilters() {
        // Сбрасываем все чекбоксы
        filterForm.querySelectorAll('input[type="checkbox"]').forEach(checkbox => {
            checkbox.checked = false;
        });
        
        // Очищаем все текстовые поля
        filterForm.querySelectorAll('input[type="text"], input[type="number"]').forEach(input => {
            if (input.name !== 'q' && input.name !== 'order' && input.name !== 'per_page') {
                input.value = '';
            }
        });
        
        // Сбрасываем сортировку на значение по умолчанию
        if (sortSelect) {
            sortSelect.value = '-created_at';
        }
        if (orderField) {
            orderField.value = '-created_at';
        }
        
        // Сбрасываем количество на странице на значение по умолчанию
        if (perPageSelect) {
            perPageSelect.value = '12';
        }
        if (perPageField) {
            perPageField.value = '12';
        }
        
        // Сбрасываем страницу
        const pageField = filterForm.querySelector('input[name="page"]');
        if (pageField) {
            pageField.value = '1';
        }

        filterForm.submit();
    }
    
    // Обработчики для кнопок сброса
    if (resetFiltersBtn) {
        resetFiltersBtn.addEventListener('click', resetAllFilters);
    }
    
    if (clearAllFiltersBtn) {
        clearAllFiltersBtn.addEventListener('click', resetAllFilters);
    }
    
    if (resetFiltersNoResults) {
        resetFiltersNoResults.addEventListener('click', resetAllFilters);
    }
    
    // Показать/скрыть фильтры на мобильных
    if (filterToggleBtn && filterCard) {
        const btnTextElement = filterToggleBtn.querySelector('.btn-text');
        const icon = filterToggleBtn.querySelector('i');
        
        if (btnTextElement && icon) {
            filterToggleBtn.addEventListener('click', function() {
                filterCard.classList.toggle('show');
                
                if (filterCard.classList.contains('show')) {
                    icon.className = 'bi bi-x-lg me-2';
                    btnTextElement.textContent = 'Скрыть фильтры';
                } else {
                    icon.className = 'bi bi-funnel me-2';
                    btnTextElement.textContent = 'Показать фильтры';
                }
            });
        }
    }
    
    // Подсчет активных фильтров (исправленная версия)
    function updateFilterCount() {
        // Получаем все отмеченные чекбоксы (кроме show_available_only)
        const checkboxes = Array.from(filterForm.querySelectorAll('input[type="checkbox"]:checked'))
            .filter(cb => cb.id !== 'show_available_only');
        
        // Получаем текстовые поля и фильтруем те, которые не пустые и не поиск
        const textInputs = Array.from(filterForm.querySelectorAll('input[type="text"]')).filter(input => {
            return input.name !== 'q' && input.value.trim() !== '';
        });
        
        // Получаем числовые поля и фильтруем те, которые не пустые
        const numberInputs = Array.from(filterForm.querySelectorAll('input[type="number"]')).filter(input => {
            return input.value.trim() !== '';
        });
        
        let activeCount = checkboxes.length + textInputs.length + numberInputs.length;
        
        // Обновляем бейдж с количеством
        const filterCountBadge = document.getElementById('filter-count-badge');
        if (filterCountBadge) {
            filterCountBadge.textContent = activeCount;
            filterCountBadge.style.display = activeCount > 0 ? 'inline-block' : 'none';
        }
        
        // Обновляем текст кнопки на мобильных
        if (filterToggleBtn) {
            const badge = filterToggleBtn.querySelector('.badge');
            if (badge) {
                badge.textContent = activeCount;
                badge.style.display = activeCount > 0 ? 'inline-block' : 'none';
            }
        }
    }
    
    // Инициализация счетчика фильтров
    updateFilterCount();
    updateAvailableOnlyCheckbox();
    
    // Обновляем счетчик при изменении фильтров
    filterForm.querySelectorAll('input').forEach(input => {
        input.addEventListener('change', updateFilterCount);
    });
    
    // Дебаунс для полей ввода (чтобы не триггерить change при каждом нажатии клавиши)
    let timeoutId;
    filterForm.querySelectorAll('input[type="text"], input[type="number"]').forEach(input => {
        input.addEventListener('input', function() {
            clearTimeout(timeoutId);
            timeoutId = setTimeout(() => {
                this.dispatchEvent(new Event('change'));
            }, 300);
        });
    });
    
    // Автоматически закрывать фильтры на мобильных после применения
    if (window.innerWidth < 992) {
        filterForm.addEventListener('submit', function() {
            if (filterCard && filterCard.classList.contains('show')) {
                filterCard.classList.remove('show');
                const icon = filterToggleBtn.querySelector('i');
                const text = filterToggleBtn.querySelector('.btn-text');
                if (icon && text) {
                    icon.className = 'bi bi-funnel me-2';
                    text.textContent = ' Показать фильтры';
                }
            }
        });
    }
    
    function adjustFilterHeight() {
        if (window.innerWidth >= 992 && filterCard) {
            const header = document.querySelector('header');
            if (header) {
                const headerHeight = header.offsetHeight;
                const viewportHeight = window.innerHeight;
                const filterTop = Math.max(headerHeight + 20, 110);
                
                filterCard.style.top = `${filterTop}px`;
                filterCard.style.maxHeight = `calc(100vh - ${filterTop + 20}px)`;
            }
        }
    }
    
    adjustFilterHeight();
    window.addEventListener('resize', adjustFilterHeight);
    window.addEventListener('scroll', adjustFilterHeight);
});