class CartManager {
  constructor() {
    this.cart = JSON.parse(localStorage.getItem('cart')) || {};
    this.initEventListeners();
    this.updateCartBadge();
  }

  updateCartBadge = () => {
    const total = Object.values(this.cart).reduce((sum, { quantity }) => sum + quantity, 0);
    const badge = document.getElementById('cart-badge');
    if (!badge) return;

    badge.classList.toggle('d-none', !total);
    badge.textContent = total || '';
  }

  saveCart = () => {
    localStorage.setItem('cart', JSON.stringify(this.cart));
    this.updateCartBadge();
  }

  addToCart = async (productId, weight) => {
    try {
      const res = await fetch(`/user/getProduct/${productId}`);
      if (!res.ok) throw new Error('Товар недоступен');

      const product = await res.json();
      const existing = this.cart[productId];

      this.cart[productId] = {
        name: product.name,
        _price: product.price * weight,
        weight,
        quantity: (existing?.quantity || 0) + 1,
        image: product.imageSrc
      };

      this.saveCart();
      this.showAlert('Товар добавлен в корзину', 'success');
    } catch (err) {
      this.showAlert(err.message, 'danger');
    }
  }

  showAlert = (msg, type) => {
    const container = this.getAlertContainer();
    const alert = document.createElement('div');

    alert.className = `alert alert-${type} alert-dismissible fade show alert-slide`;
    alert.innerHTML = `
      ${msg}
      <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;

    container.prepend(alert);

    // Автоматическое скрытие через 5 секунд
    setTimeout(() => {
      const bsAlert = new bootstrap.Alert(alert);
      bsAlert.close();
    }, 5000);
  }

  getAlertContainer = () => {
    let container = document.getElementById('alert-container');
    if (!container) {
      container = document.createElement('div');
      container.id = 'alert-container';
      container.className = 'position-fixed top-0 end-0 p-3';
      document.body.appendChild(container);
    }
    return container;
  }

  initEventListeners = () => {
    document.body.addEventListener('click', (e) => {
      const btn = e.target.closest('.add-to-cart');
      if (btn) this.addToCart(btn.dataset.productId);
    });
  }
}

document.addEventListener('DOMContentLoaded', () => new CartManager());