const signupForm = document.getElementById("signup-form");
const loginForm = document.getElementById("login-form");

signupForm.addEventListener("submit", async (e) => {
  e.preventDefault();

  const name = document.getElementById("signup-name").value;
  const email = document.getElementById("signup-email").value;
  const password = document.getElementById("signup-password").value;

  const response = await fetch("http://127.0.0.1:5000/api/users/signup", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ name, email, password }),
  });

  const result = await response.json();
  const messageDiv = document.getElementById("signup-message");
  const userDataDiv = document.getElementById("user-data");

  if (response.status === 201) {
    messageDiv.innerHTML = `<p id="success">Sign up successful!</p>`;
    // Fetch user data from the database
    userDataDiv.innerHTML = `<p><strong>Name:</strong> ${result.name}</p><p><strong>Email:</strong> ${result.email}</p>`;
  } else {
    messageDiv.innerHTML = `<p id="error">${result.error}</p>`;
    userDataDiv.innerHTML = "";
  }
});

loginForm.addEventListener("submit", async (e) => {
  e.preventDefault();

  const email = document.getElementById("login-email").value;
  const password = document.getElementById("login-password").value;

  const response = await fetch("http://127.0.0.1:5000/api/users/login", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ email, password }),
  });

  const result = await response.json();
  const messageDiv = document.getElementById("login-message");

  if (response.status === 200) {
    messageDiv.innerHTML = `<p id="success">Login successful! Welcome, ${result.user.name}!</p>`;
  } else {
    messageDiv.innerHTML = `<p id="error">${result.error}</p>`;
  }
});
