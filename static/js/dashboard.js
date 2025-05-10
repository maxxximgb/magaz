async function updateOrders() {
    const tbody = document.getElementById('ordersBody');
    const messageDiv = document.getElementById('ordersMessage');
    tbody.innerHTML = '';
    messageDiv.innerHTML = '<div class="spinner-border text-primary" role="status"></div>';

    try {
        const response = await fetch('/admin/getOrders');

        if (response.status === 401) {
            location.href = '/login';
            return;
        }

        if (response.status === 404) {
            messageDiv.innerHTML = '<p class="text-muted">Нет активных заказов</p>';
            return;
        }

        const orders = await response.json();
        messageDiv.innerHTML = '';



        orders.forEach(order => {
            const row = document.createElement('tr');
            let total = 0;

            const productsHtml = order.products.length > 0
                ? order.products.map(product => {
                      const productTotal = (product.pricePerKg * product.weight / 1000) * product.quantity;
                      total += productTotal;
                      return `
                          <div class="mb-1">
                              <span class="fw-medium">${product.name}</span>
                              <div class="text-muted small">
                                  ${product.quantity} × ${product.weight}г
                                  <span class="ms-2">${productTotal.toFixed(2)}₽</span>
                              </div>
                          </div>
                      `;
                  }).join('')
                : '<div class="text-muted small">Нет продуктов</div>';

            row.innerHTML = `
                <td class="fw-semibold">${order.id}</td>
                <td>${order.customer_name || '<span class="text-muted">Не указано</span>'}</td>
                <td class="d-none d-md-table-cell">${order.customer_phone}</td>
                <td class="d-none d-sm-table-cell">${order.promocode || '—'}</td>
                <td class="small">${productsHtml}</td>
                <td class="fw-semibold text-nowrap">${total.toFixed(2)}₽</td>
            `;

            tbody.appendChild(row);
        });

    } catch (error) {
        console.error('Ошибка:', error);
        messageDiv.innerHTML = '<div class="alert alert-danger">Ошибка загрузки заказов</div>';
    }
}

document.addEventListener('DOMContentLoaded', updateOrders);