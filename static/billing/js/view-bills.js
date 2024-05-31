let table = document.getElementById('bill-table');
function bills(page = 1) {
    table.innerHTML = '';
    fetch('/billing/api/view-bills?page=' + page)
        .then(response => response.json())
        .then(data => {
            data.pop();
            data.forEach(bill => {
                let row = table.insertRow(-1);
                let cell1 = row.insertCell(0);
                let cell2 = row.insertCell(1);
                let cell3 = row.insertCell(2);
                let cell4 = row.insertCell(3);
                let cell5 = row.insertCell(4);

                cell1.innerHTML = bill.bill_no;
                cell2.innerHTML = `Rs. ${bill.total_price}`;
                cell3.innerHTML = bill.customer_name;
                cell4.innerHTML = bill.invoice_date;
                cell5.innerHTML = `<button onClick='openBill(${bill.id})'><i class="fas fa-eye mt-3"><i></button>`;

                cell1.classList.add('w-1/4', 'text-left', 'py-3', 'px-4');
                cell2.classList.add('w-1/4', 'text-left', 'py-3', 'px-4');
                cell3.classList.add('w-1/4', 'text-left', 'py-3', 'px-4');
                cell4.classList.add('text-left', 'py-3', 'px-4');
                cell5.classList.add('text-center', 'py-3', 'px-4');

                if (table.rows.length % 2 === 0) {
                    row.classList.add('bg-gray-200');
                }
            })
        }
        );
}

bills();

function cancelledBills() {
    let csrf = document.querySelector('input[name=csrfmiddlewaretoken]').value;
    fetch('/billing/api/view-bills/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrf
        }
    })
        .then(response => response.json())
        .then(data => {
            let table = document.getElementById('bill-table');
            table.innerHTML = ``;
            data.forEach(bill => {
                let row = table.insertRow(-1);

                let cell1 = row.insertCell(0);
                let cell2 = row.insertCell(1);
                let cell3 = row.insertCell(2);
                let cell4 = row.insertCell(3);
                let cell5 = row.insertCell(4);

                cell1.innerHTML = bill.id;
                cell2.innerHTML = `Rs. ${bill.total_price}`;
                cell3.innerHTML = bill.customer_id;
                cell4.innerHTML = bill.invoice_date;
                cell5.innerHTML = `<button onClick='openBill(${bill.id})'><i class="fas fa-eye mt-3"><i></button>`;

                cell1.classList.add('w-1/4', 'text-left', 'py-3', 'px-4');
                cell2.classList.add('w-1/4', 'text-left', 'py-3', 'px-4');
                cell3.classList.add('w-1/4', 'text-left', 'py-3', 'px-4');
                cell4.classList.add('text-left', 'py-3', 'px-4');
                cell5.classList.add('text-center', 'py-3', 'px-4');

                if (table.rows.length % 2 === 0) {
                    row.classList.add('bg-gray-200');
                }
            });
        }
        );
}

function openBill(id) {
    fetch('/billing/api/view-bills/' + id)
        .then(response => response.json())
        .then(data => {

            let customerDetails = data[data.length - 1];

            data.pop()

            let table = document.querySelector('table');
            table.innerHTML = `
            <thead class="bg-gray-800 text-white">
                <tr>
                <th class="w-1/3 text-left py-3 px-4 uppercase font-semibold text-sm">Product</th>
                <th class="w-1/3 text-left py-3 px-4 uppercase font-semibold text-sm">Quantity</th>
                <th class="text-left py-3 px-4 uppercase font-semibold text-sm">Amount</th>
                <th class="text-left py-3 px-4 uppercase font-semibold text-sm">Item Total</th>
            </tr>
            </thead>`;

            let condition = true;
            data.forEach(product => {
                let row = table.insertRow(-1);
                let cell1 = row.insertCell(0);
                let cell2 = row.insertCell(1);
                let cell3 = row.insertCell(2);
                let cell4 = row.insertCell(3);

                cell1.innerHTML = product.item;
                cell2.innerHTML = product.quantity;
                cell3.innerHTML = `Rs. ${product.price}`;
                cell4.innerHTML = `Rs. ${product.price * product.quantity}`;

                cell1.classList.add('w-1/3', 'text-left', 'py-3', 'px-4');
                cell2.classList.add('w-1/3', 'text-left', 'py-3', 'px-4');
                cell3.classList.add('text-left', 'py-3', 'px-4');
                cell4.classList.add('text-left', 'py-3', 'px-4');

                if (table.rows.length % 2 === 0) {
                    row.classList.add('bg-gray-200', 'text-gray-700');
                } else {
                    row.classList.add('bg-white', 'text-gray-700');
                }
            });

            // create new element
            let div = document.createElement('div');
            div.innerHTML = `
            <div class="flex justify-between mt-10">
                <div class="w-1/2">
                    <h3 class="text-lg font-semibold">Customer Details</h3>
                    <p class="mt-2">Name

                    <span class="font-semibold">${customerDetails.billed_to}</span>
                    </p>
                    <p class="mt-2">Pan

                    <span class="font-semibold">${customerDetails.customer_pan}</span>
                    </p>
                </div>
                <div class="w-1/2">
                    <h3 class="text-lg font-semibold">Bill Details</h3>
                    <p class="mt-2">Total Price

                    <span class="font-semibold">Rs. ${customerDetails.total}</span>
                    </p>
                    <p class="mt-2">Invoice Date

                    <span class="font-semibold">${customerDetails.invoice_date}</span>
                    </p>

                </div>
            </div>
            `;
            // append the new element to the main
            let main = document.getElementById('main');
            main.appendChild(div);

            let actions = document.createElement('div');

            if (customerDetails.bill_status === 'cancelled') {
                actions.innerHTML = `
                <button class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded mt-5" onClick='printBill(${id})'>Print</button>
                <button class="bg-blue-400 hover:bg-blue-600 text-white font-bold py-2 px-4 rounded mt-5" onClick='window.location.reload()'>Back</button>
                <button class="bg-red-500 hover:bg-red-700 text-white font-bold py-2 px-4 rounded mt-5" onClick='regularBill(${id})'>Restore</button>
                `;
            } else if (customerDetails.bill_status === 'regular') {
                actions.innerHTML = `
            <button class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded mt-5" onClick='printBill(${id})'>Print</button>
            <button class="bg-blue-400 hover:bg-blue-600 text-white font-bold py-2 px-4 rounded mt-5" onClick='window.location.reload()'>Back</button>
            <button class="bg-red-500 hover:bg-red-700 text-white font-bold py-2 px-4 rounded mt-5" onClick='cancelBill(${id})'>Cancel</button>
            `;
            }
            main.appendChild(actions);
        }
        );
}

