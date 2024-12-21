import { useState } from "react";
import Header from "../Header";

const Collapsable = ({title, children}) => {
    /**
     * 
     * @param {string} title - The subtitle of the collapsable
     * @param {JSX.Elemeent} children - element stored inside of collapsible
     * @param {boolean} isOpen - Whether the collapsable is open or not
     */
    const [isOpen, setIsOpen] = useState(false);

    // handle click of collapse button
    const handleToggle = () => {
        if(isOpen) {
            setIsOpen(false);
            console.log("Collapsable is now closed");
        } else if(!isOpen) {
            setIsOpen(true);
            console.log("Collapsable is now open");
        }
    };

    return (
        <div>
            <Header 
                title={title} 
                isCollapsable={true} 
                onToggle={handleToggle}
            />
            {isOpen &&
            (
                <div className="collapsable-content">
                    {children}
                    hello
                </div>
                
            )}  
        </div>
    )
}

export default Collapsable;