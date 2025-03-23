import React from "react";
import AppRoutes from "./routes/AppRoutes";
import "./styles/App.css";
import { AuthProvider } from "./context/AuthContext";

function App() {
  return (
    <AuthProvider>
      <AppRoutes />
    </AuthProvider>
  );
}

export default App;
