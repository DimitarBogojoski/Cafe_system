document.addEventListener("DOMContentLoaded", function () {
    const tableModal = document.getElementById("tableModal");
    const tableModalLabel = document.getElementById("tableModalLabel");
    const tableStatus = document.getElementById("tableStatus");
    const selectedTableId = document.getElementById("selectedTableId");

    tableModal.addEventListener("show.bs.modal", function (event) {
        const button = event.relatedTarget;

        const tableId = button.getAttribute("data-table-id");
        const tableNumber = button.getAttribute("data-table-number");
        const status = button.getAttribute("data-table-status").trim();

        tableModalLabel.textContent = `Table ${tableNumber}`;
        tableStatus.textContent = status;
        selectedTableId.value = tableId;

        // Later, load the current order here using fetch().
        console.log("Selected table:", tableId);
    });
});