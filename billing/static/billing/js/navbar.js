let uri = window.location.pathname;
const createBills = document.getElementById('create-bill');
const viewBills = document.getElementById('view-bills');

switch(uri) {
    case '/billing/create-bill/':
        createBills.classList.add('active')
        break
    case '/billing/bills/':
        viewBills.classList.add('active')
        break
};