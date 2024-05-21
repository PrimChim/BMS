let itemsTable = document.getElementById('items-table');

function items(page = 1) {
    itemsTable.innerHTML = '';
    fetch('/billing/api/get-items?page=' + page)
        .then(response => response.json())
        .then(data => {
            data.pop();
            data.forEach(item => {
                let row = itemsTable.insertRow(-1);
                let cell1 = row.insertCell(0);
                let cell2 = row.insertCell(1);
                let cell3 = row.insertCell(2);
                let cell4 = row.insertCell(3);

                cell1.innerHTML = item.name;
                cell2.innerHTML = item.price;
                cell3.innerHTML = item.stock;
                cell4.innerHTML = `<button onClick='openItem(${item.id})'><i class="fas fa-eye mt-3"><i></button>`;

                cell1.classList.add('w-3/6', 'text-left', 'py-3', 'px-4');
                cell2.classList.add('w-1/6', 'text-left', 'py-3', 'px-4');
                cell3.classList.add('w-1/6', 'text-center', 'py-3', 'px-4');
                cell4.classList.add('w-1/6', 'text-center', 'py-3', 'px-4');

                if (itemsTable.rows.length % 2 === 0) {
                    row.classList.add('bg-gray-200');
                }
            })
        });
}

items();

// search items 
let searchForm = document.getElementById('search-form');

searchForm.addEventListener('submit', function (e) {
    e.preventDefault();
    let search = document.getElementById('search').value;
    fetch(`/billing/api/get-items?search=${search}`)
        .then(response => response.json())
        .then(data => {
            data.pop();
            itemsTable.innerHTML = '';
            data.forEach(item => {
                let row = itemsTable.insertRow(-1);
                let cell1 = row.insertCell(0);
                let cell2 = row.insertCell(1);
                let cell3 = row.insertCell(2);

                cell1.innerHTML = item.name;
                cell2.innerHTML = item.price;
                cell3.innerHTML = `<button onClick='openItem(${item.id})'><i class="fas fa-eye mt-3"><i></button>`;

                cell1.classList.add('w-3/5', 'text-left', 'py-3', 'px-4');
                cell2.classList.add('w-1/5', 'text-left', 'py-3', 'px-4');
                cell3.classList.add('w-1/5', 'text-center', 'py-3', 'px-4');

                if (itemsTable.rows.length % 2 === 0) {
                    row.classList.add('bg-gray-200');
                }
            })
        });
}
);

// add items form submit handler
let addItemForm = document.getElementById('add-item-form');

addItemForm.addEventListener('submit', function (e) {
    e.preventDefault();
    let formData = new FormData(addItemForm);
    fetch('/billing/api/add-items/', {
        method: 'POST',
        body: formData
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alertify.set('notifier', 'position', 'top-right');
                alertify.set('notifier', 'delay', 3);
                alertify.success(data.success);
                addItemForm.reset();
                dialog.close();
                items();
            } else {
                alertify.set('notifier', 'position', 'top-right');
                alertify.set('notifier', 'delay', 3);
                alertify.error(data.error);
            }
        });
})

// item details popup
let modal = document.querySelector('[item-modal]');

function openItem(id) {
    let itemId = document.getElementById('item-id');
    let name = document.getElementById('item-name');
    let price = document.getElementById('item-price');
    let stock = document.getElementById('item-stock');
    let description = document.getElementById('item-description');

    itemId.value = id;

    modal.showModal();

    fetch(`/billing/api/get-items?id=${id}`)
        .then(response => response.json())
        .then(data => {
            name.value = data.name;
            price.value = data.price;
            stock.value = data.stock;
            description.value = data.description;
        });

}

let closeButton = document.getElementById('close-button');

closeButton.addEventListener('click', function () {
    modal.close();
});

// update item details
let itemsForm = document.getElementById('item-details-form');

itemsForm.addEventListener('submit', function (e) {
    e.preventDefault();
    let id = document.getElementById('item-id').value;
    let formData = new FormData(itemsForm);
    fetch(`/billing/api/update-item/${id}`, {
        method: 'POST',
        body: formData
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alertify.set('notifier', 'position', 'top-right');
                alertify.set('notifier', 'delay', 3);
                alertify.success(data.success);
                modal.close();
                items();
            } else {
                alertify.set('notifier', 'position', 'top-right');
                alertify.set('notifier', 'delay', 3);
                alertify.error(data.error);
            }
        });
});
