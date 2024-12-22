import { useState } from "react";
import Header from "../Header";

const Collapsible = ({title, children}) => {
    /**
     * 
     * @param {string} title - The subtitle of the collapsible
     * @param {JSX.Elemeent} children - element stored inside of collapsible
     * @param {boolean} isOpen - Whether the collapsible is open or not
     */
    const [isOpen, setIsOpen] = useState(false);

    // handle click of collapse button
    const handleToggle = () => {
        if(isOpen) {
            setIsOpen(false);
            console.log("collapsible is now closed");
        } else if(!isOpen) {
            setIsOpen(true);
            console.log("collapsible is now open");
        }
    };

    return (
        <div 
            className={`collapsible ${isOpen ? 'open' : 'closed'}`}
        >
            <Header 
                title={title} 
                isCollapsible={true} 
                onToggle={handleToggle}
            />
            {isOpen && (
                <div className="collapsible-content">
                    {children}
                </div>            
            )}  
        </div>
    )
}

export default Collapsible;