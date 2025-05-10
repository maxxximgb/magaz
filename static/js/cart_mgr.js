class CartManager {
  constructor() {
    if (CartManager.instance) {
      return CartManager.instance;
    }
    CartManager.instance = this;
    this.cart = JSON.parse(localStorage.getItem('cart')) || {};
    // Элементы
    this.els = {
      tableWrapper: document.getElementById('cart-table-wrapper'),
      table: document.getElementById('cart-table'),
      tableTbody: document.querySelector('#cart-table tbody'),
      mobileCards: document.getElementById('mobile-cards'),
      emptyMsg: document.getElementById('cart-empty'),
      totalEl: document.getElementById('cart-total'),
      orderBtn: document.getElementById('order_btn'),
    }
    this.updateCartBadge();
    this.initEventListeners();
    this.syncWithServer().then(() => this.renderCart());
  }


  async syncWithServer() {
    const keys = Object.keys(this.cart);
    let needRerender = false;
    for (const key of keys) {
      const item = this.cart[key];
      try {
        const res = await fetch(`/user/getProduct/${item.id}`);
        if (res.status == 404) throw new Error('Product not found');
        const data = await res.json();
        let changed = false;

        if (item.minWeight !== data.minWeight) {
          this.showAlert(
            `Минимальный вес для продукта ${item.id} изменён: ${item.minWeight} → ${data.minWeight}`,
            'info'
          );
          item.minWeight = data.minWeight;
          changed = true;
        }

        const newPricePerKg = data.price;
        if (item.pricePerKg !== newPricePerKg) {
          const old = item.pricePerKg ? item.pricePerKg.toFixed(2) : '—';
          this.showAlert(
            `Цена за кг. для продукта ${item.id} изменена: ${old} → ${newPricePerKg.toFixed(2)}`,
            'info'
          );
          item.pricePerKg = newPricePerKg;
          changed = true;
        }

        if (item.imageSrc !== data.imageSrc) {
          this.showAlert(
            `Изображение для продукта ${item.id} обновлено.`,
            'info'
          );
          item.imageSrc = data.imageSrc;
          changed = true;
        }

        if (changed) needRerender = true;
      } catch (err) {
        delete this.cart[key];
        this.showAlert(
          `Продукт ${item.id} больше не доступен и был удалён из корзины`,
          'warning'
        );
        needRerender = true;
      }
    }
    this.saveCart();
    if (needRerender && this.els.table) this.renderCart();
  }

  updateCartBadge() {
    const totalQty = Object.values(this.cart).reduce((sum, { quantity }) => sum + quantity, 0);
    const badge = document.getElementById('cart-badge');
    if (!badge) return;
    badge.classList.toggle('d-none', totalQty === 0);
    badge.textContent = totalQty || '';
  }

  saveCart() {
    localStorage.setItem('cart', JSON.stringify(this.cart));
    this.updateCartBadge();
  }


  renderCart() {
    if (!this.els.tableWrapper) return;
    const entries = Object.entries(this.cart);
    if (!entries.length) {
      this.showEmpty();
      return;
    }
    this.hideEmpty();
    this.renderDesktop(entries);
    this.renderMobile(entries);
    this.updateTotal(entries);
  }

  addToCart(currentProduct) {
    try {
      const weight = parseFloat(document.querySelector('#weightInput').value);
      const quantity = parseInt(document.querySelector('#quantityInput').value, 10);
      const minW = currentProduct.minWeight || 0.1;
      if (!weight || weight < minW) {
        this.showAlert(`Введите корректный вес (мин. ${minW})`, 'danger');
        return;
      }
      if (!quantity || quantity < 1) {
        this.showAlert('Введите корректное количество (мин. 1)', 'danger');
        return;
      }
      const key = `${currentProduct.id}-${weight.toFixed(2)}`;
      if (this.cart[key]) this.cart[key].quantity += quantity;
      else this.cart[key] = {
        id: currentProduct.id,
        imageSrc: currentProduct.imageSrc || '',
        weight,
        quantity,
        pricePerKg: currentProduct.price || 0,
        minWeight: currentProduct.minWeight || minW
      };

      this.saveCart();
      this.showAlert('Товар добавлен в корзину', 'success');
    } catch (e) {
      this.showAlert(e.message, 'danger');
    }
  }

  removeProduct(cartKey) {
    if (this.cart[cartKey]) {
      delete this.cart[cartKey];
      this.saveCart();
      this.showAlert('Товар удален из корзины', 'warning');
      if (this.els.table) this.renderCart();
    }
  }

  showAlert(msg, type) {
    const container = this.getAlertContainer();
    const alert = document.createElement('div');
    alert.className = `alert alert-${type} alert-dismissible fade show alert-slide`;
    alert.innerHTML = `${msg}<button type="button" class="btn-close" data-bs-dismiss="alert"></button>`;
    container.prepend(alert);
    setTimeout(() => new bootstrap.Alert(alert).close(), 5000);
  }

  getAlertContainer() {
    let c = document.getElementById('alert-container');
    if (!c) {
      c = document.createElement('div');
      c.id = 'alert-container';
      c.className = 'position-fixed top-0 end-0 p-3';
      document.body.appendChild(c);
    }
    return c;
  }


  renderDesktop(entries) {
    this.els.tableWrapper.classList.remove('d-none');
    this.els.mobileCards.classList.add('d-none');
    this.els.tableTbody.innerHTML = '';
    entries.forEach(([key, item]) => {
      const sum = item.pricePerKg/1000 * item.weight * item.quantity;
      const tr = document.createElement('tr');
      tr.innerHTML = `
        <td class="align-middle"><img src="${item.imageSrc}"
          class="img-thumbnail" style="width:70px; height:70px; object-fit:cover;"></td>
        <td class="align-middle">${item.weight.toFixed(2)} г.</td>
        <td class="align-middle">${item.quantity} шт.</td>
        <td class="align-middle">${item.pricePerKg.toFixed(2)} руб/кг</td>
        <td class="align-middle">${sum.toFixed(2)} руб.</td>
        <td class="align-middle">
          <button class="btn btn-sm btn-danger remove-item-btn" data-key="${key}">✕</button>
        </td>`;
      this.els.tableTbody.appendChild(tr);
    });
    this.els.tableTbody.querySelectorAll('.remove-item-btn')
      .forEach(btn => btn.onclick = () => this.removeProduct(btn.dataset.key));
  }


  renderMobile(entries) {
    this.els.tableWrapper.classList.add('d-none');
    this.els.mobileCards.classList.remove('d-none');
    this.els.mobileCards.innerHTML = '';

    entries.forEach(([key, item]) => {
      const sum = item.pricePerKg/1000 * item.weight * item.quantity;
      const card = document.createElement('div');
      card.className = 'card mb-3';
      card.innerHTML = `
        <div class="row g-0">
          <div class="col-4">
            <img src="${item.imageSrc}" class="img-fluid rounded-start" alt="...">
          </div>
          <div class="col-8">
            <div class="card-body p-2">
              <p class="card-text mb-1">
                <strong>${item.weight.toFixed(2)} г × ${item.quantity} шт.</strong>
              </p>
              <p class="card-text mb-2">${item.pricePerKg.toFixed(2)} руб/кг</p>
              <div class="d-flex justify-content-between align-items-center">
                <span class="fw-bold">${sum.toFixed(2)} руб.</span>
                <button class="btn btn-sm btn-danger remove-item-btn" data-key="${key}">
                  Удалить
                </button>
              </div>
            </div>
          </div>
        </div>`;
      this.els.mobileCards.appendChild(card);
      card.querySelector('.remove-item-btn')
          .onclick = () => this.removeProduct(key);
    });
  }


  updateTotal(entries) {
    const total = entries.reduce((acc, [,item]) =>
      acc + (item.pricePerKg/1000)*item.weight*item.quantity
    , 0);
    this.els.totalEl.textContent = total.toFixed(2);
  }

  showEmpty() {
    this.els.table.innerHTML = '';
    this.els.orderBtn.style.visibility = "hidden"
    this.els.tableWrapper.classList.add('d-none');
    this.els.mobileCards.classList.add('d-none');
    this.els.emptyMsg.classList.remove('d-none');
    this.els.totalEl.textContent = '0';
  }

  hideEmpty() {
    this.els.emptyMsg.classList.add('d-none');
  }

  initEventListeners() {
    document.body.addEventListener('click', e => {
      const btn = e.target.closest('.add-to-cart');
      if (btn) {
        this.addToCart({
          id: btn.dataset.productId,
          minWeight: parseFloat(btn.dataset.minWeight),
          pricePerKg: parseFloat(btn.dataset.pricePerKg),
          imageSrc: btn.dataset.imageSrc
        });
      }
    });
  }

  static getInstance() {
    return CartManager.instance || new CartManager();
  }

  getTotalQuantity() {
    return Object.values(this.cart).reduce(
      (sum, item) => sum + item.quantity,
      0
    );
  }

  getTotalSum() {
    return Object.values(this.cart).reduce(
      (sum, item) => sum + (item.pricePerKg / 1000) * item.weight * item.quantity,
      0
    );
  }
}

document.addEventListener('DOMContentLoaded', () => {
  window.cartManager = new CartManager();
});