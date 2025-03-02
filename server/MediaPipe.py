import pickle  # If you plan to use the model later
import cv2
import base64
import mediapipe as mp
import numpy as np
import pandas as pd
from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
import warnings
import os
from flask_cors import CORS
import cvzone
from cvzone.PoseModule import PoseDetector  # Remove if not used
from werkzeug.utils import secure_filename
from io import BytesIO
from PIL import Image

warnings.filterwarnings(
    "ignore", 
    message="X does not have valid feature names, but RobustScaler was fitted with feature names"
)

# Initialize MediaPipe
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils

# Create Flask and WebSocket (SocketIO) server
app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")  # Allow cross-origin requests

# Landmarking
feature_columns = [f'{coord}{i}' for i in range(1, 34) for coord in ['x', 'y', 'z', 'v']]

is_streaming = False
show_angles = False
needs_update = True

# Folder paths
shirtFolderPath = "Resources/Shirts"
pantFolderPath = "Resources/Pants"

# Cache for shirt and pant images to reduce disk I/O
shirt_cache = {}
pant_cache = {}

def update_shirt_cache():
    global shirt_cache, needs_update
    shirt_cache.clear()
    for filename in os.listdir(shirtFolderPath):
        path = os.path.join(shirtFolderPath, filename)
        img = cv2.imread(path, cv2.IMREAD_UNCHANGED)
        if img is not None:
            shirt_cache[filename] = img
    needs_update = False

def update_pant_cache():
    global pant_cache
    pant_cache.clear()
    for filename in os.listdir(pantFolderPath):
        path = os.path.join(pantFolderPath, filename)
        img = cv2.imread(path, cv2.IMREAD_UNCHANGED)
        if img is not None:
            pant_cache[filename] = img

imgButtonRight = cv2.imread("Resources/button.png", cv2.IMREAD_UNCHANGED)
imgButtonLeft = cv2.flip(imgButtonRight, 1)

# Ratios for resizing overlays
fixedRatio = 262 / 190
clotheRatioHeightWidth = 581 / 440
imageNumber = 0  # index for currently selected shirt image
counterRight = 0
counterLeft = 0
selectionSpeed = 20

# Limited Starting
@app.route('/start_camera/<variant>', methods=['GET'])
def start_camera(variant):
    global is_streaming, show_angles, needs_update
    show_angles = (variant == 'angle')
    if not is_streaming:
        # Update caches on first stream start
        update_shirt_cache()
        update_pant_cache()
        socketio.start_background_task(stream_video)
        is_streaming = True
        return jsonify({'status': 'Camera streaming started'}), 200
    else:
        return jsonify({'status': 'Camera streaming already running'}), 200

# Global Stopping
@app.route('/stop_camera', methods=['GET'])
def stop_camera():
    global is_streaming
    is_streaming = False
    return jsonify({'status': 'Camera streaming stopped'}), 200

from dogshit import create_tile

@app.route("/upload_shirt_tile", methods=["POST"])
def upload_shirt_tile():
    if "image" not in request.files:
        return jsonify({"error": "No image uploaded"}), 400
    request.files["image"].save("Resources/shirt_upload.png")
    create_tile("Resources/shirt_upload.png", "Resources/shirt_base_tile.png")
    return jsonify({"status": "Tile image uploaded"}), 200

@app.route("/upload_pants_tile", methods=["POST"])
def upload_pants_tile():
    if "image" not in request.files:
        return jsonify({"error": "No image uploaded"}), 400
    request.files["image"].save("Resources/pants_upload.png")
    create_tile("Resources/pants_upload.png", "Resources/pants_base_tile.png")
    return jsonify({"status": "Tile image uploaded"}), 200

@app.route("/get_shirts_list", methods=["GET"])
def get_shirts_list():
    # Adjust the folder path as needed. Here we assume it's relative to the current working directory.
    folder_path = os.path.join(os.getcwd(), "Resources", "Shirts")
    
    images = []
    # Loop over all files in the folder
    for file in os.listdir(folder_path):
        # Optionally filter by image file extensions
        if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
            images.append(file)
    
    return jsonify(images)

@app.route("/get_pants_list", methods=["GET"])
def get_pants_list():
    # Adjust the folder path as needed. Here we assume it's relative to the current working directory.
    folder_path = os.path.join(os.getcwd(), "Resources", "Pants")
    
    images = []
    # Loop over all files in the folder
    for file in os.listdir(folder_path):
        # Optionally filter by image file extensions
        if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
            images.append(file)
    
    return jsonify(images)

