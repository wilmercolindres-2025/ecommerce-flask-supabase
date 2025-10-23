/**
 * Main JavaScript for E-Commerce
 */

// Import HTMX
import htmx from 'htmx.org';
window.htmx = htmx;

// Import Alpine.js
import Alpine from 'alpinejs';
window.Alpine = Alpine;
Alpine.start();

// Utility functions
const utils = {
  // Format currency
  formatCurrency(amount) {
    return `Q${parseFloat(amount).toFixed(2).replace(/\d(?=(\d{3})+\.)/g, '$&,')}`;
  },
  
  // Show toast notification
  showToast(message, type = 'info') {
    const toast = document.createElement('div');
    toast.className = `fixed top-4 right-4 z-50 p-4 rounded-lg shadow-lg animate-slideDown ${
      type === 'success' ? 'bg-success-500' :
      type === 'error' ? 'bg-error-500' :
      type === 'warning' ? 'bg-warning-500' :
      'bg-primary-500'
    } text-white`;
    toast.textContent = message;
    
    document.body.appendChild(toast);
    
    setTimeout(() => {
      toast.classList.add('opacity-0', 'transition-opacity');
      setTimeout(() => toast.remove(), 300);
    }, 3000);
  },
  
  // Confirm dialog
  confirm(message) {
    return window.confirm(message);
  },
  
  // Debounce function
  debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
      const later = () => {
        clearTimeout(timeout);
        func(...args);
      };
      clearTimeout(timeout);
      timeout = setTimeout(later, wait);
    };
  }
};

window.utils = utils;

// Cart functionality
const cart = {
  // Update cart count
  updateCount() {
    fetch('/carrito/contador')
      .then(res => res.json())
      .then(data => {
        const countElements = document.querySelectorAll('[data-cart-count]');
        countElements.forEach(el => {
          el.textContent = data.count;
          if (data.count > 0) {
            el.classList.remove('hidden');
          } else {
            el.classList.add('hidden');
          }
        });
      })
      .catch(err => console.error('Error updating cart count:', err));
  },
  
  // Add to cart
  add(productId, variantId = null, quantity = 1) {
    const formData = new FormData();
    formData.append('product_id', productId);
    if (variantId) formData.append('variant_id', variantId);
    formData.append('quantity', quantity);
    
    fetch('/carrito/agregar', {
      method: 'POST',
      body: formData,
      headers: {
        'HX-Request': 'true'
      }
    })
    .then(res => res.json())
    .then(data => {
      if (data.success) {
        utils.showToast('Producto agregado al carrito', 'success');
        cart.updateCount();
      } else {
        utils.showToast(data.error || 'Error al agregar al carrito', 'error');
      }
    })
    .catch(err => {
      console.error('Error:', err);
      utils.showToast('Error al agregar al carrito', 'error');
    });
  },
  
  // Remove from cart
  remove(itemId) {
    if (!utils.confirm('¿Eliminar este producto del carrito?')) return;
    
    fetch(`/carrito/eliminar/${itemId}`, {
      method: 'POST',
      headers: {
        'HX-Request': 'true'
      }
    })
    .then(res => res.json())
    .then(data => {
      if (data.success) {
        utils.showToast('Producto eliminado', 'success');
        window.location.reload();
      } else {
        utils.showToast(data.error || 'Error al eliminar', 'error');
      }
    })
    .catch(err => {
      console.error('Error:', err);
      utils.showToast('Error al eliminar', 'error');
    });
  },
  
  // Update quantity
  updateQuantity: utils.debounce((itemId, quantity) => {
    const formData = new FormData();
    formData.append('quantity', quantity);
    
    fetch(`/carrito/actualizar/${itemId}`, {
      method: 'POST',
      body: formData,
      headers: {
        'HX-Request': 'true'
      }
    })
    .then(res => res.json())
    .then(data => {
      if (data.success) {
        window.location.reload();
      } else {
        utils.showToast(data.error || 'Error al actualizar', 'error');
      }
    })
    .catch(err => {
      console.error('Error:', err);
      utils.showToast('Error al actualizar', 'error');
    });
  }, 500)
};

window.cart = cart;

// Product image gallery
function initProductGallery() {
  const mainImage = document.getElementById('main-product-image');
  const thumbnails = document.querySelectorAll('[data-thumbnail]');
  
  if (!mainImage || thumbnails.length === 0) return;
  
  thumbnails.forEach(thumb => {
    thumb.addEventListener('click', () => {
      const newSrc = thumb.dataset.thumbnail;
      mainImage.src = newSrc;
      
      // Update active state
      thumbnails.forEach(t => t.classList.remove('ring-2', 'ring-primary-500'));
      thumb.classList.add('ring-2', 'ring-primary-500');
    });
  });
}

// Search functionality
function initSearch() {
  const searchInput = document.getElementById('search-input');
  const searchResults = document.getElementById('search-results');
  
  if (!searchInput) return;
  
  const performSearch = utils.debounce((query) => {
    if (query.length < 2) {
      if (searchResults) searchResults.classList.add('hidden');
      return;
    }
    
    fetch(`/buscar?q=${encodeURIComponent(query)}`)
      .then(res => res.text())
      .then(html => {
        if (searchResults) {
          searchResults.innerHTML = html;
          searchResults.classList.remove('hidden');
        }
      })
      .catch(err => console.error('Search error:', err));
  }, 300);
  
  searchInput.addEventListener('input', (e) => {
    performSearch(e.target.value);
  });
  
  // Close results on outside click
  document.addEventListener('click', (e) => {
    if (searchResults && !searchInput.contains(e.target) && !searchResults.contains(e.target)) {
      searchResults.classList.add('hidden');
    }
  });
}

// Mobile menu toggle
function initMobileMenu() {
  const menuButton = document.getElementById('mobile-menu-button');
  const mobileMenu = document.getElementById('mobile-menu');
  
  if (!menuButton || !mobileMenu) return;
  
  menuButton.addEventListener('click', () => {
    mobileMenu.classList.toggle('hidden');
  });
}

// Initialize on DOM ready
document.addEventListener('DOMContentLoaded', () => {
  cart.updateCount();
  initProductGallery();
  initSearch();
  initMobileMenu();
  
  // Auto-dismiss alerts
  const alerts = document.querySelectorAll('[data-auto-dismiss]');
  alerts.forEach(alert => {
    setTimeout(() => {
      alert.classList.add('opacity-0', 'transition-opacity');
      setTimeout(() => alert.remove(), 300);
    }, 5000);
  });
});

// HTMX event listeners
document.body.addEventListener('htmx:afterSwap', (event) => {
  // Re-initialize components after HTMX swap
  cart.updateCount();
});

document.body.addEventListener('htmx:responseError', (event) => {
  utils.showToast('Error en la solicitud', 'error');
});

// Export for use in templates
export { utils, cart };
