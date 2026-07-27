import { createContext, useContext, useEffect, useState } from "react";
import { decodeToken } from "../utils";
import * as api from "../services/api";

const STORAGE_KEY = "nexhire_session";
const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [session, setSession] = useState(null);
  const [isRestoring, setIsRestoring] = useState(true);

  useEffect(() => {
    try {
      const stored = JSON.parse(localStorage.getItem(STORAGE_KEY));
      const payload = stored?.token ? decodeToken(stored.token) : {};
      const isExpired = payload.exp && payload.exp * 1000 <= Date.now();
      if (stored?.token && stored?.role && !isExpired) setSession(stored);
      else localStorage.removeItem(STORAGE_KEY);
    } finally {
      setIsRestoring(false);
    }
  }, []);

  function saveSession(nextSession) {
    const payload = decodeToken(nextSession.token);
    const normalized = { ...nextSession, userId: payload.id };
    localStorage.setItem(STORAGE_KEY, JSON.stringify(normalized));
    setSession(normalized);
    return normalized;
  }

  async function login(credentials) {
    return saveSession(await api.login(credentials));
  }

  async function signup(role, details) {
    return saveSession(await api.signup(role, details));
  }

  function logout() {
    localStorage.removeItem(STORAGE_KEY);
    setSession(null);
  }

  const value = {
    ...session,
    isAuthenticated: Boolean(session?.token),
    isRestoring,
    login,
    signup,
    logout,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const value = useContext(AuthContext);
  if (!value) throw new Error("useAuth must be used inside AuthProvider");
  return value;
}
