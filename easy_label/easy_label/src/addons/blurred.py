from PIL import Image
import numpy as np
import cv2

import os

def check_blurred_img(imgs):
    '''Check if the uploaded images are blurred using the Laplacian method.

    Args:
        imgs (list): list of image paths 
    '''
    for img_path in imgs:
        img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
        if img is None:
            print(f"Cannot read image: {img_path}")
            continue
        laplacian_var = cv2.Laplacian(img, cv2.CV_64F).var()
        if laplacian_var < float(130):
            return f'Al menos una de las fotos está muy borrosa.', False
    return '', True