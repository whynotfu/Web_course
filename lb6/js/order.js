const selected = { soup: null, main: null, drink: null };

document.addEventListener("click", (e) => {
  const btn = e.target.closest(".dish-add");
  if (!btn) return;

  const card = btn.closest(".dish-card");
  if (!card) return;

  const keyword = card.dataset.dish;
  if (!keyword) return;

  const dish = dishes.find(d => d.keyword === keyword);
  if (!dish) return;

  selected[dish.category] = dish;
  renderOrder();
});

function renderOrder() {
  const emptyText = document.querySelector(".order-summary .empty");
  const totalBlock = document.querySelector(".order-summary .total");
  const totalPriceEl = document.getElementById("total-price");

  let total = 0;
  let any = false;

  for (const [category, dish] of Object.entries(selected)) {
    const block = document.querySelector(`.order-summary .category[data-category="${category}"]`);
    const value = block.querySelector(".value");

    if (dish) {
      value.textContent = `${dish.name} — ${dish.price} ₽`;
      total += dish.price;
      any = true;
    } else {
      value.textContent =
        category === "soup" ? "Soup not selected" :
        category === "main" ? "Main course not selected" :
        "Drink not selected";
    }
  }

  emptyText.style.display = any ? "none" : "block";

  if (any) {
    totalBlock.classList.remove("hidden");
    totalPriceEl.textContent = String(total);
  } else {
    totalBlock.classList.add("hidden");
    totalPriceEl.textContent = "0";
  }
}

const lunchCombos = [
  ["soup", "main", "salad", "drink"],
  ["soup", "main", "drink"],
  ["soup", "salad", "drink"],
  ["main", "salad", "drink"],
  ["main", "drink"]
];
document.querySelector("form").addEventListener("submit", (e) => {
  const chosen = Object.entries(selected)
    .filter(([, v]) => v)
    .map(([k]) => k);

  if (!isValidLunch(chosen)) {
    e.preventDefault();
    showNotification(getNotificationText(chosen));
  }
});

function isValidLunch(chosen) {
  return lunchCombos.some(combo =>
    combo.every(item => chosen.includes(item))
  );
}
function getNotificationText(chosen) {
  if (chosen.length === 0)
    return "Nothing selected. Choose dishes to order";

  if (!chosen.includes("drink") &&
      (chosen.includes("soup") || chosen.includes("main")))
    return "Choose a drink";

  if (chosen.includes("soup") &&
      !chosen.includes("main") &&
      !chosen.includes("salad"))
    return "Choose main course or salad/starter";

  if (chosen.includes("salad") &&
      !chosen.includes("soup") &&
      !chosen.includes("main"))
    return "Choose soup or main course";

  if (chosen.includes("drink") &&
      !chosen.includes("main"))
    return "Choose main course";

  return "Choose missing dishes";
}
function showNotification(text) {
  const overlay = document.createElement("div");
  overlay.className = "notification-overlay";

  overlay.innerHTML = `
    <div class="notification">
      <p>${text}</p>
      <button class="ok-btn">OK</button>
    </div>
  `;

  overlay.querySelector(".ok-btn").onclick = () => overlay.remove();
  document.body.appendChild(overlay);
}
