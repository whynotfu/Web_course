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
