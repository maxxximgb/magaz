let currentProduct = null;
const domElements = {};

function calculatePricePerGram() {
    return currentProduct.price / currentProduct.weight;
}

async function initProductPage() {
    try {
        const productId = new URLSearchParams(window.location.search).get('id') || 1;
        const response = await fetch(`/user/getProduct/${productId}`);
        if (!response.ok) throw new Error('Продукт не найден');

        currentProduct = await response.json();
        renderProductLayout();
        setupDOMElements();
        addEventListeners();
        updateCalculations();

    } catch (error) {
        document.getElementById('content').innerHTML = `
            <div class="alert alert-danger">
                ${error.message}
                <button onclick="initProductPage()" class="btn btn-link">Повторить</button>
            </div>
        `;
    }
}

function addToCart() {

}

function renderProductLayout() {
    document.getElementById('content').innerHTML = `
        <div class="container mt-4">
            <div class="row">
                <div class="col-md-6 mb-4">
                    <img src="${currentProduct.imageSrc}"
                         class="img-fluid rounded shadow"
                         alt="${currentProduct.name}">
                </div>
                <div class="col-md-6">
                    <div class="d-flex justify-content-between align-items-start mb-4">
                        <h1>${currentProduct.name}</h1>
                        <div class="bg-light p-3 rounded ms-3">
                            <h4>${currentProduct.price} руб за ${currentProduct.weight} г</h4>
                            <small class="text-muted">${calculatePricePerGram().toFixed(2)} руб/г</small>
                        </div>
                    </div>
                    <div class="mb-3">
                        <label class="form-label h5">Вес (мин. ${currentProduct.weight} г)</label>
                        <input type="number" id="weightInput" class="form-control"
                               min="${currentProduct.weight}" step="0.1" value="${currentProduct.weight}">
                    </div>
                    <div class="mb-3">
                        <label class="form-label h5">Количество</label>
                        <input type="number" id="quantityInput" class="form-control" min="1" value="1">
                    </div>
                    <div class="d-flex justify-content-between align-items-center border-top pt-4">
                        <div>
                            <h3 id="totalPrice">0 руб</h3>
                            <small id="calculation" class="text-muted"></small>
                        </div>
                        <button class="btn btn-primary btn-lg" id="addToCartBtn">
                            Добавить в корзину
                        </button>
                    </div>
                </div>
            </div>
        </div>
    `;

    // Инициализируем обработчики событий
    const addToCartBtn = document.getElementById('addToCartBtn');
    addToCartBtn.addEventListener('click', () => {
        const weight = parseFloat(document.getElementById('weightInput').value);
        const quantity = parseInt(document.getElementById('quantityInput').value);

        if (isNaN(weight) || weight < currentProduct.weight) {
            alert(`Минимальный вес: ${currentProduct.weight} г`);
            return;
        }

        if (isNaN(quantity) || quantity < 1) {
            alert('Минимальное количество: 1');
            return;
        }

        // Добавляем товар quantity раз с указанным весом
        for (let i = 0; i < quantity; i++) {
            cartManager.addToCart(currentProduct.id, weight);
        }
    });

    // Инициализируем корзину если еще не инициализирована
    if (!window.cartManager) {
        window.cartManager = new CartManager();
    }
}

function setupDOMElements() {
    domElements.weightInput = document.getElementById('weightInput');
    domElements.quantityInput = document.getElementById('quantityInput');
    domElements.totalPrice = document.getElementById('totalPrice');
    domElements.calculation = document.getElementById('calculation');
    domElements.buyButton = document.getElementById('addToCartBtn');
}

function addEventListeners() {
    domElements.weightInput.addEventListener('input', updateCalculations);
    domElements.quantityInput.addEventListener('input', () => {
        domElements.quantityInput.value = Math.max(1, parseInt(domElements.quantityInput.value) || 1);
        updateCalculations();
    });
}

function updateCalculations() {
    const weight = Math.max(currentProduct.weight, parseFloat(domElements.weightInput.value) || currentProduct.weight);
    const quantity = parseInt(domElements.quantityInput.value);
    const pricePerGram = calculatePricePerGram();
    const total = (weight * pricePerGram * quantity).toFixed(2);

    domElements.weightInput.value = weight.toFixed(1);
    domElements.totalPrice.textContent = `${total} руб`;
    domElements.calculation.textContent = `${weight.toFixed(1)}г × ${quantity}шт × ${pricePerGram.toFixed(2)}руб/г`;
    domElements.buyButton.href = `/buy?id=${currentProduct.id}&weight=${weight}&quantity=${quantity}`;
}

document.addEventListener('DOMContentLoaded', initProductPage);