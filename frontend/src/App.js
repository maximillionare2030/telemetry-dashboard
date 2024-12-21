import React from 'react';
import AppRouter from './AppRouter'; // import the router to use routes
import './styles/App.sass';
import './styles/components.sass';
import './styles/global.sass';

function App() {
  return (
    <div className="App">
      <AppRouter /> 
    </div>
  );
}

export default App;