@app.route("/save_shirt", methods=["POST"])
def save_shirt():
    global shirt, needs_update

    needs_update = True

    # Define common image file extensions
    image_extensions = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".webp"}
    # Count the number of image files in the folder
    image_count = sum(1 for file in os.listdir("Resources/Shirts") if os.path.splitext(file)[1].lower() in image_extensions)
    imageFileName = f"T-Shirt_{image_count + 1}.png"

    shirt.save(f"Resources/Shirts/{imageFileName}")
    return jsonify({"status": "Tile image saved"}), 200

@app.route("/save_pants", methods=["POST"])
def save_pants():
    global pants, needs_update

    needs_update = True

    # Define common image file extensions
    image_extensions = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".webp"}
    # Count the number of image files in the folder
    image_count = sum(1 for file in os.listdir("Resources/Pants") if os.path.splitext(file)[1].lower() in image_extensions)
    imageFileName = f"Pants_{image_count + 1}.png"

    pants.save(f"Resources/Pants/{imageFileName}")
    return jsonify({"status": "Tile image saved"}), 200

@app.route("/upload_shirt", methods=["POST"])
def upload_shirt():
    global needs_update, shirt_cache, imageNumber
    if "image" not in request.files:
        return jsonify({"error": "No image uploaded"}), 400
    
    file = request.files["image"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400
    
    filename = secure_filename(file.filename)
    shirt_path = os.path.join(shirtFolderPath, filename)
    file.save(shirt_path)
    
    # Update cache after uploading a new shirt
    needs_update = True
    update_shirt_cache()
    imageNumber = 0
    return jsonify({"status": "Shirt image uploaded successfully."}), 200

def generate_frames():
    global is_streaming, imageNumber, counterRight, counterLeft, needs_update
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 848)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    
    predicted_class = None

    with mp_pose.Pose(min_detection_confidence=0.5,
                    min_tracking_confidence=0.5) as pose:
        while cap.isOpened():
            if not is_streaming:
                break

            if needs_update:
                update_shirt_cache()

            ret, frame = cap.read()
            if not ret:
                break

            # Convert frame from BGR to RGB
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False  # Improve performance.
            results = pose.process(image)
            image.flags.writeable = True   # Allow drawing.
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            # Draw pose landmarks
            mp_drawing.draw_landmarks(
                image,
                results.pose_landmarks,
                mp_pose.POSE_CONNECTIONS,
                mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=2),
                mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2)
            )
            
            confidence_value = 0.0

            if results.pose_landmarks:
                landmarks = results.pose_landmarks.landmark
                h, w, _ = image.shape
                #print(w, h)

                lm11 = [int(landmarks[11].x * w), int(landmarks[11].y * h)]
                lm12 = [int(landmarks[12].x * w), int(landmarks[12].y * h)]
                lm23 = [int(landmarks[23].x * w), int(landmarks[23].y * h)]
                lm24 = [int(landmarks[24].x * w), int(landmarks[24].y * h)]
                lm28 = [int(landmarks[28].x * w), int(landmarks[28].y * h)]
                lm15 = [int(landmarks[15].x * w), int(landmarks[15].y * h)]
                lm16 = [int(landmarks[16].x * w), int(landmarks[16].y * h)]

                pantHeightFromPose = abs(lm28[1] - lm24[1])

                shirt_keys = sorted(shirt_cache.keys())
                if shirt_keys:
                    current_shirt_key = shirt_keys[imageNumber % len(shirt_keys)]
                    imgShirt = shirt_cache[current_shirt_key]
                else:
                    imgShirt = None

                if imgShirt is not None:
                    widthOfShirt = int(abs(lm11[0] - lm12[0]) * fixedRatio)
                    widthOfShirt = max(widthOfShirt, 1)
                    heightOfShirt = int(widthOfShirt * clotheRatioHeightWidth)
                    heightOfShirt = max(heightOfShirt, 1)
                    try:
                        imgShirt_resized = cv2.resize(imgShirt, (widthOfShirt, heightOfShirt))
                    except Exception:
                        imgShirt_resized = None

                    if imgShirt_resized is not None:
                        currentScale = (lm11[0] - lm12[0]) / 190
                        offset = (int(44 * currentScale), int(48 * currentScale))
                        try:
                            image = cvzone.overlayPNG(image, imgShirt_resized, (lm12[0] - offset[0], lm12[1] - offset[1]))
                        except Exception:
                            pass

                # Retrieve current pant image from cache using sorted keys
                pant_keys = sorted(pant_cache.keys())
                if pant_keys:
                    current_pant_key = pant_keys[imageNumber % len(pant_keys)]
                    imgPant = pant_cache[current_pant_key]
                else:
                    imgPant = None

                if imgPant is not None:
                    middleHipX = (lm23[0] + lm24[0]) // 2
                    middleHipY = (lm23[1] + lm24[1]) // 2
                    pant_orig_height, pant_orig_width = imgPant.shape[:2]
                    scale = pantHeightFromPose / pant_orig_height
                    widthOfPant = int(pant_orig_width * scale)
                    heightOfPant = int(pant_orig_height * scale)
                    try:
                        imgPant_resized = cv2.resize(imgPant, (widthOfPant + 15, heightOfPant))
                    except Exception:
                        imgPant_resized = None

                    if imgPant_resized is not None:
                        offsetX = middleHipX - (imgPant_resized.shape[1] // 2)
                        offsetY = middleHipY
                        overlayPosition = (offsetX, offsetY)
                        try:
                            image = cvzone.overlayPNG(image, imgPant_resized, overlayPosition)
                        except Exception:
                            pass

                height = int(h * 0.4)
                widthR = 680
                widthL = 40
                image = cvzone.overlayPNG(image, imgButtonRight, (widthR, height))
                image = cvzone.overlayPNG(image, imgButtonLeft, (widthL, height))
                
                if lm15[0] > 680:
                    counterLeft += 1
                    cv2.ellipse(image, (widthR + 64, height + 67), (66, 66), 0, 0,
                                counterLeft * selectionSpeed, (0, 255, 0), 20)
                    if counterLeft * selectionSpeed > 360:
                        counterLeft = 0
                        if imageNumber > 0:
                            imageNumber += 1
                elif lm16[0] < 136:
                    counterRight += 1
                    cv2.ellipse(image, (widthL + 64, height + 67), (66, 66), 0, 0,
                                counterRight * selectionSpeed, (0, 255, 0), 20)
                    if counterRight * selectionSpeed > 360:
                        counterRight = 0
                        if imageNumber < len(shirt_keys) - 1:
                            imageNumber -= 1
                else:
                    counterRight = 0
                    counterLeft = 0

            
            # encode frame as jpeg to be transmitted to frontend
            ret, buffer = cv2.imencode('.jpg', image)
            frame_encoded = base64.b64encode(buffer).decode('utf-8')

            # Yield a dictionary with all the information.
            yield {
                'image': frame_encoded,
                'counter': 0,
                'predicted_class': predicted_class,
                'confidence': confidence_value
            }         

    cap.release()
    cv2.destroyAllWindows()

@socketio.on('connect')
def handle_connect():
    print("Client connected")
    emit('message', {'data': 'Connected to MediaPipe backend'})

from pattern import pattern
from TshirtOverlay import overlay
from io import BytesIO
import base64
shirt = None
pants = None

@socketio.on("tile_size_shirt")
def tile_size_shirt(data):
    global shirt
    tile_x = data.get('tile_x', 3)
    tile_y = data.get('tile_y', 3)

    tiled_image = pattern("Resources/shirt_base_tile.png", tile_x, tile_y)
    base = Image.open("Resources/Shirts/1.png").convert("RGBA")
    shirt = overlay(base, tiled_image)

    buffer = BytesIO()
    shirt.save(buffer, format="PNG")
    img_str = base64.b64encode(buffer.getvalue()).decode("utf-8")

    emit('shirt_image', img_str)

@socketio.on("tile_size_pants")
def tile_size_pants(data):
    global pants
    tile_x = data.get('tile_x', 3)
    tile_y = data.get('tile_y', 3)

    tiled_image = pattern("Resources/pants_base_tile.png", tile_x, tile_y)
    base = Image.open("Resources/Pants/beige_pants.png").convert("RGBA")
    pants = overlay(base, tiled_image)

    buffer = BytesIO()
    pants.save(buffer, format="PNG")
    img_str = base64.b64encode(buffer.getvalue()).decode("utf-8")

    emit('pants_image', img_str)
    

def stream_video():
    for frame_data in generate_frames():
        socketio.emit('frame', frame_data)
        socketio.sleep(0.03)  # roughly 33 fps

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)