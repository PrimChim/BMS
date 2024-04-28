fetch('/billing/api/view-bills/')
    .then(response => response.json())
    .then(data => {
        let table = document.getElementById('bill-table');
        let condition = true;
        for (let bill of data) {
            if (condition) {
                let row = `<tr>
                <td class="w-1/3 text-left py-3 px-4">${bill.id}</td>
                <td class="w-1/3 text-left py-3 px-4">${bill.total_price}</td>
                <td class="text-left py-3 px-4">${bill.invoice_date}</td>
                <td class="text-center py-3 px-4"><button onClick='openBill(${bill.id})'>
                <i class="fas fa-eye mt-3"></i>
                </button></td>
            </tr>`;
                table.innerHTML += row;
                condition = false;
            } else {
                let row = `<tr class="bg-gray-200">
                <td class="w-1/3 text-left py-3 px-4">${bill.id}</td>
                <td class="w-1/3 text-left py-3 px-4">${bill.total_price}</td>
                <td class="text-left py-3 px-4">${bill.invoice_date}</td>
                <td class="text-center py-3 px-4"><button onClick='openBill(${bill.id})'>
                <i class="fas fa-eye mt-3"></i>
                </button></td>
            </tr>`;
                table.innerHTML += row;
                condition = true;
            }
        }
    }
    );

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
            let condition = true;
            table.innerHTML = ``;
            for (let bill of data) {
                if (condition) {
                    let row = `<tr>
                <td class="w-1/3 text-left py-3 px-4">${bill.id}</td>
                <td class="w-1/3 text-left py-3 px-4">${bill.total_price}</td>
                <td class="text-left py-3 px-4">${bill.invoice_date}</td>
                <td class="text-center py-3 px-4"><button onClick='openBill(${bill.id})'>
                <i class="fas fa-eye mt-3"></i>
                </button></td>
            </tr>`;
                    table.innerHTML += row;
                    condition = false;
                } else {
                    let row = `<tr class="bg-gray-200">
                <td class="w-1/3 text-left py-3 px-4">${bill.id}</td>
                <td class="w-1/3 text-left py-3 px-4">${bill.total_price}</td>
                <td class="text-left py-3 px-4">${bill.invoice_date}</td>
                <td class="text-center py-3 px-4"><button onClick='openBill(${bill.id})'>
                <i class="fas fa-eye mt-3"></i>
                </button></td>
            </tr>`;
                    table.innerHTML += row;
                    condition = true;
                }
            }
        }
        );
}

function openBill(id) {
    fetch('/billing/api/view-bills/' + id)
        .then(response => response.json())
        .then(data => {

            let customerDetails = data[data.length - 1];

            console.log(customerDetails);

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
            for (let product of data) {
                let row = '';
                if (condition) {
                    row = `<tr>
                    <td class="w-1/3 text-left py-3 px-4">${product.item}</td>
                    <td class="w-1/3 text-left py-3 px-4">${product.quantity}</td>
                    <td class="text-left py-3 px-4">${product.price}</td>
                    <td class="text-left py-3 px-4">${product.price * product.quantity}</td>
                    </tr>`;
                    condition = false;
                } else {
                    row = `<tr class="bg-gray-200">
                    <td class="w-1/3 text-left py-3 px-4">${product.item}</td>
                    <td class="w-1/3 text-left py-3 px-4">${product.quantity}</td>
                    <td class="text-left py-3 px-4">${product.price}</td>
                    <td class="text-left py-3 px-4">${product.price * product.quantity}</td>
                    </tr>`;
                    condition = true;
                }
                table.innerHTML += row;
            }

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

                    <span class="font-semibold">${customerDetails.total}</span>
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
            actions.innerHTML = `
            <button class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded mt-5" onClick='printBill(${id})'>Print</button>
            <button class="bg-blue-400 hover:bg-blue-600 text-white font-bold py-2 px-4 rounded mt-5" onClick='window.location.reload()'>Back</button>
            <button class="bg-red-500 hover:bg-red-700 text-white font-bold py-2 px-4 rounded mt-5" onClick='cancelBill(${id})'>Cancel</button>
            `;
            main.appendChild(actions);


        }
        );
}

function cancelBill(id) {
    fetch('/billing/api/cancel-bill/' + id, {
        method: 'GET'
    })
        .then(response => response.json())
        .then(data => {
            console.log(data);
            window.location.reload();
        });
}