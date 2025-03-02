from PIL import Image, ImageOps

# Open the image
im = Image.open("4.png")
bbox = im.getbbox()  # Returns (left, upper, right, lower)
cropped_im = im.crop(bbox)

# Resize the image to desired dimensions
desired_size = (440, 813)
padded_im = ImageOps.pad(cropped_im, desired_size, method=Image.LANCZOS, color=(0, 0, 0, 0))

# Save the output
padded_im.save("4.png")