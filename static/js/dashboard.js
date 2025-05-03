async function updateOrders() {
	div = document.getElementById('orderList');
	div.innerText = 'Загрузка...';
    orders = await fetch('/admin/getOrders');
	if (orders.status == 401) {
		location.href = '/login';
	}
	
	if (orders.status == 404) {
		div.innerText = 'Заказы отсутствуют.';
	}
	
	console.log(orders.JSON);
}

updateOrders()