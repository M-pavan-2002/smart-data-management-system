const API = "http://127.0.0.1:5000";

// Add user
function addUser() {
    let name = document.getElementById("name").value;
    let email = document.getElementById("email").value;

    fetch(`${API}/add`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ name, email })
    })
    .then(res => res.json())
    .then(data => {
        alert(data.message);
        loadUsers();
    })
    .catch(err => console.error(err));
}

// Load users
function loadUsers() {
    fetch(`${API}/get`)
    .then(res => res.json())
    .then(data => {
        let list = document.getElementById("list");
        list.innerHTML = "";

        data.forEach(user => {
            let li = document.createElement("li");
            li.innerHTML = `
                ${user.name} - ${user.email}
                <button onclick="deleteUser(${user.id})">X</button>
            `;
            list.appendChild(li);
        });
    });
}

// Delete user
function deleteUser(id) {
    fetch(`${API}/delete/${id}`, {
        method: "DELETE"
    })
    .then(() => loadUsers());
}

// Load on start
window.onload = loadUsers;