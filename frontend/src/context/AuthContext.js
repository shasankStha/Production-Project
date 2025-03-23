import { createContext, useContext, useEffect, useState } from "react";
import { getToken, setToken, removeToken, decodeToken } from "../utils/Auth";

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);

  useEffect(() => {
    const token = getToken();
    if (token) {
      const decoded = decodeToken(token);
      setUser(decoded?.sub || null);
    }
  }, []);

  const login = (token) => {
    setToken(token);
    const decoded = decodeToken(token);
    setUser(decoded?.sub || null);
  };

  const logout = () => {
    removeToken();
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

// Custom hook to use AuthContext
export const useAuth = () => useContext(AuthContext);
