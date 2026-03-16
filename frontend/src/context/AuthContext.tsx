/* eslint-disable react-refresh/only-export-components */
import React, { createContext, useState, ReactNode } from 'react';
import { createApi } from '@/api/axios';

interface User {
  username: string;
}

interface AuthContextType {
  currentUser: User | null;
  login: (username: string, password: string) => Promise<void>;
  logout: () => Promise<void>;
  api: ReturnType<typeof createApi>;
}

export const AuthContext = createContext<AuthContextType | undefined>(undefined);

interface AuthProviderProps {
  children: ReactNode;
}

export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const [currentUser, setCurrentUser] = useState<User | null>(null);

  // Ensure we keep the user logged in across refreshes when an access token exists.
  // This avoids situations where the auth token is present but `currentUser` is null,
  // which would prevent Axios from attaching the Authorization header.
  const decodeTokenUsername = (token: string) => {
    try {
      const payload = token.split('.')[1];
      const decoded = JSON.parse(atob(payload.replace(/-/g, '+').replace(/_/g, '/')));
      return decoded?.username || decoded?.user_id || null;
    } catch {
      return null;
    }
  };

  React.useEffect(() => {
    const accessToken = localStorage.getItem('access_token');
    if (accessToken && !currentUser) {
      const username = decodeTokenUsername(accessToken) || 'user';
      setCurrentUser({ username });
    }
  }, [currentUser]);

  // Create an Axios instance that reads the current Auth state for the access token.
  const api = createApi(() => {
    // Always attach Authorization when an access token exists so API calls
    // succeed even if `currentUser` state is not yet hydrated.
    return localStorage.getItem('access_token');
  });

  const login = async (username: string, password: string) => {
    const response = await api.post('/accounts/login/', { username, password });
    const { access, refresh } = response.data;
    localStorage.setItem('access_token', access);
    localStorage.setItem('refresh_token', refresh);
    setCurrentUser({ username });
  };

  const logout = async () => {
    const refreshToken = localStorage.getItem('refresh_token');
    if (refreshToken) {
      try {
        await api.post('/accounts/logout/', { refresh: refreshToken });
      } catch (error) {
        // Ignore logout API errors
      }
    }
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    setCurrentUser(null);
  };

  const value: AuthContextType = {
    currentUser,
    login,
    logout,
    api,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};