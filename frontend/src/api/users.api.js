import client from "./client";


export function getUserMe() {
  return client.get(`/users/me`)
}

export function getUser(id) {
  return client.get(`/users/${id}`);
}

export function getUsers(params = {}) {
  return client.get("/users/", { params });
}

export function createUser(data) {
  return client.post("/users/", data);
}

export function updateUser(id, data) {
  return client.put(`/users/${id}`, data);
}

export function deleteUser(id) {
  return client.delete(`/users/${id}`);
}