#need to take the image fo the shirt and overlay the other image over it
from PIL import Image
import numpy as np

def overlay(pattern_file):
    # Load the images
    shirt = Image.open("Resources\\Shirts\\1.png").convert("RGBA")
    # overlay = Image.open("C:\\Users\\tyrar\\OneDrive\\Desktop\\Hackathon2025\\flowers.jpg").convert("RGBA")

    # Resize the overlay image to fit the shirt
    overlay = pattern_file.resize(shirt.size)

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

    # Save and display the final output
    result.save("C:\\Users\\tyrar\\OneDrive\\Desktop\\Hackathon2025\\shirt_with_stretched_overlay.png")
    result.show()