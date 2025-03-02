// Initiate the socket connection.
const socket = io("http://localhost:5000");

// Tiling update functions: these emit the current slider values.
function updateShirtTile() {
    socket.emit("tile_size_shirt", {
    tile_x: document.getElementById("tile_x_shirt").value,
    tile_y: document.getElementById("tile_y_shirt").value
    });
}

function updatePantsTile() {
    socket.emit("tile_size_pants", {
    tile_x: document.getElementById("tile_x_pants").value,
    tile_y: document.getElementById("tile_y_pants").value
    });
}

// Socket listeners to update the display images from backend frames.
socket.on("shirt_image", (frame) => {
    const shirtImg = document.getElementById("shirt_image");
    if (shirtImg) {
    shirtImg.src = "data:image/jpeg;base64," + frame;
    }
    // Hide the loading indicator once an image is received.
    document.getElementById("loading_shirt").style.display = "none";
    document.getElementById("shirt_image").style.opacity = 1;
});

socket.on("pants_image", (frame) => {
    const pantsImg = document.getElementById("pants_image");
    if (pantsImg) {
    pantsImg.src = "data:image/jpeg;base64," + frame;
    }
    // Hide the loading indicator once an image is received.
    document.getElementById("loading_pants").style.display = "none";
    document.getElementById("pants_image").style.opacity = 1;
});

// When uploading starts, show the loading indicator.
function showLoading(id) {
    document.getElementById(id).style.display = "flex";
}

// Upload functions with image resizing using canvas.
function uploadShirt() {
    const maxWidth = 300, maxHeight = 300;
    const shirt_upload = document.getElementById('tile_upload_shirt');
    const file = shirt_upload.files[0];
    if (!file) {
    updateShirtTile();
    return;
    }
    // Show loading indicator
    showLoading("loading_shirt");
    const reader = new FileReader();
    reader.onload = function (event) {
    const img = new Image();
    img.onload = function () {
        let width = img.width, height = img.height;
        if (width > maxWidth || height > maxHeight) {
        if (width > height) {
            height = Math.round((maxWidth / width) * height);
            width = maxWidth;
        } else {
            width = Math.round((maxHeight / height) * width);
            height = maxHeight;
        }
        }
        const canvas = document.createElement("canvas");
        canvas.width = width;
        canvas.height = height;
        const ctx = canvas.getContext("2d");
        ctx.drawImage(img, 0, 0, width, height);
        canvas.toBlob((blob) => {
        const formData = new FormData();
        formData.append('image', blob);
        fetch("http://localhost:5000/upload_shirt_tile", {
            method: 'POST',
            body: formData
        }).then(() => {
            console.log("Shirt image uploaded");
            updateShirtTile();
        }).catch(() => {
            console.log("Error uploading shirt image");
        });
        }, file.type);
    };
    img.src = event.target.result;
    };
    reader.readAsDataURL(file);
}

function uploadPants() {
    const maxWidth = 300, maxHeight = 300;
    const pants_upload = document.getElementById('tile_upload_pants');
    const file = pants_upload.files[0];
    if (!file) {
    updatePantsTile();
    return;
    }
    // Show loading indicator
    showLoading("loading_pants");
    const reader = new FileReader();
    reader.onload = function (event) {
    const img = new Image();
    img.onload = function () {
        let width = img.width, height = img.height;
        if (width > maxWidth || height > maxHeight) {
        if (width > height) {
            height = Math.round((maxWidth / width) * height);
            width = maxWidth;
        } else {
            width = Math.round((maxHeight / height) * width);
            height = maxHeight;
        }
        }
        const canvas = document.createElement("canvas");
        canvas.width = width;
        canvas.height = height;
        const ctx = canvas.getContext("2d");
        ctx.drawImage(img, 0, 0, width, height);
        canvas.toBlob((blob) => {
        const formData = new FormData();
        formData.append('image', blob);
        fetch("http://localhost:5000/upload_pants_tile", {
            method: 'POST',
            body: formData
        }).then(() => {
            console.log("Pants image uploaded");
            updatePantsTile();
        }).catch(() => {
            console.log("Error uploading pants image");
        });
        }, file.type);
    };
    img.src = event.target.result;
    };
    reader.readAsDataURL(file);
}

// Automatically upload images when a file is selected.
document.getElementById("tile_upload_shirt").addEventListener("change", uploadShirt);
document.getElementById("tile_upload_pants").addEventListener("change", uploadPants);

// Update tiling whenever slider values change.
document.getElementById("tile_x_shirt").addEventListener("input", updateShirtTile);
document.getElementById("tile_y_shirt").addEventListener("input", updateShirtTile);
document.getElementById("tile_x_pants").addEventListener("input", updatePantsTile);
document.getElementById("tile_y_pants").addEventListener("input", updatePantsTile);

function saveShirt() {
    fetch("http://localhost:5000/save_shirt", {method: 'POST'})
    .then((response) => {
        console.log("Pattern saved");
        document.getElementById('shirt_image').src = 'assets/white-shirt.png';
        document.getElementById("shirt_image").style.opacity = 0.5;
        fetchShirts();
    })
    .catch((error) => {
        console.log("Error saving pattern");
    });
}

function savePants() {
    fetch("http://localhost:5000/save_pants", {method: 'POST'})
        .then((response) => {
            console.log("Pattern saved");
            document.getElementById('pants_image').src = 'assets/white-pants.png';
            document.getElementById("pants_image").style.opacity = 0.5;
            fetchPants();
        })
        .catch((error) => {
            console.log("Error saving pattern");
        });
}