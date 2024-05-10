let logoutForm = document.getElementById('logout-form');

function logout() {
    var xhr = new XMLHttpRequest();
    xhr.open('GET', '/api/logout', true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4 && xhr.status === 200) {
            var response = JSON.parse(xhr.responseText);
            if (response.success) {
                window.location.href = '/';
            } else {
                alert(response.message);
            }
        }
    };
    xhr.send();
}

if (logoutForm) {
    logoutForm.addEventListener('submit', function (e) {
        e.preventDefault();
        logout();
    });
}

// for active nav link

function handleNavLinks() {
    let navLinks = document.querySelectorAll('nav a');
    navLinks.forEach(function (link) {
        link.classList.remove('active-nav-link');
    });
    let path = window.location.pathname;
    if (path === '/billing/dashboard/') {
        navLinks[0].classList.add('active-nav-link');
    } else if (path === '/billing/create-bill/') {
        navLinks[1].classList.add('active-nav-link');
    } else if (path === '/billing/bills/') {
        navLinks[2].classList.add('active-nav-link');
    } else if (path === '/billing/items/') {
        navLinks[3].classList.add('active-nav-link');
    } else if (path === '/billing/customers/') {
        navLinks[4].classList.add('active-nav-link');
    } else if (path === '/billing/business-settings/') {
        navLinks[5].classList.add('active-nav-link');
    }
}

handleNavLinks();