export const setToken = (token) => {
  localStorage.setItem("access_token", token);
};

export const getToken = () => {
  return localStorage.getItem("access_token");
};

export const isAdmin = () => {
  const token = getToken();
  if (token) {
    const payload = JSON.parse(atob(token.split(".")[1]));
    return payload.role === "admin";
  }
  return false;
};

export const logout = () => {
  localStorage.removeItem("access_token");
};
