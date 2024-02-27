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

let customersList = document.getElementById('customers-list');
if (localStorage.getItem('customers') === null) {
    fetchCustomers();
} else {
    let customers = JSON.parse(localStorage.getItem('customers'));
    if (customers != null) {
        customers.forEach(customer => {
            customersList.innerHTML += `<li onClick="setCustomer('${customer.name}', ${customer.pan})">${customer.name}</li>`;
            console.log(customer);
        });
    }
}

let customer = document.getElementById('customer');

function setCustomer(name, pan) {
    customer.value = name;
    customerPan.value = pan;
    customersList.style.display = 'none';
}

customer.addEventListener('focus', function () {
    if (this.value == '') {
        customersList.style.display = 'block';
    }

    let customers = JSON.parse(localStorage.getItem('customers'));
    let filteredCustomers = customers.filter(customer => customer.name.toLowerCase().includes(this.value.toLowerCase()));

    customersList.innerHTML = '';
    filteredCustomers.forEach(customer => {
        customersList.innerHTML += `<li onClick="setCustomer('${customer.name}', ${customer.pan})">${customer.name}</li>`;
    });
    customersList.style.display = 'block';

    if (filteredCustomers.length == 0) {
        fetchCustomers();
        customersList.style.display = 'none';
    }
})

customer.addEventListener('input', function () {
    customersList.style.display = 'block';

    let customers = JSON.parse(localStorage.getItem('customers'));
    let filteredCustomers = customers.filter(customer => customer.name.toLowerCase().includes(this.value.toLowerCase()));
    
    if (filteredCustomers.length == 0) {
        fetchCustomers();
        customersList.style.display = 'none';
    }
    
    customersList.innerHTML = '';
    filteredCustomers.forEach(customer => {
        customersList.innerHTML += `<li onClick="setCustomer('${customer.name}', ${customer.pan})">${customer.name}</li>`;
    });
});

customer.addEventListener('focusout', function () {
    if (this.value == '') {
        customerPan.value = '';
    }
    setTimeout(() => {
        customersList.style.display = 'none';
    }, 200);
})

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