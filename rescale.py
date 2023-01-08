from PIL import Image

# Opens a image in RGB mode

import os

for i in range(-6, 7):
    if i == 0:
        continue
    # os.remove(f"pieces/{i}test.png")
    im = Image.open(f"pieces/{i}.png")
    im = im.resize((128, 128))
    im.save(f"pieces/{i}.png")
# im = Image.open(r"boards/test.png")
 
# # Size of the image in pixels (size of original image)
# # (This is not mandatory)
# width, height = im.size
 
# # Setting the points for cropped image
# left = 4
# top = height / 5
# right = 154
# bottom = 3 * height / 5
 
# # Cropped image of above dimension
# # (It will not change original image)
# im1 = im.crop((left, top, right, bottom))
# newsize = (300, 300)
# im1 = im1.resize(newsize)
# # Shows the image in image viewer
# im1.show()