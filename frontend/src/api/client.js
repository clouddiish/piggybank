import axios from "axios";


const client = axios.create({
  baseURL: process.env.REACT_APP_API_BASE_URL || "http://localhost:8000/",
  headers: {
    "Content-Type": "application/json",
  },
  withCredentials: true,
});


client.interceptors.response.use(
  response => response,
  async error => {
    const originalRequest = error.config;
    const publicPaths = ["/", "/login", "/register", "/register-success"];

    if (sessionStorage.getItem("refreshFailed")) {
      window.location.href = "/";
      return Promise.reject(error);
    }

    if (
      error.response && 
      error.response.status === 401 && 
      !originalRequest._retry &&
      !originalRequest.url.includes("/token/refresh") &&
      !originalRequest.url.includes("/token/logout")
    ) {
      originalRequest._retry = true;
      try {
        await client.post("/token/refresh");
        return client(originalRequest);
      } catch {
        if (!publicPaths.includes(window.location.pathname)) {
          window.location.href = "/";
        }
        // sessionStorage.setItem("refreshFailed", "true");
        return Promise.reject(error);
      }
    }
    return Promise.reject(error);
  }
);

export default client;