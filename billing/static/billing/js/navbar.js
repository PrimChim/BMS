let uri = window.location.pathname;
const createBills = document.getElementById('create-bill');
const viewBills = document.getElementById('view-bills');
const button = document.getElementById('burger');
const nav = document.getElementById('nav');

switch(uri) {
    case '/billing/create-bill/':
        createBills.classList.add('active')
        break
    case '/billing/bills/':
        viewBills.classList.add('active')
        break
};

function changeIcon(){
    if (button.classList.contains('closed')){

        button.classList.remove('closed');
        button.classList.add('open');

        button.innerHTML = '&times';
        button.style.font = '40px';

        nav.classList.remove('collapsed');
    }else{
        
        button.classList.remove('open');
        button.classList.add('closed');

        button.innerHTML = '&#9776;';

        nav.classList.add('collapsed');
    }
}