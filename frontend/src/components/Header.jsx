import React from "react";

const Header = () => {
  return (
    <nav className="header">
      {["Overview", "Power", "Motor", "Microcontroller"].map((item) => (
        <div
          key={item}
          className="header-item"
        >
          <a
            href={`/${item.toLowerCase()}`}
            aria-label={`Navigate to ${item}`}
            className="header-link"
          >
            {item}
          </a>
        </div>
      ))}
    </nav>
  );
};

export default Header;
