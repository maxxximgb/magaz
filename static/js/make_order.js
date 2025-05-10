document.addEventListener('DOMContentLoaded', async () => {
  const cartManager = CartManager.getInstance();
  await cartManager.syncWithServer();
  const info = document.getElementById('order_info');
  info.innerText = `Вы заказали ${cartManager.getTotalQuantity()} товар(а/ов) на сумму ${cartManager.getTotalSum()} руб.`;

  const cleanedCart = Object.fromEntries(
    Object.entries(cartManager.cart).map(([key, product]) => {
      const {imageSrc, pricePerKg, minWeight, ...cleanProduct} = product;
      return [key, cleanProduct];
    })
  );

  document.getElementById('products').value = JSON.stringify(cleanedCart);
});