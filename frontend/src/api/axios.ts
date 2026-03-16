import axios, { AxiosInstance } from 'axios';

export type GetTokenFn = () => string | null;

export function createApi(getToken?: GetTokenFn): AxiosInstance {
  const api = axios.create({
    baseURL: 'http://localhost:8000/api/',
  });

  api.interceptors.request.use(
    (config) => {
      const token = getToken ? getToken() : localStorage.getItem('access_token');
      if (token) {
        config.headers.Authorization = `Bearer ${token}`;
      }
      return config;
    },
    (error) => Promise.reject(error)
  );

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

  return api;
}

// Default instance (falls back to localStorage token)
export const api = createApi();