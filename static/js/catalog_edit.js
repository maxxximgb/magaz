async function updateCatalog() {
    div = document.getElementById('productList');
	div.innerHTML = 'Загрузка...';
    orders = await fetch('/cpApi/getOrders');
	if (orders.status == 401) {
		location.href = '/login';
	}

	if (orders.status == 404) {
		div.innerText = 'Заказы отсутствуют.';
	}

	console.log(orders.JSON);
}