const sections = {
  soup: document.querySelectorAll(".menu-section")[0].querySelector(".dishes-grid"),
  main: document.querySelectorAll(".menu-section")[1].querySelector(".dishes-grid"),
  drink: document.querySelectorAll(".menu-section")[2].querySelector(".dishes-grid")
};

// очистка статического HTML
Object.values(sections).forEach(s => s.innerHTML = "");

dishes
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
      <button class="dish-add">Добавить</button>
    `;

    sections[dish.category].appendChild(card);
  });
