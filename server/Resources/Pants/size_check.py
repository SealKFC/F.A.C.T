import cv2

image = cv2.imread("1.png")

if image is None:
    print("Error: Image not found or could not be loaded.")
else:
    # image.shape returns (height, width, channels) if color, or (height, width) if grayscale.
    print("Image size (height, width, channels):", image.shape)

