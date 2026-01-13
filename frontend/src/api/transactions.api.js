import client from "./client";


export function getTransaction(id) {
    return client.get(`/transactions/${id}`);
}

export function getTransactions() {
    return client.get("/transactions");
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