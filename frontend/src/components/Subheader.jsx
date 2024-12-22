import React, { useState } from "react";


const Subheader = ({ title, isCollapsible, onToggle }) => {
  /**
   * @param {str} title - title of header component
   * @param {bool} iscollapsible - wether the header contains a collapsible button
   * @param {bool} onToggle - when the collapse button is clicked
   */

  const [isCollapsed, setIsCollapsed] = useState(false);

  return (
    <div className="header">
      <div className="subheading">{title}</div>
      {!isCollapsible ? null : (
        <>
          <button 
            onClick={() => {
              setIsCollapsed(!isCollapsed);
              onToggle();
            }} 
            className="collapsible-button"
          >
            {isCollapsed ? (
              <i class="fa-solid fa-chevron-right"></i>
            ) : (
              <i class="fa-solid fa-chevron-left"></i>
            )}
          </button>
        </>
      )}
    </div>
  );
};

export default Subheader;
