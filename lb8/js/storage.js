// Получить заказ из localStorage
window.getOrder = function () {
  const data = localStorage.getItem("lunch_order");
  return data ? JSON.parse(data) : {};
};

// Добавить блюдо в заказ (сохраняем id)
window.setDish = function (category, id) {
  const order = window.getOrder();
  order[category] = id;
  localStorage.setItem("lunch_order", JSON.stringify(order));
};

// Удалить блюдо из заказа
window.removeDish = function (category) {
  const order = window.getOrder();
  delete order[category];
  localStorage.setItem("lunch_order", JSON.stringify(order));
};

// Очистить весь заказ
window.clearOrder = function () {
  localStorage.removeItem("lunch_order");
};
