const LOCAL_API =
  "http://lab7-api.std-900.ist.mospolytech.ru/api/dishes?api_key=4733eaf4-4488-484d-bab6-70863c53ffc9";

const PUBLIC_API =
  "https://edu.std-900.ist.mospolytech.ru/labs/api/dishes";

const API_URL =
  location.hostname.includes("github.io")
    ? PUBLIC_API
    : LOCAL_API;

let dishes = [];
const CATEGORY_MAP = {
  soup: "soup",
  main_course: "main",
  salad: "salad",
  drink: "drink",
  dessert: "dessert"
};
/* =========================
   LOAD DISHES FROM API
   ========================= */
async function loadDishes() {
  try {
    const response = await fetch(API_URL);

    if (!response.ok) {
      throw new Error("Ошибка загрузки блюд");
    }

    dishes = await response.json();
    renderAllCategories();
  } catch (err) {
    console.error(err);
    alert("Не удалось загрузить меню");
  }
}

/* =========================
   INITIAL RENDER
   ========================= */
function renderAllCategories() {
  const grids = {
    soup: document.querySelector('.menu-section[data-category="soup"] .dishes-grid'),
    main: document.querySelector('.menu-section[data-category="main"] .dishes-grid'),
    salad: document.querySelector('.menu-section[data-category="salad"] .dishes-grid'),
    drink: document.querySelector('.menu-section[data-category="drink"] .dishes-grid'),
    dessert: document.querySelector('.menu-section[data-category="dessert"] .dishes-grid')
  };

  Object.values(grids).forEach(grid => grid.innerHTML = "");

  dishes
    .slice()
    .sort((a, b) => a.name.localeCompare(b.name))
    .forEach(dish => {
      const normalizedCategory = CATEGORY_MAP[dish.category];
      const grid = grids[normalizedCategory];
      if (!grid) return;

      const card = document.createElement("div");
      card.className = "dish-card";
      card.dataset.dish = dish.keyword;

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

/* =========================
   FILTERS
   ========================= */
document.addEventListener("click", (e) => {
  const btn = e.target.closest(".filters button");
  if (!btn) return;

  const section = btn.closest(".menu-section");
  const category = section.dataset.category;
  const kind = btn.dataset.kind;

  const active = btn.classList.contains("active");

  section.querySelectorAll(".filters button")
    .forEach(b => b.classList.remove("active"));

  if (active) {
    renderCategory(category);
    return;
  }

  btn.classList.add("active");
  renderCategory(category, kind);
});

function renderCategory(category, kind = null) {
  const grid = document.querySelector(
    `.menu-section[data-category="${category}"] .dishes-grid`
  );

  grid.innerHTML = "";

  dishes
    .filter(d => d.category === category)
    .filter(d => !kind || d.kind === kind)
    .sort((a, b) => a.name.localeCompare(b.name))
    .forEach(dish => {
      const card = document.createElement("div");
      card.className = "dish-card";
      card.dataset.dish = dish.keyword;

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

/* =========================
   BOOTSTRAP
   ========================= */
document.addEventListener("DOMContentLoaded", loadDishes);
