from PIL import Image

img = Image.open("src/useful_utilities_collection/assets/icon.png").convert("RGBA")
sizes = [(16, 16), (24, 24), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
img.save("src/useful_utilities_collection/assets/icon.ico", format="ICO", sizes=sizes)