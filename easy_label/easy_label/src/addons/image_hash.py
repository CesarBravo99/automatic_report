import os
import numpy as np
import scipy as sp
import cv2
import glob


class HashManager:
    '''Base class for create and compare image hashes

    Args:
        imgs (list): list of image paths 
    '''

    def __init__(self, imgs:list) -> None:
        self.imgs = imgs


    def generate_hashes(self) -> list:
        hashes = []
        for img in self.imgs:
            hashes.append(self.image_hashing(img))
        return hashes
    
    
    def image_hashing(self, img_path:str) -> str:
        img = cv2.imread(img_path)
        img = cv2.resize(img, (64, 64))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img = np.array(img, dtype = np.float64)
        dct = cv2.dct(img)
        dct_block = dct[:16, :16]
        dct_average = (dct_block.mean() * dct_block.size - dct_block[0, 0]) / (dct_block.size - 1)
        dct_block[dct_block < dct_average] = 0.0
        dct_block[dct_block != 0] = 1.0
        return self.hash_array_to_hash_hex(dct_block.flatten())


    def hash_array_to_hash_hex(self, hash_array:list) -> str:
        hash_array = np.array(hash_array, dtype = np.uint8)
        hash_str = ''.join(str(i) for i in 1 * hash_array.flatten())
        return (hex(int(hash_str, 2)))


    def hash_distance(self, hash1:str, hash2:str) -> float:
        distance = sp.spatial.distance.hamming(
            self.hash_hex_to_hash_array(hash1), 
            self.hash_hex_to_hash_array(hash2)
        )
        return distance


    def hash_hex_to_hash_array(self, hash_hex:str) -> list:
        hash_str = int(hash_hex, 16)
        array_str = bin(hash_str)[2:]
        return np.array([i for i in array_str], dtype = np.float32)