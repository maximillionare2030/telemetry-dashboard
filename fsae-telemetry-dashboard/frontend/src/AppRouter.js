import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Home from './pages/Home.jsx'; 
import NotFound from './pages/NotFound.jsx'; 


const AppRouter = () => {
    return (
        <Router>
            <Routes>
                <Route path="/" element={<Home/>} />
                <Route path="*" element={<NotFound />} />
                <Route path="/:component" element={<Home/> } />
                
            </Routes>
        </Router>
    );
};

export default AppRouter;