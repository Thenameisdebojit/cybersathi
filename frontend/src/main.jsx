import React from "react";
import { createRoot } from "react-dom/client";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Dashboard from "./pages/Dashboard";
import "./styles.css";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/*" element={<Dashboard />} />
      </Routes>
    </BrowserRouter>
  );
}

createRoot(document.getElementById("root")).render(<App />);
