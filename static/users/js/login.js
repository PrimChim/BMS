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
                alertify.set('notifier', 'position', 'top-center');
                alertify.success(response.success);
                setTimeout(function () {
                    if (response.superuser) {
                        window.location.href = '/admin/';
                    } else {
                        window.location.href = '/billing/dashboard';
                    }
                }, 2000);
            } else if (response.error) {
                alertify.set('notifier', 'position', 'top-center');
                alertify.success(response.error);
            }
        } else if (xhr.readyState === 4 && xhr.status === 403) {
            window.location.href = '/billing/dashboard';
        } else if (xhr.readyState === 4 && xhr.status === 400) {
            var response = JSON.parse(xhr.responseText);
            alertify.set('notifier', 'delay', 2);
            alertify.set('notifier', 'position', 'top-center');
            alertify.error(response.error);
        }
    };
    xhr.send(JSON.stringify(data));
});