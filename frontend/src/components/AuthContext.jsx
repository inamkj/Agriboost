import { createContext, useState, useEffect, useCallback } from "react";

export const AuthContext = createContext();

export function AuthProvider({ children }) {
  const [user, setUser] = useState(() => {
    const storedUser = localStorage.getItem("user");
    return storedUser ? JSON.parse(storedUser) : null;
  });

  useEffect(() => {
    // Keep localStorage in sync with state
    if (user) {
      localStorage.setItem("user", JSON.stringify(user));
    } else {
      localStorage.removeItem("user");
    }
  }, [user]);

  // Set the current user after successful login
  const loginUser = useCallback((nextUser, tokens) => {
    if (tokens?.access) localStorage.setItem("access", tokens.access);
    if (tokens?.refresh) localStorage.setItem("refresh", tokens.refresh);
    setUser(nextUser || null);
  }, []);

  // Clear all auth-related state and storage
  const logout = useCallback(() => {
    try {
      localStorage.removeItem("access");
      localStorage.removeItem("refresh");
      localStorage.removeItem("user");
    } catch (_) {}
    setUser(null);
  }, []);

  return (
    <AuthContext.Provider value={{ user, setUser, loginUser, logout }}>
      {children}
    </AuthContext.Provider>
  );
}
