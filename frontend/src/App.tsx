import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import './App.css';
import Home from './route/Home/home'
import LogIn from './route/LogIn/log-in';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path='/' element={<Home />} />
        <Route path='/login' element={<LogIn />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
