document.addEventListener("DOMContentLoaded", function () {
    const tableModal = document.getElementById("tableModal");
    const tableModalLabel = document.getElementById("tableModalLabel");
    const tableStatus = document.getElementById("tableStatus");
    const selectedTableId = document.getElementById("selectedTableId");
    const orderItemsDiv = document.getElementById("orderItems");
    const orderTotalEl = document.getElementById("orderTotal");
    const addProductForm = document.getElementById("addProductForm");
    const payOrderButton = document.getElementById("payOrderButton");

    function getCsrfToken() {
        return document.querySelector("[name=csrfmiddlewaretoken]").value;
    }

    function renderOrder(data) {
        if (!data.items || data.items.length === 0) {
            orderItemsDiv.innerHTML =
                '<div class="alert alert-secondary">No products added yet.</div>';
        } else {
            orderItemsDiv.innerHTML = data.items.map(function (item) {
                return `
                    <div class="order-item d-flex justify-content-between align-items-center">
                        <span>${item.quantity} x ${item.product_name}</span>
                        <div>
                            <span class="me-3">${item.subtotal} ден.</span>
                            <button
                                type="button"
                                class="btn btn-sm btn-outline-danger remove-item-btn"
                                data-item-id="${item.id}"
                            >
                                Delete
                            </button>
                        </div>
                    </div>
                `;
            }).join("");
        }

        orderTotalEl.textContent = data.total + " ден.";

        document.querySelectorAll(".remove-item-btn").forEach(function (btn) {
            btn.addEventListener("click", function () {
                removeItem(btn.dataset.itemId);
            });
        });
    }

    function loadOrder(tableId) {
        fetch(`/api/tables/${tableId}/order/`)
            .then((response) => response.json())
            .then(renderOrder);
    }

    function removeItem(itemId) {
        const tableId = selectedTableId.value;

        fetch(`/api/order-items/${itemId}/remove/`, {
            method: "POST",
            headers: { "X-CSRFToken": getCsrfToken() },
        })
            .then((response) => response.json())
            .then(renderOrder)
            .then(() => loadOrder(tableId));
    }

    tableModal.addEventListener("show.bs.modal", function (event) {
        const button = event.relatedTarget;

        const tableId = button.getAttribute("data-table-id");
        const tableNumber = button.getAttribute("data-table-number");
        const status = button.getAttribute("data-table-status").trim();

        tableModalLabel.textContent = `Table ${tableNumber}`;
        tableStatus.textContent = status;
        selectedTableId.value = tableId;

        loadOrder(tableId);
    });

    addProductForm.addEventListener("submit", function (event) {
        event.preventDefault();

        const tableId = selectedTableId.value;
        const productId = document.getElementById("product").value;
        const quantity = document.getElementById("quantity").value;

        fetch(`/api/tables/${tableId}/order/add/`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": getCsrfToken(),
            },
            body: JSON.stringify({
                product_id: productId,
                quantity: quantity,
            }),
        })
            .then((response) => response.json())
            .then(function (data) {
                if (data.error) {
                    alert(data.error);
                    return;
                }

                renderOrder(data);
                addProductForm.reset();
            });
    });

    payOrderButton.addEventListener("click", function () {
        const tableId = selectedTableId.value;

        if (!confirm("Mark this table's order as paid?")) {
            return;
        }

        fetch(`/api/tables/${tableId}/order/pay/`, {
            method: "POST",
            headers: { "X-CSRFToken": getCsrfToken() },
        })
            .then((response) => response.json())
            .then(function () {
                location.reload();
            });
    });
});