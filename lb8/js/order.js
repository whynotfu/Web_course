// Выбранные блюда (объекты из API)
const selected = {
  soup: null,
  main: null,
  salad: null,
  drink: null,
  dessert: null
};

// Допустимые комбо
const combos = [
  ["soup", "main", "salad", "drink"],
  ["soup", "main", "drink"],
  ["soup", "salad", "drink"],
  ["main", "salad", "drink"],
  ["main", "drink"]
];

// Когда блюда загружены - восстанавливаем заказ из localStorage
window.addEventListener("dishes-loaded", () => {
  const order = window.getOrder();

  for (const category in order) {
    const id = order[category];
    const dish = window.dishes.find(d => d.id == id);
    if (dish) {
      const cat = dish.category === "main-course" ? "main" : dish.category;
      selected[cat] = dish;
    }
  }

  render();
  highlightSelected();
});

// Клик по кнопке "Добавить"
document.addEventListener("click", (e) => {
  const btn = e.target.closest(".dish-add");
  if (!btn) return;

  const card = btn.closest(".dish-card");
  const id = card.dataset.id;
  const dish = window.dishes.find(d => d.id == id);
  if (!dish) return;

  const category = dish.category === "main-course" ? "main" : dish.category;
  selected[category] = dish;
  window.setDish(category, dish.id);

  render();
  highlightSelected();
});

// Клик по кнопке "Удалить" (на order.html)
document.addEventListener("click", (e) => {
  const btn = e.target.closest(".dish-remove");
  if (!btn) return;

  const card = btn.closest(".dish-card");
  const id = card.dataset.id;
  const dish = window.dishes.find(d => d.id == id);
  if (!dish) return;

  const category = dish.category === "main-course" ? "main" : dish.category;
  selected[category] = null;
  window.removeDish(category);

  render();
});

// Подсветка выбранных блюд
function highlightSelected() {
  document.querySelectorAll(".dish-card").forEach(card => {
    card.classList.remove("selected");
  });

  for (const dish of Object.values(selected)) {
    if (dish) {
      const card = document.querySelector(`.dish-card[data-id="${dish.id}"]`);
      if (card) card.classList.add("selected");
    }
  }
}

// Главная функция рендера
function render() {
  renderCheckoutPanel();
  renderOrderSummary();
  renderOrderItemsList();
}

// Панель внизу на lunch.html
function renderCheckoutPanel() {
  const panel = document.querySelector(".checkout-panel");
  if (!panel) return;

  let total = 0;
  let hasAny = false;

  for (const dish of Object.values(selected)) {
    if (dish) {
      total += dish.price;
      hasAny = true;
    }
  }

  panel.classList.toggle("hidden", !hasAny);

  const totalEl = panel.querySelector(".checkout-total");
  if (totalEl) totalEl.textContent = `${total} ₽`;

  const link = panel.querySelector(".checkout-link");
  if (link) {
    const valid = isComboValid();
    link.classList.toggle("disabled", !valid);
    link.style.pointerEvents = valid ? "auto" : "none";
    link.style.opacity = valid ? "1" : "0.5";
  }
}

// Сводка заказа на order.html (справа)
function renderOrderSummary() {
  const summary = document.querySelector(".order-summary");
  if (!summary) return;

  let total = 0;
  let hasAny = false;

  for (const category in selected) {
    const block = summary.querySelector(`.category[data-category="${category}"]`);
    if (!block) continue;

    const value = block.querySelector(".value");
    if (!value) continue;

    const dish = selected[category];
    if (dish) {
      value.textContent = `${dish.name} — ${dish.price} ₽`;
      total += dish.price;
      hasAny = true;
    } else {
      value.textContent = "Не выбрано";
    }
  }

  const emptyText = summary.querySelector(".empty");
  if (emptyText) emptyText.style.display = hasAny ? "none" : "block";

  const totalBlock = summary.querySelector(".total");
  if (totalBlock) totalBlock.classList.toggle("hidden", !hasAny);

  const totalPrice = document.getElementById("total-price");
  if (totalPrice) totalPrice.textContent = total;
}

// Список блюд с кнопками "Удалить" на order.html (слева)
function renderOrderItemsList() {
  const container = document.querySelector(".order-items-list");
  if (!container) return;

  container.innerHTML = "";

  const dishes = Object.values(selected).filter(d => d);

  if (dishes.length === 0) {
    container.innerHTML = `
      <p class="empty-message">Ничего не выбрано. Чтобы добавить блюда в заказ, перейдите на страницу <a href="lunch.html">Собрать ланч</a>.</p>
    `;
    return;
  }

  dishes.forEach(dish => {
    const card = document.createElement("div");
    card.className = "dish-card";
    card.dataset.id = dish.id;

    card.innerHTML = `
      <img src="${dish.image}" alt="${dish.name}">
      <p class="dish-price">${dish.price} ₽</p>
      <p class="dish-name">${dish.name}</p>
      <p class="dish-weight">${dish.count}</p>
      <button class="dish-remove" type="button">Удалить</button>
    `;

    container.appendChild(card);
  });
}

