import client from "./client";


export function login(email, password) {
  const formData = new URLSearchParams();
  formData.append("username", email);
  formData.append("password", password);
  return client.post("/token", formData, {
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
  });
}

export function register(email, password) {
  return client.post("/users", { "email": email, "password": password });
}

export function logout() {
  localStorage.removeItem("token");
}