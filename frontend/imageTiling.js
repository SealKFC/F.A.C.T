uploadImage = () => {
    const fileInput = document.getElementById('file_upload');

    const tile_base = document.getElementById("tile_base");
    tile_base.src = URL.createObjectURL(fileInput.files[0]);

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

savePattern = () => {
    fetch("http://localhost:5000/save_pattern", {method: 'POST'})
        .then((response) => {
            console.log("Pattern saved");
        })
        .catch((error) => {
            console.log("Error saving pattern");
        });
}