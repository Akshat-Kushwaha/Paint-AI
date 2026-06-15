import cv2
import numpy as np
from models.image_api import generate_image

def get_image_rgb(prompt):
    image_bytes = generate_image(
        prompt=prompt,
        output_path=None
    )

    if image_bytes:
        # Convert bytes → NumPy array
        np_img = np.frombuffer(image_bytes, np.uint8)

        # Decode image
        img = cv2.imdecode(np_img, cv2.IMREAD_COLOR)
        if img is not None:
            return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        else:
            print("❌ Failed to decode image")
            return None
    else:
        return None
