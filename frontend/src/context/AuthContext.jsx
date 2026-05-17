/**
 * TakhleeqX Auth Context — Global auth state management.
 */
import { createContext, useContext, useState, useEffect } from 'react';
import api from '../api/client';

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(localStorage.getItem('takhleeqx_token'));
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (token) {
      const stored = localStorage.getItem('takhleeqx_user');
      if (stored) {
        try {
          setUser(JSON.parse(stored));
        } catch { }
      }
    }
    setLoading(false);
  }, [token]);

  const login = async (username, password) => {
    const res = await api.post('/auth/login', { username, password });
    const data = res.data;
    localStorage.setItem('takhleeqx_token', data.access_token);
    localStorage.setItem('takhleeqx_user', JSON.stringify({ id: data.user_id, username: data.username }));
    setToken(data.access_token);
    setUser({ id: data.user_id, username: data.username });
    return data;
  };

  const register = async (email, username, password, full_name) => {
    const res = await api.post('/auth/register', { email, username, password, full_name });
    const data = res.data;
    localStorage.setItem('takhleeqx_token', data.access_token);
    localStorage.setItem('takhleeqx_user', JSON.stringify({ id: data.user_id, username: data.username }));
    setToken(data.access_token);
    setUser({ id: data.user_id, username: data.username });
    return data;
  };

  const logout = () => {
    localStorage.removeItem('takhleeqx_token');
    localStorage.removeItem('takhleeqx_user');
    setToken(null);
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, token, loading, login, register, logout, isAuthenticated: !!token }}>
      {children}
    </AuthContext.Provider>
  );
}

export const useAuth = () => useContext(AuthContext);
