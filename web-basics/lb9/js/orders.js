const API_KEY = "4733eaf4-4488-484d-bab6-70863c53ffc9";
const API_BASE = "https://edu.std-900.ist.mospolytech.ru/labs/api";
const DISHES_API = "https://edu.std-900.ist.mospolytech.ru/labs/api/dishes";

let orders = [];
let dishes = [];

// Загрузка данных при загрузке страницы
document.addEventListener("DOMContentLoaded", async () => {
    await loadDishes();
    await loadOrders();
});

// Загрузка блюд для отображения названий
async function loadDishes() {
    try {
        const res = await fetch(DISHES_API);
        if (!res.ok) throw new Error("Ошибка загрузки блюд");
        dishes = await res.json();
    } catch (e) {
        console.error("Не удалось загрузить блюда:", e);
    }
}

// Получить название блюда по id
function getDishName(id) {
    if (!id) return null;
    const dish = dishes.find(d => d.id == id);
    return dish ? dish.name : `Блюдо #${id}`;
}

// Получить цену блюда по id
function getDishPrice(id) {
    if (!id) return 0;
    const dish = dishes.find(d => d.id == id);
    return dish ? dish.price : 0;
}

// Загрузка заказов
async function loadOrders() {
    const container = document.querySelector(".orders-list");
    container.innerHTML = '<p class="loading-message">Загрузка заказов...</p>';

    try {
        const res = await fetch(`${API_BASE}/orders?api_key=${API_KEY}`);
        if (!res.ok) {
            const error = await res.json();
            throw new Error(error.error || "Ошибка загрузки заказов");
        }

        orders = await res.json();

        // Сортировка по дате (новые сначала)
        orders.sort((a, b) => new Date(b.created_at) - new Date(a.created_at));

        renderOrders();
    } catch (e) {
        container.innerHTML = `<p class="error-message">Ошибка: ${e.message}</p>`;
    }
}

// Рендер списка заказов
function renderOrders() {
    const container = document.querySelector(".orders-list");

    if (orders.length === 0) {
        container.innerHTML = '<p class="empty-message">У вас пока нет заказов</p>';
        return;
    }

    container.innerHTML = `
        <table class="orders-table">
            <thead>
                <tr>
                    <th>№</th>
                    <th>Дата оформления</th>
                    <th>Состав заказа</th>
                    <th>Стоимость</th>
                    <th>Доставка</th>
                    <th>Действия</th>
                </tr>
            </thead>
            <tbody>
            </tbody>
        </table>
    `;

    const tbody = container.querySelector("tbody");

    orders.forEach((order, index) => {
        const row = document.createElement("tr");
        row.dataset.id = order.id;

        // Собираем названия блюд
        const dishNames = [];
        if (order.soup_id) dishNames.push(getDishName(order.soup_id));
        if (order.main_course_id) dishNames.push(getDishName(order.main_course_id));
        if (order.salad_id) dishNames.push(getDishName(order.salad_id));
        if (order.drink_id) dishNames.push(getDishName(order.drink_id));
        if (order.dessert_id) dishNames.push(getDishName(order.dessert_id));

        // Вычисляем стоимость
        const totalPrice =
            getDishPrice(order.soup_id) +
            getDishPrice(order.main_course_id) +
            getDishPrice(order.salad_id) +
            getDishPrice(order.drink_id) +
            getDishPrice(order.dessert_id);

        // Время доставки
        let deliveryText = "Как можно скорее (с 7:00 до 23:00)";
        if (order.delivery_type === "by_time" && order.delivery_time) {
            deliveryText = `К ${order.delivery_time}`;
        }

        // Форматируем дату
        const date = new Date(order.created_at);
        const formattedDate = date.toLocaleString("ru-RU", {
            day: "2-digit",
            month: "2-digit",
            year: "numeric",
            hour: "2-digit",
            minute: "2-digit"
        });

        row.innerHTML = `
            <td>${index + 1}</td>
            <td>${formattedDate}</td>
            <td class="dishes-cell">${dishNames.filter(n => n).join(", ")}</td>
            <td>${totalPrice} ₽</td>
            <td>${deliveryText}</td>
            <td class="actions-cell">
                <button class="btn-action btn-view" data-id="${order.id}" title="Подробнее">
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16" fill="currentColor">
                        <path d="M16 8s-3-5.5-8-5.5S0 8 0 8s3 5.5 8 5.5S16 8 16 8zM1.173 8a13.133 13.133 0 0 1 1.66-2.043C4.12 4.668 5.88 3.5 8 3.5c2.12 0 3.879 1.168 5.168 2.457A13.133 13.133 0 0 1 14.828 8c-.058.087-.122.183-.195.288-.335.48-.83 1.12-1.465 1.755C11.879 11.332 10.119 12.5 8 12.5c-2.12 0-3.879-1.168-5.168-2.457A13.134 13.134 0 0 1 1.172 8z"/>
                        <path d="M8 5.5a2.5 2.5 0 1 0 0 5 2.5 2.5 0 0 0 0-5zM4.5 8a3.5 3.5 0 1 1 7 0 3.5 3.5 0 0 1-7 0z"/>
                    </svg>
                </button>
                <button class="btn-action btn-edit" data-id="${order.id}" title="Редактировать">
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16" fill="currentColor">
                        <path d="M12.146.146a.5.5 0 0 1 .708 0l3 3a.5.5 0 0 1 0 .708l-10 10a.5.5 0 0 1-.168.11l-5 2a.5.5 0 0 1-.65-.65l2-5a.5.5 0 0 1 .11-.168l10-10zM11.207 2.5 13.5 4.793 14.793 3.5 12.5 1.207 11.207 2.5zm1.586 3L10.5 3.207 4 9.707V10h.5a.5.5 0 0 1 .5.5v.5h.5a.5.5 0 0 1 .5.5v.5h.293l6.5-6.5zm-9.761 5.175-.106.106-1.528 3.821 3.821-1.528.106-.106A.5.5 0 0 1 5 12.5V12h-.5a.5.5 0 0 1-.5-.5V11h-.5a.5.5 0 0 1-.468-.325z"/>
                    </svg>
                </button>
                <button class="btn-action btn-delete" data-id="${order.id}" title="Удалить">
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16" fill="currentColor">
                        <path d="M5.5 5.5A.5.5 0 0 1 6 6v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5zm2.5 0a.5.5 0 0 1 .5.5v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5zm3 .5a.5.5 0 0 0-1 0v6a.5.5 0 0 0 1 0V6z"/>
                        <path fill-rule="evenodd" d="M14.5 3a1 1 0 0 1-1 1H13v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V4h-.5a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1H6a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1h3.5a1 1 0 0 1 1 1v1zM4.118 4 4 4.059V13a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1V4.059L11.882 4H4.118zM2.5 3V2h11v1h-11z"/>
                    </svg>
                </button>
            </td>
        `;

        tbody.appendChild(row);
    });
}

