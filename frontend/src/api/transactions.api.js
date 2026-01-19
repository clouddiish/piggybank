import client from "./client";


export function getTransaction(id) {
  return client.get(`/transactions/${id}`);
}

export function getTransactions(params = {}) {
  return client.get("/transactions", { params });
}

export function getTransactionsTotal(params = {}) {
  return client.get("/transactions/total", { params });
}

export function createTransaction(data) {
  return client.post("/transactions", data);
}

export function updateTransaction(id, data) {
  return client.put(`/transactions/${id}`, data);
}

export function deleteTransaction(id) {
  return client.delete(`/transactions/${id}`);
}