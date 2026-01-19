import client from "./client";


export function getCategory(id) {
  return client.get(`/categories/${id}`);
}

export function getCategories(params = {}) {
  return client.get("/categories", { params });
}

export function createCategory(data) {
  return client.post("/categories", data);
}

export function updateCategory(id, data) {
  return client.put(`/categories/${id}`, data);
}

export function deleteCategory(id) {
  return client.delete(`/categories/${id}`);
}