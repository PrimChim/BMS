let profileForm = document.getElementById('profile-form');

profileForm.addEventListener('submit', function(e) {
    e.preventDefault();
    let formData = new FormData(profileForm);
    fetch('/api/change-profile-details', {
        method: 'POST',
        body: formData
    }).then(response => response.json())
    .then(data => {
        if (data.success) {
            alert(data.success);
        } else {
            alert(data.error);
        }
    });
});