// Проверка валидности комбо
function isComboValid() {
  const chosen = [];
  for (const cat in selected) {
    if (selected[cat] && cat !== "dessert") {
      chosen.push(cat);
    }
  }

  return combos.some(combo =>
    combo.every(item => chosen.includes(item))
  );
}

// Текст ошибки для комбо
function getComboError() {
  const chosen = [];
  for (const cat in selected) {
    if (selected[cat] && cat !== "dessert") {
      chosen.push(cat);
    }
  }

  if (chosen.length === 0) {
    return "Вы ничего не выбрали. Необходимо выбрать блюда.";
  }

  // Находим ближайшее комбо
  let best = null;
  for (const combo of combos) {
    const missing = combo.filter(item => !chosen.includes(item));
    if (!best || missing.length < best.missing.length) {
      best = { combo, missing };
    }
  }

  const names = {
    soup: "суп",
    main: "главное блюдо",
    salad: "салат",
    drink: "напиток"
  };

  if (best.missing.length === 1) {
    return `Выберите ${names[best.missing[0]]}`;
  }

  const text = best.missing.map(m => names[m]).join(", ");
  return `Выберите: ${text}`;
}

// Модальное окно
function showNotification(text) {
  const overlay = document.createElement("div");
  overlay.className = "notification-overlay";

  overlay.innerHTML = `
    <div class="notification">
      <p>${text}</p>
      <button class="ok-btn">Окей</button>
    </div>
  `;

  overlay.querySelector(".ok-btn").onclick = () => overlay.remove();
  overlay.onclick = (e) => {
    if (e.target === overlay) overlay.remove();
  };

  document.body.appendChild(overlay);
}

// Отправка формы
const form = document.querySelector("form");
if (form) {
  form.addEventListener("submit", async (e) => {
    e.preventDefault();

    // Проверка комбо
    if (!isComboValid()) {
      showNotification(getComboError());
      return;
    }

    // Сбор данных
    const formData = {
      full_name: document.getElementById("name")?.value || "",
      email: document.getElementById("email")?.value || "",
      subscribe: document.getElementById("newsletter")?.checked ? 1 : 0,
      phone: document.getElementById("phone")?.value || "",
      delivery_address: document.getElementById("address")?.value || "",
      delivery_type: document.querySelector('input[name="delivery_type"]:checked')?.value || "now",
      delivery_time: document.getElementById("delivery_time")?.value || "",
      comment: document.getElementById("comment")?.value || ""
    };

    // Добавляем id блюд в форму
    if (selected.soup) formData.soup_id = selected.soup.id;
    if (selected.main) formData.main_course_id = selected.main.id;
    if (selected.salad) formData.salad_id = selected.salad.id;
    if (selected.drink) formData.drink_id = selected.drink.id;
    if (selected.dessert) formData.dessert_id = selected.dessert.id;

    // Проверки
    if (!formData.full_name) {
      showNotification("Заполните поле 'Имя'");
      return;
    }
    if (!formData.email) {
      showNotification("Заполните поле 'Email'");
      return;
    }
    if (!formData.phone) {
      showNotification("Заполните поле 'Телефон'");
      return;
    }
    if (!formData.delivery_address) {
      showNotification("Заполните поле 'Адрес'");
      return;
    }
    if (!formData.drink_id) {
      showNotification("Напиток обязателен для заказа");
      return;
    }

    if (formData.delivery_type === "by_time") {
      if (!formData.delivery_time) {
        showNotification("Укажите время доставки");
        return;
      }
    } else {
      formData.delivery_time = "";
    }

    // Удаляем пустые поля
    Object.keys(formData).forEach(key => {
      if (!formData[key] && formData[key] !== 0) {
        delete formData[key];
      }
    });

    // Отправка
    try {
      const API_KEY = "4733eaf4-4488-484d-bab6-70863c53ffc9";
      const API_URL = `http://lab8-api.std-900.ist.mospolytech.ru/labs/api/orders?api_key=${API_KEY}`;

      const response = await fetch(API_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(formData)
      });

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.error || "Ошибка при создании заказа");
      }

      const result = await response.json();

      // Очистка заказа
      window.clearOrder();
      for (const key in selected) {
        selected[key] = null;
      }

      showNotification("Заказ успешно оформлен! ID заказа: " + result.id);

      form.reset();
      render();

    } catch (error) {
      showNotification("Ошибка: " + error.message);
    }
  });
}

// Первичный рендер
render();
