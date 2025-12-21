const STORAGE_KEY = "lunch_order";

export function getOrder() {
  return JSON.parse(localStorage.getItem(STORAGE_KEY)) || {
    soup: null,
    main_course: null,
    salad: null,
    drink: null,
    dessert: null
  };
}

export function setDish(category, id) {
  const order = getOrder();
  order[category] = id;
  localStorage.setItem(STORAGE_KEY, JSON.stringify(order));
}

export function removeDish(category) {
  const order = getOrder();
  order[category] = null;
  localStorage.setItem(STORAGE_KEY, JSON.stringify(order));
}

export function clearOrder() {
  localStorage.removeItem(STORAGE_KEY);
}
