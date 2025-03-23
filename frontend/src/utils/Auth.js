export const setToken = (token) => {
  localStorage.setItem("token", token);
};

export const getToken = () => {
  return localStorage.getItem("token");
};

export const removeToken = () => {
  localStorage.removeItem("token");
};

export const decodeToken = (token) => {
  try {
    const base64Payload = token.split(".")[1];
    if (!base64Payload) return null;
    return JSON.parse(atob(base64Payload));
  } catch (error) {
    console.error("Error decoding token:", error);
    return null;
  }
};

export const isAdmin = () => {
  const token = getToken();
  if (!token) return false;
  const decoded = decodeToken(token);
  return decoded?.sub?.role === "admin";
};
