/* =========================
   ORDER LOGIC (COMBO ONLY)
   ========================= */

/* выбранные блюда */
const selected = {
  soup: null,
  main: null,
  salad: null,
  drink: null,
  dessert: null
};

/* доступные комбо */
const lunchCombos = [
  ["soup", "main", "salad", "drink"],
  ["soup", "main", "drink"],
  ["soup", "salad", "drink"],
  ["main", "salad", "drink"],
  ["main", "drink"]
];

/* =========================
   ADD DISH
   ========================= */
document.addEventListener("click", (e) => {
  const btn = e.target.closest(".dish-add");
  if (!btn) return;

  const card = btn.closest(".dish-card");
  if (!card) return;

  const keyword = card.dataset.dish;
  const dish = dishes.find(d => d.keyword === keyword);
  if (!dish) return;

  selected[dish.category] = dish;
  renderOrder();
});

/* =========================
   RENDER ORDER SUMMARY
   ========================= */
function renderOrder() {
  const emptyText = document.querySelector(".order-summary .empty");
  const totalBlock = document.querySelector(".order-summary .total");
  const totalPriceEl = document.getElementById("total-price");

  let total = 0;
  let anySelected = false;

  for (const [category, dish] of Object.entries(selected)) {
    const block = document.querySelector(
      `.order-summary .category[data-category="${category}"]`
    );
    if (!block) continue;

    const value = block.querySelector(".value");

    if (dish) {
      value.textContent = `${dish.name} — ${dish.price} ₽`;
      total += dish.price;
      anySelected = true;
    } else {
      const emptyTextMap = {
        soup: "Soup not selected",
        main: "Main course not selected",
        salad: "Salad / starter not selected",
        drink: "Drink not selected",
        dessert: "Dessert not selected"
      };
      value.textContent = emptyTextMap[category];
    }
  }

  emptyText.style.display = anySelected ? "none" : "block";

  if (anySelected) {
    totalBlock.classList.remove("hidden");
    totalPriceEl.textContent = total;
  } else {
    totalBlock.classList.add("hidden");
    totalPriceEl.textContent = "0";
  }
}

/* =========================
   COMBO VALIDATION HELPERS
   ========================= */

/* что выбрано (десерт не участвует) */
function getChosenCategories() {
  return Object.entries(selected)
    .filter(([key, value]) => value && key !== "dessert")
    .map(([key]) => key);
}

/* ближайшее комбо (минимум недостающих позиций) */
function findClosestCombo(chosen) {
  let best = null;

  for (const combo of lunchCombos) {
    const missing = combo.filter(item => !chosen.includes(item));

    if (!best || missing.length < best.missing.length) {
      best = { combo, missing };
    }
  }

  return best;
}

/* текст для поп-апа */
function getComboErrorText(chosen) {
  if (chosen.length === 0) {
    return "Вы ничего не выбрали";
  }

  const { missing } = findClosestCombo(chosen);

  const names = {
    soup: "soup",
    main: "main course",
    salad: "salad",
    drink: "drink"
  };

  if (missing.length === 1) {
    return `You have not choose ${names[missing[0]]} for combo`;
  }

  return "Choose dish for combo";
}

/* =========================
   FORM SUBMIT
   ========================= */
document.querySelector("form").addEventListener("submit", (e) => {
  const chosen = getChosenCategories();

  const isValid = lunchCombos.some(combo =>
    combo.every(item => chosen.includes(item))
  );

  if (!isValid) {
    e.preventDefault();
    showNotification(getComboErrorText(chosen));
  }
});

/* =========================
   POP-UP (UI)
   ========================= */
function showNotification(text) {
  const overlay = document.createElement("div");
  overlay.className = "notification-overlay";

  overlay.innerHTML = `
    <div class="notification">
      <p>${text}</p>
      <button class="ok-btn">Окей 👌</button>
    </div>
  `;

  overlay.querySelector(".ok-btn").onclick = () => overlay.remove();
  document.body.appendChild(overlay);
}
