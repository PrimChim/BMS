let itemsSearch = document.getElementById('items-search');
let billTable = document.getElementById('bill-table');
let itemsSearchResults = document.getElementById('items-search-result');

// fetch all items and store them in localstorage
function fetchItems() {
    let items = [];
    fetch('/billing/api/get-items/')
        .then((response) => response.json())
        .then((data) => {
            items = data;
            localStorage.setItem('items', JSON.stringify(items));
        });
}

// initial item fetch and store in localstorage
if (!localStorage.getItem('items')) {
    fetchItems();
}

// search items dom manipulation
itemsSearch.addEventListener('input', function () {
    let items = JSON.parse(localStorage.getItem('items'));
    let filteredItems = items.filter(item => item.name.toLowerCase().includes(this.value.toLowerCase()));
    if (filteredItems.length == 0) {
        fetchItems();
        itemsSearchResults.innerHTML = 'No items found. Please try again.';
    }
    itemsSearchResults.innerHTML = '';
    filteredItems.forEach(item => {
        itemsSearchResults.innerHTML += `
        <li class="h-8 hover:bg-slate-600 hover:cursor-pointer" onclick="setItem('${item.name}', ${item.price})">${item.name}</li>`;
    });
})

// items fade in
itemsSearch.addEventListener('focus', function () {
    let items = JSON.parse(localStorage.getItem('items'));
    let filteredItems = items.filter(item => item.name.toLowerCase().includes(this.value.toLowerCase()));
    if (filteredItems.length == 0) {
        fetchItems();
        itemsSearchResults.innerHTML = 'No items found. Please try again.';
    }
    itemsSearchResults.innerHTML = '';
    filteredItems.forEach(item => {
        itemsSearchResults.innerHTML += `
        <li class="h-8 hover:bg-slate-600 hover:cursor-pointer" onclick="setItem('${item.name}', ${item.price})">${item.name}</li>`;
    });
})

// items fade out
itemsSearch.addEventListener('focusout', function () {
    setTimeout(() => {
        itemsSearchResults.innerHTML = '';
    }, 200);
})

// add items on click
function setItem(name, price) {
    if (name == "Digital 16' External Monitor") {
        name = "Digital 16\' External Monitor";
    }

    if (items.items.includes(name)) {
        items.quantity[items.items.indexOf(name)] += 1;
    } else {
        items.items.push(name);
        items.quantity.push(1);
        items.price.push(price);
    }
    let tableData = '';
    for (let i = 0; i < items.items.length; i++) {
        tableData += `<tr>
        <td class="w-1/2 text-left py-3 px-4 bg-slate-300">${items.items[i]}</td>
        <td class="w-28 text-left bg-slate-200"><input type="number" name="" value=${items.quantity[i]} class="w-full px-4 bg-transparent" readonly></td>
        <td class="w-28 text-left py-3 px-4 bg-slate-300">${items.price[i]}</td>
        <td class="w-28 text-left py-3 px-4 bg-slate-200">${items.price[i]*items.quantity[i]}</td>
        <td class="w-28 text-left py-3 px-4 bg-slate-300"><button onClick='removeItem(this)'>Remove</button></td>
        </tr>`;
    }
    billTable.innerHTML = tableData;
    tableData = '';
    itemsSearch.value = '';
    itemsSearchResults.innerHTML = '';
    calculateTotalOnChange();
}

// calculate total on quantity change
let total = document.getElementById('total');
function calculateTotalOnChange() {
    let totalAmount = 0;
    // multiply each item price with its quantity
    for (let i = 0; i < items.quantity.length; i++) {
        totalAmount += items.price[i] * items.quantity[i];
    }
    total.value = totalAmount;
    items.total = totalAmount;
}
