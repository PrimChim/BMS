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
    console.log(filteredItems)
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
    billTable.innerHTML += `<tr>
        <td><input type="text" value="${name}" readonly></td>
        <td><input type="number" value="${price}" readonly></td>
        <td><input type="number" value="1" min="1" max="10"></td>
        <td></td>
        </tr>`;
    itemsSearch.value = '';
    itemsList.style.display = 'none';
}