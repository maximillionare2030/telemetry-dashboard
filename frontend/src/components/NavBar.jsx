import React from "react";
import { Link, useLocation } from "react-router-dom";
import anteaterLogo from "../images/anteaterLogoWide.svg";

const navItems = [
  { name: "Home", icon: "fa-solid fa-house" },
  { name: "Log", icon: "fa-solid fa-file-lines" },
]
const NavBar = () => {
  // get the current path
  const location = useLocation();

  return (
    <nav className="navbar">
      <img src={anteaterLogo} alt="anteaterLogo" style={{ width: "80px" }}/>
      <div className="divider"></div>
      {navItems.map((item) => {
        const path = `/${item.name.toLowerCase()}`;
        const isActive = location.pathname === path; // check if the current path is the same as the item path
        return (
        <div
          key={item.name}
          className="nav-item"
        >
          <Link 
            to={path}
            className={`nav-link ${isActive ? 'active' : ''}`}
          >
            <i className={item.icon}></i>
            {item.name}
          </Link>

        </div>
        );
      })}
    </nav>
  )
}

export default NavBar;