fetch('/billing/api/view-bills/')
    .then(response => response.json())
    .then(data => {
        let table = document.querySelector('table');
        for (let bill of data) {
            let row = `<tr>
                <td>${bill.id}</td>
                <td>${bill.total_price}</td>
                <td>${bill.invoice_date}</td>
                <td><button onClick='openBill(${bill.id})'>Open</button></td>
            </tr>`;
            table.innerHTML += row;
        }
    }
    );

function openBill(id) {
    data = {
        "bill-id": id
    }
    fetch('/billing/api/view-bills/'+id)
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