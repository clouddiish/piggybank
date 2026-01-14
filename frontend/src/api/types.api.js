import client from "./client";


export function getType(id) {
    return client.get(`/types/${id}`);
}

export function getTypes() {
    return client.get("/types");
}