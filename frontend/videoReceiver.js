const socket = io("http://localhost:5000");

console.log("Connecting to server");

window.addEventListener('DOMContentLoaded', function() {
    img = document.getElementById("video");
});

socket.on("connect", () => {
    console.log("Connected to server");
});

socket.on("frame", (frame) => {
    if (img == null) {
        img = document.getElementById("video");
    } else {
        img.src = "data:image/jpeg;base64," + frame.image;
    }
});

startCamera = () => {
    fetch("http://localhost:5000/start_camera/angle")
        .then((response) => {
            console.log("Camera started");
        })
        .catch((error) => {
            console.log("Error starting camera");
        });
}

stopCamera = () => {
    fetch("http://localhost:5000/stop_camera")
        .then((response) => {
            console.log("Camera stopped");
        })
        .catch((error) => {
            console.log("Error stopping camera");
        });
}