from PIL import Image
import os

from PIL import Image
import os

def optimize_images(input_directory, output_directory, quality=90, max_size=1024):
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    for filename in os.listdir(input_directory):
        if filename.endswith(".jpg") or filename.endswith(".png"):
            image_path = os.path.join(input_directory, filename)
            img = Image.open(image_path)

            # resize image, maintaining aspect ratio
            max_dim = max(img.size)
            scale = max_size / max_dim
            new_size = (int(img.size[0]*scale), int(img.size[1]*scale))
            img.thumbnail(new_size)

            # save image with new quality setting
            new_filename = os.path.splitext(filename)[0] + ".png"
            new_path = os.path.join(output_directory, new_filename)
            img.save(new_path, "JPEG", quality=quality)

optimize_images("./large_images", "./static/images")

