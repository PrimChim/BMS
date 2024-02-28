let customersList = document.getElementById('customers-list');
let customer = document.getElementById('customer');
let customerPan = document.querySelectorAll('.customer-details')[1];

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

// initial fetch of customers to localstorage
if (localStorage.getItem('customers') === null) {
    fetchCustomers();
} else {
    let customers = JSON.parse(localStorage.getItem('customers'));
    if (customers != null) {
        customers.forEach(customer => {
            customersList.innerHTML += `<li onClick="setCustomer('${customer.name}', ${customer.pan})">${customer.name}</li>`;
        });
    }
}

// set customer name and pan in input fields
function setCustomer(name, pan) {
    customer.value = name;
    customerPan.value = pan;
    customersList.style.display = 'none';
}

// search customer from localstorage
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

// search customer from localstorage
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

// hide customer list when focus out
customer.addEventListener('focusout', function () {
    if (this.value == '') {
        customerPan.value = '';
    }
    setTimeout(() => {
        customersList.style.display = 'none';
    }, 200);
})

// populate new data in localstorage in certain interval
setInterval(fetchCustomers, 120000);

// adding new table row in bill
function addLineToBill() {
    ```
    function to add new line to bill table
    ```
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