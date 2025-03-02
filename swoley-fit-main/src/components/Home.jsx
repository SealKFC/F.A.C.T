// Home.jsx
import React from 'react';
import { useNavigate } from 'react-router-dom';
import Button from './Button';

const Home = () => {
  const navigate = useNavigate();

  const handleStartCamera = async () => {
    try {
      const res = await fetch('http://localhost:5000/start_camera');
      const data = await res.json();
      console.log("API Response:", data.status);
    } catch (error) {
      console.error("Error starting camera:", error);
    }
    navigate('/video');
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-slate-800 text-white">
      <Button func={handleStartCamera} text="Start Camera" />
    </div>
  );
};

export default Home;
