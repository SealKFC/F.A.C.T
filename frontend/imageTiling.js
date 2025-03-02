shirt_image = document.getElementById("shirt_image");
pants_image = document.getElementById("pants_image");

updateShirtTile = () => {
    socket.emit("tile_size_shirt", {
        tile_x: document.getElementById("tile_x_shirt").value,
        tile_y: document.getElementById("tile_y_shirt").value
    })
}

updatePantsTile = () => {
    socket.emit("tile_size_pants", {
        tile_x: document.getElementById("tile_x_pants").value,
        tile_y: document.getElementById("tile_y_pants").value
    })
}

socket.on("shirt_image", (frame) => {
    if (shirt_image == null) {
        shirt_image = document.getElementById("shirt_image");
    } else {
        shirt_image.src = "data:image/jpeg;base64," + frame;
    }
});

socket.on("pants_image", (frame) => {
    if (pants_image == null) {
        pants_image = document.getElementById("pants_image");
    } else {
        pants_image.src = "data:image/jpeg;base64," + frame;
    }
});

saveShirt = () => {
    fetch("http://localhost:5000/save_shirt", {method: 'POST'})
        .then((response) => {
            console.log("Pattern saved");
        })
        .catch((error) => {
            console.log("Error saving pattern");
        });
}

savePants = () => {
    fetch("http://localhost:5000/save_pants", {method: 'POST'})
        .then((response) => {
            console.log("Pattern saved");
        })
        .catch((error) => {
            console.log("Error saving pattern");
        });
}

uploadShirt = () => {
    maxWidth = 300;
    maxHeight = 300;

    const shirt_tile_base = document.getElementById("tile_base_shirt");

    const shirt_upload = document.getElementById('tile_upload_shirt');
    const file = shirt_upload.files[0];

    const reader = new FileReader();

    reader.onload = function (event) {
        const img = new Image();
        img.onload = function () {
            let width = img.width;
            let height = img.height;

            // Calculate new dimensions while maintaining aspect ratio
            if (width > maxWidth || height > maxHeight) {
                if (width > height) {
                    height = Math.round((maxWidth / width) * height);
                    width = maxWidth;
                } else {
                    width = Math.round((maxHeight / height) * width);
                    height = maxHeight;
                }
            }

            // Resize image using canvas
            const canvas = document.createElement("canvas");
            canvas.width = width;
            canvas.height = height;
            const ctx = canvas.getContext("2d");
            ctx.drawImage(img, 0, 0, width, height);

            // Convert canvas to Blob
            canvas.toBlob((blob) => {
                shirt_tile_base.src = URL.createObjectURL(blob);

                const formData = new FormData();
                formData.append('image', blob);
                fetch("http://localhost:5000/upload_shirt_tile", {
                    method: 'POST',
                    body: formData
                }).then((response) => {
                    console.log("Image uploaded");

                    // Update the tile image
                    updateShirtTile();
                }).catch((error) => {
                    console.log("Error uploading image");
                });
            }, file.type);
        };
        img.src = event.target.result;
    };

    reader.readAsDataURL(file);
}

uploadPants = () => {
    maxWidth = 300;
    maxHeight = 300;

    const pants_tile_base = document.getElementById("tile_base_pants");

    const pants_upload = document.getElementById('tile_upload_pants');
    const file = pants_upload.files[0];

    const reader = new FileReader();

    reader.onload = function (event) {
        const img = new Image();
        img.onload = function () {
            let width = img.width;
            let height = img.height;

            // Calculate new dimensions while maintaining aspect ratio
            if (width > maxWidth || height > maxHeight) {
                if (width > height) {
                    height = Math.round((maxWidth / width) * height);
                    width = maxWidth;
                } else {
                    width = Math.round((maxHeight / height) * width);
                    height = maxHeight;
                }
            }

            // Resize image using canvas
            const canvas = document.createElement("canvas");
            canvas.width = width;
            canvas.height = height;
            const ctx = canvas.getContext("2d");
            ctx.drawImage(img, 0, 0, width, height);

            // Convert canvas to Blob
            canvas.toBlob((blob) => {
                pants_tile_base.src = URL.createObjectURL(blob);

                const formData = new FormData();
                formData.append('image', blob);
                fetch("http://localhost:5000/upload_pants_tile", {
                    method: 'POST',
                    body: formData
                }).then((response) => {
                    console.log("Image uploaded");

                    // Update the tile image
                    updatePantsTile();
                }).catch((error) => {
                    console.log("Error uploading image");
                });
            }, file.type);
        };
        img.src = event.target.result;
    };

    reader.readAsDataURL(file);
}