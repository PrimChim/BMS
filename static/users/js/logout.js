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