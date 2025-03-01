uploadImage = () => {
    const fileInput = document.getElementById('file_upload');

    const formData = new FormData();
    formData.append('image', fileInput.files[0]);
    fetch("http://localhost:5000/upload_tile_image", {
        method: 'POST',
        body: formData
    }).then((response) => {
        console.log("Image uploaded");

        // Update the tile image
        updateTile();
    }).catch((error) => {
        console.log("Error uploading image");
    });
}

updateTile = () => {
    socket.emit("tile_size", {
        tile_x: document.getElementById("tile_x").value,
        tile_y: document.getElementById("tile_y").value
    })
}

socket.on("tiled_image", (frame) => {
    if (tile_image == null) {
        tile_image = document.getElementById("tile_image");
    } else {
        tile_image.src = "data:image/jpeg;base64," + frame;
    }
});