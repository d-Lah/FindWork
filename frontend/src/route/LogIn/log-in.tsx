// import React, { useState, useEffect } from "react";
import "./log-in.css";

function LogIn() {
  return (
    <div className="login-container">
      <div className="login-box">
        <input type="email" placeholder="Email" required />
        <input type="password" placeholder="Password" required />
        <a href="#" className="forgot-password">
          Forgot password?
        </a>
        <p>
          No account?{" "}
          <a href="#" className="register">
            Register
          </a>
        </p>
        <button type="submit">Log In</button>
      </div>
    </div>
  );
}

export default LogIn;
