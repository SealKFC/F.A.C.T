from PIL import Image

from TshirtOverlay import overlay

def pattern(filename, tile_x, tile_y):

    # Load the user's image
    image = Image.open(filename).convert("RGBA")

    # Define the new size (increase size by repeating pattern)
    # tile_x = 3  # Number of times to repeat horizontally
    # tile_y = 3  # Number of times to repeat vertically

    tile_x = int(tile_x)
    tile_y = int(tile_y)

    # Create a new blank image with the scaled size
    new_width = image.width * tile_x
    new_height = image.height * tile_y
    new_image = Image.new("RGB", (new_width, new_height))

    # Tile the original image
    for i in range(tile_x):
        for j in range(tile_y):
            new_image.paste(image, (i * image.width, j * image.height))

    tshirt = overlay(new_image)

    return tshirt

    # Show and save the new image
    # new_image.show()
    # new_image.save("C:\\Users\\tyrar\\OneDrive\\Desktop\\Hackathon2025\\tiled_image.jpg")
