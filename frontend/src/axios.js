
import axios from "axios";

const api = axios.create({
  baseURL: "http://127.0.0.1:8000/api",
});

// Attach access token to every request
api.interceptors.request.use((config) => {
  const token = localStorage.getItem("access");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// ✅ Handle expired tokens automatically
api.interceptors.response.use(
  (response) => response, // pass successful responses
  async (error) => {
    const originalRequest = error.config;

    // If unauthorized due to token expiry
    if (
      error.response &&
      error.response.status === 401 &&
      !originalRequest._retry
    ) {
      originalRequest._retry = true; // prevent infinite loop

      try {
        const refresh = localStorage.getItem("refresh");
        if (refresh) {
          const res = await axios.post("http://127.0.0.1:8000/api/token/refresh/", {
            refresh: refresh,
          });

          localStorage.setItem("access", res.data.access);
          originalRequest.headers.Authorization = `Bearer ${res.data.access}`;

          return api(originalRequest); // retry the failed request
        }
      } catch (refreshError) {
        console.error("Refresh token expired, please login again");
        localStorage.removeItem("access");
        localStorage.removeItem("refresh");
        window.location.href = "/login"; // redirect to login
      }
    }
    return Promise.reject(error);
  }
);

export default api;