// Обработка кликов по кнопкам действий
document.addEventListener("click", (e) => {
    const viewBtn = e.target.closest(".btn-view");
    const editBtn = e.target.closest(".btn-edit");
    const deleteBtn = e.target.closest(".btn-delete");

    if (viewBtn) {
        openDetailsModal(viewBtn.dataset.id);
    } else if (editBtn) {
        openEditModal(editBtn.dataset.id);
    } else if (deleteBtn) {
        openDeleteModal(deleteBtn.dataset.id);
    }
});

// Модальное окно: Подробнее
function openDetailsModal(orderId) {
    const order = orders.find(o => o.id == orderId);
    if (!order) return;

    // Собираем названия блюд
    const dishNames = [];
    if (order.soup_id) dishNames.push(getDishName(order.soup_id));
    if (order.main_course_id) dishNames.push(getDishName(order.main_course_id));
    if (order.salad_id) dishNames.push(getDishName(order.salad_id));
    if (order.drink_id) dishNames.push(getDishName(order.drink_id));
    if (order.dessert_id) dishNames.push(getDishName(order.dessert_id));

    // Вычисляем стоимость
    const totalPrice =
        getDishPrice(order.soup_id) +
        getDishPrice(order.main_course_id) +
        getDishPrice(order.salad_id) +
        getDishPrice(order.drink_id) +
        getDishPrice(order.dessert_id);

    // Время доставки
    let deliveryText = "Как можно скорее (с 7:00 до 23:00)";
    if (order.delivery_type === "by_time" && order.delivery_time) {
        deliveryText = `К ${order.delivery_time}`;
    }

    // Форматируем дату
    const date = new Date(order.created_at);
    const formattedDate = date.toLocaleString("ru-RU", {
        day: "2-digit",
        month: "2-digit",
        year: "numeric",
        hour: "2-digit",
        minute: "2-digit"
    });

    document.getElementById("detail-date").textContent = formattedDate;
    document.getElementById("detail-name").textContent = order.full_name || "-";
    document.getElementById("detail-email").textContent = order.email || "-";
    document.getElementById("detail-phone").textContent = order.phone || "-";
    document.getElementById("detail-address").textContent = order.delivery_address || "-";
    document.getElementById("detail-delivery").textContent = deliveryText;
    document.getElementById("detail-dishes").textContent = dishNames.filter(n => n).join(", ") || "-";
    document.getElementById("detail-price").textContent = `${totalPrice} ₽`;
    document.getElementById("detail-comment").textContent = order.comment || "-";

    document.getElementById("modal-details").classList.remove("hidden");
}

