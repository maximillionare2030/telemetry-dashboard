import React from "react";

const NavBar = () => {
  return (
    <nav>
      {["Overview", "Power", "Motor", "Microcontroller"].map((item) => (
        <div
          key={item}
          className="nav-item"
        >
          <a
            href={`/${item.toLowerCase()}`}
            aria-label={`Navigate to ${item}`}
            className="nav-link"
          >
            {item}
          </a>
        </div>
      ))}
    </nav>
  );
};

export default NavBar;
