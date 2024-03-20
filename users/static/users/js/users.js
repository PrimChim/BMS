let tablebody = document.getElementById('table-body');
let userTable = document.getElementById('user-table');

function getUsers() {
    fetch('/api/users')
        .then(response => response.json())
        .then(data => {
            data.forEach(element => {
                userTable.innerHTML += `<tr>
                <td>1</td>
                <td>${element.username}</td>
                <td>${element.email}</td>
                <td>${element.is_superuser}</td>
                <td>edit delete</td>
                </tr>`;
            });
        })

}
getUsers()