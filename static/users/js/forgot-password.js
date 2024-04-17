let form = document.getElementById('forgot-password-form');
let resetForm = document.getElementById('password-reset-form');

let email = "";

form.addEventListener('submit', function (e) {
    e.preventDefault();
    let formData = new FormData(form);
    email = formData.get('email');
    let xhr = new XMLHttpRequest();
    xhr.open('POST', '/api/forgot-password', true);
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4 && xhr.status === 200) {
            let response = JSON.parse(xhr.responseText);
            if (response.success) {
                alert(response.success);
                form.style.display = 'none';
                resetForm.style.display = 'block';
            } else {
                alert(response.error);
            }
        } else if (xhr.readyState === 4 && xhr.status === 404) {
            let response = JSON.parse(xhr.responseText);
            if (response.error) {
                alert(response.error);
            }
        }
    }
    xhr.send(formData);
});

resetForm.addEventListener('submit', function (e) {
    e.preventDefault();
    let formData = new FormData(resetForm);
    formData.append('email', email);
    console.log(formData);
    let password = formData.get('password');
    let confirmPassword = formData.get('confirm-password');
    if (password !== confirmPassword) {
        alert('Passwords do not match');
        return;
    }
    let xhr = new XMLHttpRequest();
    xhr.open('POST', '/api/reset-password', true);
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4 && xhr.status === 200) {
            let response = JSON.parse(xhr.responseText);
            console.log(response); // Just for debugging, remove this line in production
            if (response.success) {
                alert(response.success);
                window.location.href = '/login';
            } else {
                alert(response.error);
            }
        } else if (xhr.readyState === 4 && xhr.status === 404) {
            let response = JSON.parse(xhr.responseText);
            if (response.error) {
                alert(response.error);
            }
        } else if (xhr.readyState === 4 && xhr.status === 400) {
            let response = JSON.parse(xhr.responseText);
            if (response.error) {
                console.log(response.error);
            }
        }
    }
    xhr.send(formData);
});