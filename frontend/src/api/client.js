import axios from 'axios';

// English: Base axios client for all backend requests.
// Roman Urdu: Sab backend requests ke liye ek common axios client.
const api = axios.create({
  baseURL: 'http://127.0.0.1:8000',
});

// English: Attach the JWT token to every request if present.
// Roman Urdu: Har request ke saath JWT token bhejte hain agar mojood ho.
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = 'Bearer ' + token;
  }
  return config;
});

// English: If the token has expired, clear it and send the user to login automatically.
// Roman Urdu: Agar token expire ho gaya ho to use hata kar user ko login page pe bhej dete hain.
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      if (window.location.pathname !== '/login' && window.location.pathname !== '/register') {
        window.location.href = '/login';
      }
    }
    return Promise.reject(error);
  }
);

export default api;
