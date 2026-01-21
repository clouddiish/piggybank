import client from "./client";


export function getGoal(id) {
  return client.get(`/goals/${id}`);
}

export function getGoals(params = {}) {
  return client.get("/goals", { params });
}

export function createGoal(data) {
  return client.post("/goals", data);
}

export function updateGoal(id, data) {
  return client.put(`/goals/${id}`, data);
}

export function deleteGoal(id) {
  return client.delete(`/goals/${id}`);
}