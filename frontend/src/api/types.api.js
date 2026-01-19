import client from "./client";


export function getType(id) {
  return client.get(`/types/${id}`);
}

export function getTypes(params = {}) {
  return client.get("/types", { params });
}