// Модальное окно: Редактирование
function openEditModal(orderId) {
    const order = orders.find(o => o.id == orderId);
    if (!order) return;

    document.getElementById("edit-id").value = order.id;
    document.getElementById("edit-name").value = order.full_name || "";
    document.getElementById("edit-email").value = order.email || "";
    document.getElementById("edit-phone").value = order.phone || "";
    document.getElementById("edit-address").value = order.delivery_address || "";
    document.getElementById("edit-comment").value = order.comment || "";

    if (order.delivery_type === "by_time") {
        document.getElementById("edit-delivery-time").checked = true;
        document.getElementById("edit-time").value = order.delivery_time || "";
    } else {
        document.getElementById("edit-delivery-now").checked = true;
        document.getElementById("edit-time").value = "";
    }

    document.getElementById("modal-edit").classList.remove("hidden");
}

// Модальное окно: Удаление
function openDeleteModal(orderId) {
    document.getElementById("delete-id").value = orderId;
    document.getElementById("modal-delete").classList.remove("hidden");
}

// Закрытие модальных окон
document.querySelectorAll(".modal-close, .btn-cancel, .btn-ok").forEach(btn => {
    btn.addEventListener("click", () => {
        document.querySelectorAll(".modal-overlay").forEach(modal => {
            modal.classList.add("hidden");
        });
    });
});

// Закрытие по клику на оверлей
document.querySelectorAll(".modal-overlay").forEach(overlay => {
    overlay.addEventListener("click", (e) => {
        if (e.target === overlay) {
            overlay.classList.add("hidden");
        }
    });
});

// Отправка формы редактирования
document.getElementById("edit-form").addEventListener("submit", async (e) => {
    e.preventDefault();

    const orderId = document.getElementById("edit-id").value;
    const deliveryType = document.querySelector('#edit-form input[name="delivery_type"]:checked').value;

    const formData = {
        full_name: document.getElementById("edit-name").value,
        email: document.getElementById("edit-email").value,
        phone: document.getElementById("edit-phone").value,
        delivery_address: document.getElementById("edit-address").value,
        delivery_type: deliveryType,
        delivery_time: deliveryType === "by_time" ? document.getElementById("edit-time").value : "",
        comment: document.getElementById("edit-comment").value
    };

    // Валидация времени
    if (deliveryType === "by_time" && !formData.delivery_time) {
        showToast("Укажите время доставки", "error");
        return;
    }

    try {
        const res = await fetch(`${API_BASE}/orders/${orderId}?api_key=${API_KEY}`, {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(formData)
        });

        if (!res.ok) {
            const error = await res.json();
            throw new Error(error.error || "Ошибка при обновлении заказа");
        }

        document.getElementById("modal-edit").classList.add("hidden");
        showToast("Заказ успешно изменён", "success");
        await loadOrders();

    } catch (e) {
        showToast("Ошибка: " + e.message, "error");
    }
});

// Подтверждение удаления
document.querySelector(".btn-confirm-delete").addEventListener("click", async () => {
    const orderId = document.getElementById("delete-id").value;

    try {
        const res = await fetch(`${API_BASE}/orders/${orderId}?api_key=${API_KEY}`, {
            method: "DELETE"
        });

        if (!res.ok) {
            const error = await res.json();
            throw new Error(error.error || "Ошибка при удалении заказа");
        }

        document.getElementById("modal-delete").classList.add("hidden");
        showToast("Заказ успешно удалён", "success");
        await loadOrders();

    } catch (e) {
        showToast("Ошибка: " + e.message, "error");
    }
});

// Уведомления (toast)
function showToast(message, type = "success") {
    const toast = document.getElementById("toast");
    const toastMessage = toast.querySelector(".toast-message");

    toastMessage.textContent = message;
    toast.className = `toast ${type}`;

    setTimeout(() => {
        toast.classList.add("hidden");
    }, 3000);
}