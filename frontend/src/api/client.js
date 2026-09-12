import axios from 'axios';

const api = axios.create({
  baseURL: 'http://127.0.0.1:8000',
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  console.log('[API Request]', config.method?.toUpperCase(), config.url, 'Token present:', !!token);
  if (token) {
    config.headers.Authorization = 'Bearer ' + token;
  }
  return config;
});

api.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('[API Error]', error.config?.method?.toUpperCase(), error.config?.url, error.message);
    return Promise.reject(error);
  }
);

export default api;
