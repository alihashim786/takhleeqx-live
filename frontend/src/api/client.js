/**
 * TakhleeqX API Client — Axios instance with JWT auth interceptor.
 */
import axios from 'axios';

const API_BASE = 'https://takhleeqx-live.onrender.com/api';

const api = axios.create({
  baseURL: API_BASE,
  headers: { 'Content-Type': 'application/json' },
});

// Request interceptor — attach JWT token and OpenAI Key
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('takhleeqx_token');
  const openaiKey = localStorage.getItem('takhleeqx_openai_key');

  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  if (openaiKey) {
    config.headers['X-OpenAI-Key'] = openaiKey;
  }
  return config;
});

// Response interceptor — handle 401
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('takhleeqx_token');
      localStorage.removeItem('takhleeqx_user');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export default api;
