let customersList = document.getElementById('customers-list');
let customerPan = document.getElementById('customer-pan');
let customer = document.getElementById('customer-name');

// creating a list of all items and customer name and email in a object
let items = {
    'customer-email': '',
    'bill-total': 0,
    'items': [],
    'quantity': [],
    'price': [],
    'total': 0
};

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
}

// set customer name and pan in input fields
function setCustomer(name, pan, email) {
    customer.value = name;
    customerPan.value = pan;
    customersList.style.display = 'none';
    items['customer-email'] = email;
    console.log(items);
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
        customersList.innerHTML += `<li class="hover:cursor-pointer hover:bg-slate-600" onClick="setCustomer('${customer.name}', ${customer.pan}, '${customer.email}')">${customer.name}</li>`;
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
        customersList.innerHTML += `<li class="hover:cursor-pointer hover:bg-slate-600" onClick="setCustomer('${customer.name}', ${customer.pan}, '${customer.email}')">${customer.name}</li>`;
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

// create bill
function createBill() {
    let url = '/billing/api/create-bill-api/';
    let data = items;
    let csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify(data),
    })
        .then((response) => response.json())
        .then((data) => {
            console.log(data);
        })
        .catch((error) => {
            console.error('Error:', error);
        });
    items = {
        'customer-email': '',
        'bill-total': 0,
        'items': [],
        'quantity': [],
        'price': [],
        'total': 0
    };    
}