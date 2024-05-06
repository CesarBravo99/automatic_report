import sys
import os
import numpy as np
import glob 

from easy_label.src.addons import *


class QualityCheck:
    ''' Class for quality control
    
    Args:
        path (str): Path to a folder were all the data is stored
        add_images_path (bool): True if all the data is stored in images
    '''
    
    ALLOWED_EXTENSIONS = {
        'png', 'jpg', 'jpeg', 'svg', 'webp'
    }
    
    def __init__(self, path:str, add_images_path:bool=False) -> None:
        self.path = os.path.normpath(os.path.join(path, 'images') if add_images_path else path)
        self.images_path = os.path.normpath(os.path.join(path, 'images'))
        self.path_hashes = os.path.normpath('qualitycheck/data/hashes')
        self.imgs = self.load_images()
        self.base_hashes = self.load_hashes()


    def load_images(self) -> list:
        imgs = list()
        for filepath in os.listdir(self.images_path):
            ext = os.path.splitext(filepath)[1].lower()[1:]
            if ext in self.ALLOWED_EXTENSIONS:
                imgs.append(os.path.join(self.images_path, filepath))
        return imgs


    def load_hashes(self) -> list:
        base_hashes = []
        txts = glob.glob(os.path.join(self.path_hashes, '*.txt'))
        for txt_name in txts:
            with open(txt_name, 'r') as txt:
                hashes = txt.read().split('\n')
                for hash in hashes:
                    base_hashes.append(hash)
        return base_hashes

    
    def quality_control(self) -> dict:
        msg_blurred, blurred = check_blurred_img(self.imgs)
        msg_repeated, repeated, hashes = check_repeated_img(self.imgs, self.base_hashes)
        msg_ctx, ctx = check_context(self.imgs)
        msg_labels, labels = check_img_labels(self.imgs)
        
        response = {}
        if msg_blurred and msg_repeated:
            msg_blurred += '<hr>'
        response['msg'] = msg_blurred + msg_repeated + msg_ctx + msg_labels
        response['status'] = bool(np.all([blurred, repeated, labels, ctx]))
        if response['status']:
            self.save(hashes)
        return response
    
    def save(self, hashes:list) -> None :
        txt_name = os.path.join(self.path, 'hashes.txt')
        with open(txt_name, 'w') as txt:
            for hash in hashes:
                txt.write(f'{hash}\n')