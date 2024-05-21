let profileForm = document.getElementById('profile-form');

profileForm.addEventListener('submit', function (e) {
    e.preventDefault();
    let formData = new FormData(profileForm);
    fetch('/api/change-profile-details', {
        method: 'POST',
        body: formData
    }).then(response => response.json())
        .then(data => {
            if (data.success) {
                alertify.set('notifier', 'position', 'top-right');
                alertify.set('notifier', 'delay', 3);
                alertify.success(data.success);
            } else {
                alertify.set('notifier', 'position', 'top-right');
                alertify.set('notifier', 'delay', 3);
                alertify.error(data.error);
            }
        });
});

let passwordForm = document.getElementById('password-form');
let passwordModal = document.querySelector('[password-modal]');

function openForm() {
    passwordModal.showModal();
}

function closeForm() {
    passwordModal.close();
}

passwordForm.addEventListener('submit', function (e) {
    e.preventDefault();
    let formData = new FormData(passwordForm);
    passwordForm.reset();
    passwordModal.close();
    fetch('/api/change-profile-details?change_password=True', {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': document.querySelector('input[name="csrfmiddlewaretoken"]').value
        }
    }).then(response => response.json())
        .then(data => {
            if (data.success) {
                alertify.set('notifier', 'position', 'top-right');
                alertify.set('notifier', 'delay', 3);
                alertify.success(data.success);
            } else {
                alertify.set('notifier', 'position', 'top-right');
                alertify.set('notifier', 'delay', 3);
                alertify.error(data.error);
            }
        });
    setTimeout(function () {
        window.location.reload();
    }, 2000);
});