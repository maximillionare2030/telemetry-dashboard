import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Home from './pages/Home.jsx'; 
import NotFound from './pages/NotFound.jsx'; 
import Log from './pages/Log.jsx';

const AppRouter = () => {
    return (
        <Router>
            <Routes>
                <Route path="/" element={<Home/>} />
                <Route path="/home" element={<Home/>} />
                <Route path="/log" element={<Log/>} />
                <Route path="*" element={<NotFound />} />
                <Route path="/:extension" element={<Home/> } />
            </Routes>
        </Router>
    );
};

export default AppRouter;