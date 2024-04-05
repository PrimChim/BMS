fetch('/billing/api/view-bills/')
    .then(response => response.json())
    .then(data => {
        let table = document.querySelector('table');
        let condition = true;
        for (let bill of data) {
            if (condition) {
                let row = `<tr>
                <td class="w-1/3 text-left py-3 px-4">${bill.id}</td>
                <td class="w-1/3 text-left py-3 px-4">${bill.total_price}</td>
                <td class="text-left py-3 px-4">${bill.invoice_date}</td>
                <td class="text-left py-3 px-4"><button onClick='openBill(${bill.id})'>Open</button></td>
            </tr>`;
                table.innerHTML += row;
                condition = false;
            } else {
                let row = `<tr class="bg-gray-200">
                <td class="w-1/3 text-left py-3 px-4">${bill.id}</td>
                <td class="w-1/3 text-left py-3 px-4">${bill.total_price}</td>
                <td class="text-left py-3 px-4">${bill.invoice_date}</td>
                <td class="text-left py-3 px-4"><button onClick='openBill(${bill.id})'>Open</button></td>
            </tr>`;
                table.innerHTML += row;
                condition = true;
            }
        }
    }
    );

function openBill(id) {
    data = {
        "bill-id": id
    }
    fetch('/billing/api/view-bills/' + id)
        .then(response => response.json())
        .then(data => {
            console.log(data);
            let table = document.querySelector('table');
            table.innerHTML = `<tr>
                <th>Product</th>
                <th>Quantity</th>
                <th>Price</th>
            </tr>`;
            for (let product of data) {
                let row = `<tr>
                    <td>${product.item}</td>
                    <td>${product.quantity}</td>
                    <td>${product.price}</td>
                </tr>`;
                table.innerHTML += row;
            }
        }
        );
}