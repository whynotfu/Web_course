document.addEventListener("DOMContentLoaded", () => {
  // контейнеры для категорий
const grids = {
  soup: document.querySelector('.menu-section[data-category="soup"] .dishes-grid'),
  main: document.querySelector('.menu-section[data-category="main"] .dishes-grid'),
  salad: document.querySelector('.menu-section[data-category="salad"] .dishes-grid'),
  drink: document.querySelector('.menu-section[data-category="drink"] .dishes-grid'),
  dessert: document.querySelector('.menu-section[data-category="dessert"] .dishes-grid'),
};


  // проверка и очистка
  for (const key of Object.keys(grids)) {
    if (!grids[key]) {
      throw new Error(`Нет контейнера для категории: ${key}`);
    }
    grids[key].innerHTML = "";
  }

  // сортировка по алфавиту
  const sorted = [...dishes].sort((a, b) =>
    a.name.localeCompare(b.name)
  );

  // рендер карточек
  for (const dish of sorted) {
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

    // защита от неправильной категории
    if (!grids[dish.category]) {
      console.warn("Неизвестная категория:", dish.category, dish);
      continue;
    }

    grids[dish.category].appendChild(card);
  }
});


document.addEventListener("click", (e) => {
  const filterBtn = e.target.closest(".filters button");
  if (!filterBtn) return;

  const section = filterBtn.closest(".menu-section");
  const category = section.dataset.category;
  const kind = filterBtn.dataset.kind;

  const isActive = filterBtn.classList.contains("active");

  // сброс всех фильтров в секции
  section.querySelectorAll(".filters button")
    .forEach(b => b.classList.remove("active"));

  if (isActive) {
    renderCategory(category);
    return;
  }

  filterBtn.classList.add("active");
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
