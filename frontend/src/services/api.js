import axios from "axios";

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

const api = axios.create({
  baseURL: API_URL,
  timeout: 10000,
});

// optional request/response interceptors
api.interceptors.response.use(
  (res) => res,
  (err) => {
    // simple console log; extend with toast notifications
    console.error("API error:", err?.response?.data ?? err.message);
    return Promise.reject(err);
  }
);

export default api;
