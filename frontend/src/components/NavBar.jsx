import React from "react";
import { Link } from "react-router-dom";

const navItems = [
  { name: "Home", icon: "fa-solid fa-house" },
  { name: "Log", icon: "fa-solid fa-file-lines" },
]
const NavBar = () => {
  return (
    <nav className="navbar">
      {navItems.map((item) => (
        <div
          key={item.name}
          className="nav-item"
        >
          <Link 
            to={`/${item.name.toLowerCase()}`}
            className="nav-link"
          >
            <i className={item.icon}></i>
            {item.name}
          </Link>

        </div>
      ))}
    </nav>
  )
}

export default NavBar;