function printBill(id) {
// redirect to print page
    window.location.href = '/billing/generate-invoice/' + id;
}

function cancelBill(id) {
    fetch('/billing/api/cancel-bill/' + id, {
        method: 'GET'
    })
        .then(response => response.json())
        .then(data => {
            if (data.message) {
                alertify.set('notifier', 'position', 'top-right');
                alertify.set('notifier', 'delay', 3);
                alertify.success(data.message);
                setTimeout(() => {
                    window.location.reload();
                }, 2000);
            } else if (data.error) {
                alertify.set('notifier', 'position', 'top-right');
                alertify.set('notifier', 'delay', 3);
                alertify.error(data.error);
            }
        });
}

function regularBill(id) {
    fetch('/billing/api/cancel-bill/' + id, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': document.querySelector('input[name=csrfmiddlewaretoken]').value
        }
    })
        .then(response => response.json())
        .then(data => {
            if (data.message) {
                alertify.set('notifier', 'position', 'top-right');
                alertify.set('notifier', 'delay', 3);
                alertify.success(data.message);
                setTimeout(() => {
                    window.location.reload();
                }, 2000);
            } else if (data.error) {
                alertify.set('notifier', 'position', 'top-right');
                alertify.set('notifier', 'delay', 3);
                alertify.error(data.error);
            }
        });
}

// select custoemers
let selectCustomers = document.getElementById('customers-select');

// add customers to select element
function fetchCustomers() {
    let customers = [];
    fetch('/customers')
        .then((response) => response.json())
        .then((data) => {
            customers = data;
            customers.forEach(customer => {
                selectCustomers.innerHTML += `<option value="${customer.pan}">${customer.name}</option>`;
            });
        });
}

fetchCustomers();

selectCustomers.addEventListener('change', function () {
    let customer_pan = this.value;
    fetch('/billing/api/view-bills?customer_pan=' + customer_pan)
        .then(response => response.json())
        .then(data => {
            table.innerHTML = '';
            data.pop();
            data.forEach(bill => {
                let row = table.insertRow(-1);
                let cell1 = row.insertCell(0);
                let cell2 = row.insertCell(1);
                let cell3 = row.insertCell(2);
                let cell4 = row.insertCell(3);
                let cell5 = row.insertCell(4);

                cell1.innerHTML = bill.id;
                cell2.innerHTML = `Rs. ${bill.total_price}`;
                cell3.innerHTML = bill.customer_name;
                cell4.innerHTML = bill.invoice_date;
                cell5.innerHTML = `<button onClick='openBill(${bill.id})'><i class="fas fa-eye mt-3"><i></button>`;

                cell1.classList.add('w-1/4', 'text-left', 'py-3', 'px-4');
                cell2.classList.add('w-1/4', 'text-left', 'py-3', 'px-4');
                cell3.classList.add('w-1/4', 'text-left', 'py-3', 'px-4');
                cell4.classList.add('text-left', 'py-3', 'px-4');
                cell5.classList.add('text-center', 'py-3', 'px-4');

                if (table.rows.length % 2 === 0) {
                    row.classList.add('bg-gray-200');
                }
            })
        }
        );
}
);

