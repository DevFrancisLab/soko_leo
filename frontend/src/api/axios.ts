import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000/api/',
});

// Request interceptor to add Authorization header
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor to handle token refresh on 401
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    if (error.response?.status === 401 && !error.config._retry) {
      error.config._retry = true;
      const refreshToken = localStorage.getItem('refresh_token');
      if (refreshToken) {
        try {
          const response = await api.post('/accounts/token/refresh/', { refresh: refreshToken });
          const { access } = response.data;
          localStorage.setItem('access_token', access);
          error.config.headers.Authorization = `Bearer ${access}`;
          return api(error.config);
        } catch (refreshError) {
          // Refresh failed, reject the error
        }
      }
    }
    return Promise.reject(error);
  }
);

export default api;