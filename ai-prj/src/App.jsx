// src/App.jsx
import React,{ useState } from "react";
import Landing from "./components/landing";
import Board from "./components/Board";
import {  Routes, Route } from 'react-router-dom';

export default function App(){
  return (
    <Routes>
     <Route path = "/" element ={<Landing /> } /> 
     <Route path = "/board" element = {<Board />} /> 
     

    </Routes>
    
  );
}

