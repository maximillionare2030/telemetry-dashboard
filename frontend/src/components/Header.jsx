import React from 'react';

const Header = ({title, isCollapsable, onToggle}) => {
    /**
     * @param {str} title - title of header component
     * @param {bool} isCollapsable - wether the header contains a collapsable button
     * @param {bool} onToggle - when the collapse button is clicked
     */
    
    return(
        <div className="header">
            <h2>{title}</h2>
            {!isCollapsable ? 
            null
            : <div className="collapsable-button">
                <button onClick={onToggle}>
                    <h2>-</h2>
                </button>
            </div>}
        </div>
    )
}

export default Header;