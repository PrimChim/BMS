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
    itemsSearchResults.style.display = 'block';

    let items = JSON.parse(localStorage.getItem('items'));
    let filteredItems = items.filter(item => item.name.toLowerCase().includes(this.value.toLowerCase()));
    if (filteredItems.length == 0) {
        fetchItems();
        itemsSearchResults.style.display = 'none';
    }
    itemsSearchResults.innerHTML = '';
    filteredItems.forEach(item => {
        itemsSearchResults.innerHTML += `<div class='item' onclick="setItem('${item.name}', ${item.price})">` + item.name + '</div>';
    });
})

// items fade out
itemsSearch.addEventListener('focusout', function () {
    setTimeout(() => {
        itemsSearchResults.style.display = 'none';
    }, 200);
})

// add items on click
function setItem(name, price) {
    let sn = billTable.rows.length;

    if (name == "Digital 16' External Monitor") {
        name = "Digital 16\' External Monitor";
    }

    billTable.innerHTML += `<tr>
        <td class="w-1/3 text-left py-3 px-4">${name}</td>
        <td class="w-1/3 text-left py-3 px-4"><input type="number" name="item-quantity" value="1"></td>
        <td class="w-1/3 text-left py-3 px-4">${price}</td>
        <td class="text-left py-3 px-4">${price}</td>
        <td class="text-left py-3 px-4"><button onClick='removeItem(this)'>Remove</button></td>
    </tr>`;
    itemsSearch.value = '';
    itemsSearchResults.style.display = 'none';
    calculateTotalOnChange();
}

// calculate total on quantity change
let quantity = document.getElementsByName('item-quantity');
let price = document.getElementsByName('item-price');
let total = document.getElementsByName('item-total');
function calculateTotalOnChange() {
    for (let i = 0; i < quantity.length; i++) {
        quantity[i].addEventListener('input', function () {
            total[i].value = quantity[i].value * price[i].value;
        })
    }
}
