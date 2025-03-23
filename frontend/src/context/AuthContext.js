import { createContext, useContext, useEffect, useState } from "react";
import { getToken, setToken, removeToken, decodeToken } from "../utils/Auth";

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const token = getToken();
    if (token) {
      const decoded = decodeToken(token);
      setUser(decoded?.sub || null);
    }
    setLoading(false);
  }, []);

  const login = (token) => {
    setToken(token);
    const decoded = decodeToken(token);
    setUser(decoded?.sub || null);
  };

  const logout = () => {
    removeToken();
    setUser(null);
    window.location.reload();
  };

  if (loading) {
    return <div>Loading...</div>;
  }

  return (
    <AuthContext.Provider value={{ user, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);
