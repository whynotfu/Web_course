// Публичное API возвращает id, локальное - нет
const API_URL = "https://edu.std-900.ist.mospolytech.ru/labs/api/dishes";

window.dishes = [];

// Загрузка блюд при загрузке страницы
document.addEventListener("DOMContentLoaded", async () => {
  try {
    const res = await fetch(API_URL);
    if (!res.ok) throw new Error("Ошибка загрузки меню");

    window.dishes = await res.json();
    renderMenu();
    window.dispatchEvent(new Event("dishes-loaded"));
  } catch (e) {
    alert("Не удалось загрузить меню: " + e.message);
  }
});

// Рендер всего меню
function renderMenu() {
  const grids = {
    soup: document.querySelector('.menu-section[data-category="soup"] .dishes-grid'),
    main: document.querySelector('.menu-section[data-category="main"] .dishes-grid'),
    salad: document.querySelector('.menu-section[data-category="salad"] .dishes-grid'),
    drink: document.querySelector('.menu-section[data-category="drink"] .dishes-grid'),
    dessert: document.querySelector('.menu-section[data-category="dessert"] .dishes-grid')
  };

  // Если нет гридов - мы не на странице меню
  const hasGrids = Object.values(grids).some(g => g);
  if (!hasGrids) return;

  // Очищаем грды
  Object.values(grids).forEach(g => { if (g) g.innerHTML = ""; });

  // Рендерим блюда
  window.dishes
    .sort((a, b) => a.name.localeCompare(b.name))
    .forEach(dish => {
      const category = dish.category === "main-course" ? "main" : dish.category;
      const grid = grids[category];
      if (!grid) return;

      const card = document.createElement("div");
      card.className = "dish-card";
      card.dataset.id = dish.id;
      card.dataset.keyword = dish.keyword;
      card.dataset.category = dish.category;

      card.innerHTML = `
        <img src="${dish.image}" alt="${dish.name}">
        <p class="dish-price">${dish.price} ₽</p>
        <p class="dish-name">${dish.name}</p>
        <p class="dish-weight">${dish.count}</p>
        <button class="dish-add" type="button">Добавить</button>
      `;

      grid.appendChild(card);
    });
}

// Фильтры
document.addEventListener("click", (e) => {
  const btn = e.target.closest(".filters button");
  if (!btn) return;

  const section = btn.closest(".menu-section");
  const categoryAttr = section.dataset.category;
  const kind = btn.dataset.kind;

  // Переключаем активность
  const wasActive = btn.classList.contains("active");
  section.querySelectorAll(".filters button").forEach(b => b.classList.remove("active"));

  if (wasActive) {
    // Сбросили фильтр - показываем все
    renderCategory(categoryAttr, null);
  } else {
    // Включили фильтр
    btn.classList.add("active");
    renderCategory(categoryAttr, kind);
  }
});

function renderCategory(categoryAttr, kind) {
  const grid = document.querySelector(`.menu-section[data-category="${categoryAttr}"] .dishes-grid`);
  if (!grid) return;

  grid.innerHTML = "";

  window.dishes
    .filter(d => {
      const cat = d.category === "main-course" ? "main" : d.category;
      return cat === categoryAttr;
    })
    .filter(d => !kind || d.kind === kind)
    .sort((a, b) => a.name.localeCompare(b.name))
    .forEach(dish => {
      const card = document.createElement("div");
      card.className = "dish-card";
      card.dataset.id = dish.id;
      card.dataset.keyword = dish.keyword;
      card.dataset.category = dish.category;

      card.innerHTML = `
        <img src="${dish.image}" alt="${dish.name}">
        <p class="dish-price">${dish.price} ₽</p>
        <p class="dish-name">${dish.name}</p>
        <p class="dish-weight">${dish.count}</p>
        <button class="dish-add" type="button">Добавить</button>
      `;

      grid.appendChild(card);
    });
}
