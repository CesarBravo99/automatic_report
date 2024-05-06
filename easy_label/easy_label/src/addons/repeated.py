import sys
import os
from .image_hash import HashManager

def check_repeated_img(imgs:list, base_hashes:list):
    '''Check if the uploaded images are repeated

    Args:
        imgs (list): list of image paths 
        base_hashes (list): list of previous image hashes uploaded to EasyLabel
    '''
    hash_manager = HashManager(imgs)
    hashes = hash_manager.generate_hashes()
    if len(hashes) != len(set(hashes)):
        return 'Hay imágenes subidas repetidas', False , hashes
    for i in range(len(hashes)):
        for hash2 in base_hashes:
            if hash_manager.hash_distance(hashes[i], hash2) < 0.1:
                return f'La imagen {os.path.basename(imgs[i])} está repetida', False, hashes
    else:
        return '', True, hashes

    