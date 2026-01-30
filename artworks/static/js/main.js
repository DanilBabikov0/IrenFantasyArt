// artworks/static/js/main.js
document.addEventListener('DOMContentLoaded', function() {
    const collectionSearch = document.getElementById('collectionSearch');
    const collectionItems = document.querySelectorAll('.collection-item');
    
    if (collectionSearch && collectionItems.length > 0) {
        collectionSearch.addEventListener('input', function(e) {
            const searchTerm = e.target.value.toLowerCase().trim();
            
            collectionItems.forEach(item => {
                const itemName = item.getAttribute('data-name');
                const itemText = item.textContent.toLowerCase();
                
                if (searchTerm === '' || itemName.includes(searchTerm) || itemText.includes(searchTerm)) {
                    item.style.display = 'flex';
                } else {
                    item.style.display = 'none';
                }
            });
        });
    }
    
    const collectionDropdown = document.querySelector('.nav-item.dropdown');
    if (collectionDropdown) {
        collectionDropdown.addEventListener('shown.bs.dropdown', function() {
            setTimeout(() => {
                const searchField = this.querySelector('input[type="text"]');
                if (searchField) {
                    searchField.focus();
                }
            }, 100);
        });
    }
});