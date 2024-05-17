import "./navbar.css";
import React, { useState, useEffect } from "react";

function Navbar() {
  let authorization = localStorage.getItem("authorization");

  const [menuButtonBool, setMenuButtonStatus] = useState(false);
  function switchMenu() {
    let navbarCollapse = document.getElementById("navbarCollapse");

    if (!menuButtonBool) {
      navbarCollapse?.classList.add("show");
      setMenuButtonStatus(!menuButtonBool);
      return;
    }
    setMenuButtonStatus(!menuButtonBool);
    navbarCollapse?.classList.remove("show");
    return;
  }

  var logIn = (
    <li>
      <a href="/" className="nav-link">
        Log in
      </a>
    </li>
  );
  var profile = (
    <li>
      <a href="/" className="nav-link">
        Profile
      </a>
    </li>
  );

  return (
    <nav className="navbar d-flex">
      <div className="navbar-container d-flex">
        <div className="navbar-header d-flex">
          <a href="/" className="navbar-logo">
            Find Work
          </a>
          <button onClick={switchMenu} className="navbar-menu ml-auto">
            <span className="material-icons">menu</span>
          </button>
        </div>
        <div id="navbarCollapse" className="navbar-collapse collapse">
          <ul className="navbar-nav d-flex">
            <li className="nav-item">
              <a href="/" className="nav-link bgc-hover">
                Employs
              </a>
            </li>
            <li className="nav-item">
              <a href="/" className="nav-link bgc-hover">
                Vacancys
              </a>
            </li>
          </ul>
          <ul className="navbar-nav ml-auto d-flex">
            {!authorization ? (
              logIn
            ) : (
              profile
            )}
          </ul>
        </div>
      </div>
    </nav>
  );
}

export default Navbar;
