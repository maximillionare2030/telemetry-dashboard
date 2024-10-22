// fsae-telemetry-dashboard/frontend/src/AppRouter.js
import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Header from './components/Header.jsx'; // Adjust the path if necessary
import Home from './pages/Home.jsx'; // Create this component
import NotFound from './pages/NotFound.jsx'; 

const AppRouter = () => {
  return (
    <Router>
      <Header />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="*" element={<NotFound />} />
      </Routes>
    </Router>
  );
};

export default AppRouter;
