import axios from "axios";

const getApiUrl = () => {
  if (import.meta.env.VITE_API_URL) {
    return import.meta.env.VITE_API_URL;
  }
  if (typeof window !== 'undefined' && window.location.hostname.includes('replit.dev')) {
    const replitDomain = window.location.hostname;
    return `https://${replitDomain}:8000`;
  }
  return "http://localhost:8000";
};

const API_URL = getApiUrl();

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
