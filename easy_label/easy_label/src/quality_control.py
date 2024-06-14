import sys
import os
from pathlib import Path
import numpy as np
import json

from easy_label.src.addons import *



class QualityCheck:
    ''' Class for quality control
    
    Args:
        path (str): Path to a folder were all the data is stored
    '''
    
    ALLOWED_EXTENSIONS = {
        'png', 'jpg', 'jpeg', 'svg', 'webp'
    }
    
    def __init__(self, media_dir:str) -> None:
        self.images_path = os.path.normpath(os.path.join(media_dir, 'images'))
        # self.path_hashes = os.path.normpath('qualitycheck/data/hashes')
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
        BASE_DIR = Path(__file__).resolve().parent.parent
        with open(os.path.join(BASE_DIR, 'data', 'hashes.json')) as f:
            base_hashes = json.load(f)

        # base_hashes = []
        # txts = glob.glob(os.path.join(self.path_hashes, '*.txt'))
        # for txt_name in txts:
        #     with open(txt_name, 'r') as txt:
        #         hashes = txt.read().split('\n')
        #         for hash in hashes:
        #             base_hashes.append(hash)
        return base_hashes['hashes']

    
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
        BASE_DIR = Path(__file__).resolve().parent.parent
        with open(os.path.join(BASE_DIR, 'data', 'hashes.json')) as f:
            base_hashes = json.load(f)['hashes']
            print(base_hashes)
            base_hashes += hashes
        with open(os.path.join(BASE_DIR, 'data', 'hashes.json'), 'w') as f:
            print(base_hashes)
            json.dump({"hashes": base_hashes}, f, indent=4)