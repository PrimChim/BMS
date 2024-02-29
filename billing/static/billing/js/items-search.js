let itemsSearch = document.getElementById('items-search');
let billTable = document.getElementById('bill-table');
let itemsList = document.getElementById('items-list');

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
    itemsList.style.display = 'block';

    let items = JSON.parse(localStorage.getItem('items'));
    let filteredItems = items.filter(item => item.name.toLowerCase().includes(this.value.toLowerCase()));
    if (filteredItems.length == 0) {
        fetchItems();
        itemsList.style.display = 'none';
    }
    itemsList.innerHTML = '';
    filteredItems.forEach(item => {
        itemsList.innerHTML += `<li onClick="setItem('${item.name}', ${item.price})">
        ${item.name}
        Rs.${item.price}
        </li>`;
    });
})

// items fade out
itemsSearch.addEventListener('focusout', function () {
    setTimeout(() => {
        itemsList.style.display = 'none';
    }, 200);
})

// add items on click
function setItem(name, price) {
    let sn = billTable.rows.length;

    if(name == "Digital 16' External Monitor"){
        name = "Digital 16\' External Monitor";
    }

    billTable.innerHTML += `<tr>
        <td class='sn'>${sn}</td>
        <td class='item-name'><input type="text" value="${name}" name="item-name" class="item-name" readonly></td>
        <td class='quantity'><input type="number" name='item-quantity' value='1'></td>
        <td class='price'><input type="number" name='item-price' value="${price}" readonly></td>
        <td clas='total'><input type='number' name='item-total'value=${price} readonly></td>
        </tr>`;
    itemsSearch.value = '';
    itemsList.style.display = 'none';
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
