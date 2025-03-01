#need to take the image fo the shirt and overlay the other image over it
from PIL import Image
import numpy as np
import os

def overlay(pattern_file):
    # Load the images
    shirt = Image.open("Resources\\Shirts\\1.png").convert("RGBA")
    overlay = Image.open(pattern_file).convert("RGBA")

    # Resize the overlay image to fit the shirt
    overlay = overlay.resize(shirt.size)

    # Convert images to numpy arrays
    shirt_array = np.array(shirt)
    overlay_array = np.array(overlay)

    # Extract alpha channel (transparency) from the shirt
    alpha_channel = shirt_array[:, :, 3]

    # Create a mask where the shirt is fully opaque (not transparent)
    mask = alpha_channel > 0

    # Replace only the green part (not transparent areas) with the flower pattern
    shirt_array[mask] = overlay_array[mask]

    # Convert back to an image
    result = Image.fromarray(shirt_array, "RGBA")
    
    imagecount = count_images("Resources//Shirts") + 1
    
    print(f"The image count is: {imagecount}")
    #creates a new file name and adds 1 to create  new file for t-shirt
    name = "T-Shirt_"
    png = ".png"
    imageFileName = f"{name}{imagecount}{png}"

    # Save and display the final output
    result.save(f"Resources//Shirts//{imageFileName}")
    result.show()


#check how many photos are in the folder
def count_images(folder_path):
    # Define common image file extensions
    image_extensions = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".webp"}
    
    # Count the number of image files in the folder
    image_count = sum(1 for file in os.listdir(folder_path) if os.path.splitext(file)[1].lower() in image_extensions)
    
    return image_count


overlay("C:\\Users\\tyrar\\OneDrive\\Desktop\\Hackathon2025\\flowers.jpg")
