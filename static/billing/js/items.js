let itemsTable = document.getElementById('items-table');

function items() {
    fetch('/billing/api/get-items')
        .then(response => response.json())
        .then(data => {
            data.forEach(item => {
                let row = itemsTable.insertRow(-1);
                let cell1 = row.insertCell(0);
                let cell2 = row.insertCell(1);
                let cell3 = row.insertCell(2);

                cell1.innerHTML = item.name;
                cell2.innerHTML = item.price;
                cell3.innerHTML = `<button onClick='openItem(${item.id})'><i class="fas fa-eye mt-3"><i></button>`;

                cell1.classList.add('w-3/5', 'text-left', 'py-3', 'px-4');
                cell2.classList.add('w-1/5', 'text-left', 'py-3', 'px-4');
                cell3.classList.add('w-1/5', 'text-center', 'py-3', 'px-4');

                if (itemsTable.rows.length % 2 === 0) {
                    row.classList.add('bg-gray-200');
                }
            })
        });
}

items();

let searchForm = document.getElementById('search-form');

searchForm.addEventListener('submit', function (e) {
    e.preventDefault();
    let search = document.getElementById('search').value;
    fetch(`/billing/api/get-items?search=${search}`)
        .then(response => response.json())
        .then(data => {
            itemsTable.innerHTML = '';
            data.forEach(item => {
                let row = itemsTable.insertRow(-1);
                let cell1 = row.insertCell(0);
                let cell2 = row.insertCell(1);
                let cell3 = row.insertCell(2);

                cell1.innerHTML = item.name;
                cell2.innerHTML = item.price;
                cell3.innerHTML = `<button onClick='openItem(${item.id})'><i class="fas fa-eye mt-3"><i></button>`;

                cell1.classList.add('w-3/5', 'text-left', 'py-3', 'px-4');
                cell2.classList.add('w-1/5', 'text-left', 'py-3', 'px-4');
                cell3.classList.add('w-1/5', 'text-center', 'py-3', 'px-4');

                if (itemsTable.rows.length % 2 === 0) {
                    row.classList.add('bg-gray-200');
                }
            })
        });
}
);