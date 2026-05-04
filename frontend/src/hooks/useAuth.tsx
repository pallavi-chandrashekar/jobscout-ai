"use client";

import { useState, useEffect, useCallback, type ReactNode } from "react";
import api from "@/lib/api";
import { AuthContext, type AuthContextType } from "@/lib/auth";
import type { User, TokenResponse } from "@/lib/types";

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(null);

  const fetchUser = useCallback(async (t: string) => {
    try {
      const res = await api.get<User>("/auth/me", {
        headers: { Authorization: `Bearer ${t}` },
      });
      setUser(res.data);
    } catch {
      localStorage.removeItem("token");
      setToken(null);
      setUser(null);
    }
  }, []);

  useEffect(() => {
    const stored = localStorage.getItem("token");
    if (stored) {
      setToken(stored);
      fetchUser(stored);
    }
  }, [fetchUser]);

  const login = async (email: string, password: string) => {
    const res = await api.post<TokenResponse>("/auth/login", { email, password });
    const t = res.data.access_token;
    localStorage.setItem("token", t);
    setToken(t);
    await fetchUser(t);
  };

  const register = async (email: string, password: string, name: string) => {
    const res = await api.post<TokenResponse>("/auth/register", { email, password, name });
    const t = res.data.access_token;
    localStorage.setItem("token", t);
    setToken(t);
    await fetchUser(t);
  };

  const logout = () => {
    localStorage.removeItem("token");
    setToken(null);
    setUser(null);
  };

  const value: AuthContextType = {
    user,
    token,
    login,
    register,
    logout,
    isAuthenticated: !!token && !!user,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}
