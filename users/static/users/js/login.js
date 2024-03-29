var loginForm = document.getElementById('login-form');

loginForm.addEventListener('submit', function (e) {
    e.preventDefault();
    var formData = new FormData(loginForm);
    var data = {};
    formData.forEach(function (value, key) {
        data[key] = value;
    });
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/api/login', true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4 && xhr.status === 200) {
            var response = JSON.parse(xhr.responseText);
            if (response.success) {
                if (response.superuser) {
                    window.location.href = '/admin/';
                } else {
                    window.location.href = '/billing/create-bill/';
                }
            } else {
                alert(response.message);
            }
        }
    };
    xhr.send(JSON.stringify(data));
});