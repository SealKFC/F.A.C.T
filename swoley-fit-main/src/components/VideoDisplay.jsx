import React, { useEffect, useState } from 'react';
import { io } from 'socket.io-client';

// Connect to your backend (update the URL/port as needed)
const socket = io('http://localhost:5000');
window.socket = socket;

const VideoDisplay = ({ model }) => {
  const [imageSrc, setImageSrc] = useState(null);
  const [counter, setCounter] = useState(0);
  const [predictedClass, setPredictedClass] = useState('');
  const [confidence, setConfidence] = useState(0.0);

  // Log the model prop and fetch data from socket based on the selected model
  useEffect(() => {
    console.log("Selected Model:", model);  // Log the active model to verify selection

    // Connect to the socket and listen for frames
    socket.on('connect', () => {
      console.log('Connected to backend');
    });

    socket.on('frame', (data) => {
      console.log('Received frame data:', data);

      // Assuming the frame data contains the same structure across models
      setImageSrc('data:image/jpeg;base64,' + data.image);
      setCounter(data.counter);
      setPredictedClass(data.predicted_class);
      setConfidence(data.confidence);
    });

    // Cleanup the socket connection on component unmount
    return () => {
      socket.off('connect');
      socket.off('frame');
    };
  }, [model]);  // Re-run the effect when the model prop changes

  return (
    <div
      style={{
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        height: '100vh', // Full viewport height
        background: 'linear-gradient(to right, #2E2E2E, #000000)', // Optional background
        position: 'relative'
      }}
    >
      {imageSrc ? (
        <div style={{ position: 'relative' }}>
          {/* Video feed image with rounded corners */}
          <img
            src={imageSrc}
            alt="Live feed"
            style={{
              borderRadius: '20px', // Adjust this value to smooth out edges
              //maxWidth: '640px',
              width: '100%',
              height: '100%',
              display: 'block'
            }}
          />
         
          {/* Optionally, you can also display additional data (counter, stage, etc.) below or on top of the video */}
          <div
            style={{
              position: 'absolute',
              top: '10px',
              left: '10px',
              backgroundColor: 'rgba(0, 0, 0, 0.5)',
              padding: '5px 10px',
              borderRadius: '5px',
              color: 'white'
            }}
          >
            <p>Reps: {counter}</p>
            <p>Stage: {predictedClass}</p>
            <p>Confidence: {confidence.toFixed(2)}</p>
          </div>
        </div>
      ) : (
        <p style={{ color: 'white' }}>Waiting for video stream...</p>
      )}
    </div>
  );
};

export default VideoDisplay;