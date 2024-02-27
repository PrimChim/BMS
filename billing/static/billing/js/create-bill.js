// fetch all customers and store them in cache
function fetchCustomers() {
    let customers = [];
    fetch('/customers')
        .then((response) => response.json())
        .then((data) => {
            customers = data;
            localStorage.setItem('customers', JSON.stringify(customers));
        });
}

let customerPan = document.querySelectorAll('.customer-details')[1];
if (localStorage.getItem('customers') === null) {
    fetchCustomers();
} else {
    let customers = JSON.parse(localStorage.getItem('customers'));
    let customerSelect = document.getElementById('customer');
    customers.forEach(customer => {
        let option = document.createElement('option');
        option.value = customer.pan;
        option.text = customer.name;
        customerSelect.appendChild(option);
    });
    customerPan.value = customers[0].pan;

}

document.getElementById('customer').addEventListener('change', function () {
    let customers = JSON.parse(localStorage.getItem('customers'));
    console.log(customerPan);
    let customer = customers.find(customer => customer.pan == this.value);
    customerPan.value = customer.pan;
});

// populate new data in localstorage in certain interval
setInterval(fetchCustomers, 120000);

function addLineToBill() {
    let table = document.getElementById('bill-table');
    let sn = table.rows.length;
    table.innerHTML += `
        <tr>
            <td class="sn" width="40px">${sn}</td>
            <td class="item-name"><input type="text" name="${sn}item-name" class="item-name"></td>
            <td class="quantity"><input type="number" name="${sn}item-quantity"></td>
            <td class="price"><input type="number" name="${sn}item-price"></td>
            <td class="total"><input type="number" name="${sn}item-total" id="" readonly></td>
        </tr>`;
}