/**
 * Admin Dashboard JavaScript
 * La Bodegona - Admin Panel
 */

// Mobile menu toggle
document.addEventListener('DOMContentLoaded', function() {
    const mobileMenuBtn = document.getElementById('mobile-menu-btn');
    const sidebar = document.querySelector('aside');
    
    if (mobileMenuBtn && sidebar) {
        mobileMenuBtn.addEventListener('click', function() {
            sidebar.classList.toggle('hidden');
        });
    }
    
    // Auto-dismiss alerts
    const alerts = document.querySelectorAll('[data-auto-dismiss]');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.opacity = '0';
            setTimeout(() => alert.remove(), 300);
        }, 5000);
    });
    
    // Confirm delete actions
    const deleteButtons = document.querySelectorAll('[data-confirm-delete]');
    deleteButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            if (!confirm('¿Estás seguro de que deseas eliminar este elemento? Esta acción no se puede deshacer.')) {
                e.preventDefault();
            }
        });
    });
    
    // Image preview
    const imageInputs = document.querySelectorAll('input[type="file"][accept*="image"]');
    imageInputs.forEach(input => {
        input.addEventListener('change', function(e) {
            const file = e.target.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    const preview = document.getElementById('image-preview');
                    if (preview) {
                        preview.src = e.target.result;
                        preview.classList.remove('hidden');
                    }
                };
                reader.readAsDataURL(file);
            }
        });
    });
    
    // Form validation
    const forms = document.querySelectorAll('form[data-validate]');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const requiredFields = form.querySelectorAll('[required]');
            let isValid = true;
            
            requiredFields.forEach(field => {
                if (!field.value.trim()) {
                    isValid = false;
                    field.classList.add('border-red-500');
                    
                    // Show error message
                    let errorMsg = field.nextElementSibling;
                    if (!errorMsg || !errorMsg.classList.contains('error-message')) {
                        errorMsg = document.createElement('p');
                        errorMsg.className = 'error-message text-red-500 text-sm mt-1';
                        errorMsg.textContent = 'Este campo es requerido';
                        field.parentNode.insertBefore(errorMsg, field.nextSibling);
                    }
                } else {
                    field.classList.remove('border-red-500');
                    const errorMsg = field.nextElementSibling;
                    if (errorMsg && errorMsg.classList.contains('error-message')) {
                        errorMsg.remove();
                    }
                }
            });
            
            if (!isValid) {
                e.preventDefault();
                showNotification('Por favor completa todos los campos requeridos', 'error');
            }
        });
    });
    
    // Table row selection
    const selectAllCheckbox = document.getElementById('select-all');
    if (selectAllCheckbox) {
        selectAllCheckbox.addEventListener('change', function() {
            const checkboxes = document.querySelectorAll('input[type="checkbox"][name="selected[]"]');
            checkboxes.forEach(checkbox => {
                checkbox.checked = this.checked;
            });
        });
    }
    
    // Bulk actions
    const bulkActionBtn = document.getElementById('bulk-action-btn');
    if (bulkActionBtn) {
        bulkActionBtn.addEventListener('click', function() {
            const selected = document.querySelectorAll('input[type="checkbox"][name="selected[]"]:checked');
            if (selected.length === 0) {
                showNotification('Selecciona al menos un elemento', 'warning');
                return;
            }
            
            const action = document.getElementById('bulk-action-select').value;
            if (!action) {
                showNotification('Selecciona una acción', 'warning');
                return;
            }
            
            if (confirm(`¿Estás seguro de aplicar esta acción a ${selected.length} elementos?`)) {
                // Submit form or make AJAX request
                console.log('Bulk action:', action, 'Items:', selected.length);
            }
        });
    }
    
    // Search with debounce
    const searchInputs = document.querySelectorAll('input[type="search"], input[data-search]');
    searchInputs.forEach(input => {
        let timeout;
        input.addEventListener('input', function() {
            clearTimeout(timeout);
            timeout = setTimeout(() => {
                // Trigger search
                console.log('Search:', this.value);
            }, 500);
        });
    });
    
    // Sortable tables
    const sortableHeaders = document.querySelectorAll('th[data-sortable]');
    sortableHeaders.forEach(header => {
        header.style.cursor = 'pointer';
        header.addEventListener('click', function() {
            const column = this.dataset.sortable;
            const currentOrder = this.dataset.order || 'asc';
            const newOrder = currentOrder === 'asc' ? 'desc' : 'asc';
            
            // Update URL with sort parameters
            const url = new URL(window.location);
            url.searchParams.set('sort', column);
            url.searchParams.set('order', newOrder);
            window.location = url;
        });
    });
});

/**
 * Show notification
 */
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `fixed top-4 right-4 px-6 py-3 rounded-lg shadow-lg z-50 animate-slideDown ${
        type === 'success' ? 'bg-green-500' :
        type === 'error' ? 'bg-red-500' :
        type === 'warning' ? 'bg-yellow-500' :
        'bg-blue-500'
    } text-white`;
    notification.textContent = message;
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.style.opacity = '0';
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

/**
 * Format currency
 */
function formatCurrency(amount) {
    return new Intl.NumberFormat('es-GT', {
        style: 'currency',
        currency: 'GTQ'
    }).format(amount);
}

/**
 * Format date
 */
function formatDate(date) {
    return new Intl.DateTimeFormat('es-GT', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    }).format(new Date(date));
}

/**
 * Copy to clipboard
 */
function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
        showNotification('Copiado al portapapeles', 'success');
    }).catch(err => {
        console.error('Error copying:', err);
        showNotification('Error al copiar', 'error');
    });
}

/**
 * Export table to CSV
 */
function exportTableToCSV(tableId, filename = 'export.csv') {
    const table = document.getElementById(tableId);
    if (!table) return;
    
    let csv = [];
    const rows = table.querySelectorAll('tr');
    
    rows.forEach(row => {
        const cols = row.querySelectorAll('td, th');
        const rowData = Array.from(cols).map(col => {
            return '"' + col.textContent.trim().replace(/"/g, '""') + '"';
        });
        csv.push(rowData.join(','));
    });
    
    const csvContent = csv.join('\n');
    const blob = new Blob([csvContent], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    a.click();
    window.URL.revokeObjectURL(url);
}

/**
 * Print element
 */
function printElement(elementId) {
    const element = document.getElementById(elementId);
    if (!element) return;
    
    const printWindow = window.open('', '', 'height=600,width=800');
    printWindow.document.write('<html><head><title>Imprimir</title>');
    printWindow.document.write('<link rel="stylesheet" href="/static/css/output.css">');
    printWindow.document.write('</head><body>');
    printWindow.document.write(element.innerHTML);
    printWindow.document.write('</body></html>');
    printWindow.document.close();
    printWindow.print();
}

// Export functions for global use
window.showNotification = showNotification;
window.formatCurrency = formatCurrency;
window.formatDate = formatDate;
window.copyToClipboard = copyToClipboard;
window.exportTableToCSV = exportTableToCSV;
window.printElement = printElement;
