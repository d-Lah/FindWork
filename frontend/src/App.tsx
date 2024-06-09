import React from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import "./App.css";
import Home from "./route/Home/home";
import LogIn from "./route/LogIn/log-in";
import Register from "./route/Register/register";
import ActivateUser from "./route/ActivateUser/activate-user";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/login" element={<LogIn />} />
        <Route path="/register" element={<Register />} />
        <Route path="/activate-user/:userActivationUUID" element={<ActivateUser />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
