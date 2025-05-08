async function updateCatalog() {
    const div = document.getElementById('productList');
    try {
        const response = await fetch('/user/getCatalog');
        if (!response.ok) {
            throw new Error('Ошибка загрузки каталога');
        }

        const products = await response.json();

        let html = '<div class="row row-cols-1 row-cols-md-3 g-4">';
        products.forEach(product => {
            html += `
                <div class="col">
                    <div class="card h-100">
                        <img src="${product.imageSrc}" class="card-img-top" alt="${product.name}" style="height: 200px; object-fit: cover;">
                        <div class="card-body d-flex flex-column">
                            <div class="d-flex justify-content-between align-items-start mb-2">
                                <div>
                                    <h5 class="card-title">${product.name}</h5>
                                    <p class="card-text mb-0">
                                        ${product.price.toLocaleString()} руб/кг.
                                    </p>
                                </div>
                                <a href="/user/about?id=${product.id}" class="btn btn-primary ms-3">Подробнее</a>
                            </div>
                        </div>
                    </div>
                </div>
            `;
        });
        html += '</div>';

        div.innerHTML = html;
    } catch (error) {
        div.innerHTML = `<div class="alert alert-danger">${error.message}</div>`;
        console.error('Ошибка:', error);
    }
}

updateCatalog();