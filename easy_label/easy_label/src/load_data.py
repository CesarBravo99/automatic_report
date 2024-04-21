import os
import json

from django.shortcuts import redirect
from django.conf import settings


class DataLoader():
    
    def __init__(self, hash):
        self.hash = hash
        self.media_dir = os.path.join(settings.MEDIA_ROOT, str(hash), 'imgs')
        self.centers_path = os.path.join(settings.BASE_DIR, 'easy_label', 'data', 'centers.json')
        self.weights_path = os.path.join(settings.BASE_DIR, 'easy_label', 'data', 'weights.json')
        self.imgs_name = ''

        with open(self.centers_path, 'r', encoding='latin-1') as f:
            centers = json.load(f)
        self.centers = centers
    
        with open(self.weights_path, 'r', encoding='latin-1') as f:
            weights = json.load(f)
        self.weights = weights

        # [' '.join(list(map(str.capitalize, center.split(' ')))) for center in self.centers.keys()]
        self.centers_name = sorted(list(self.centers.keys()))

    def sanity_check(self):
        if not os.path.exists(self.media_dir): 
            return redirect('/')
        else:
            self.imgs_name = os.listdir(self.media_dir)

    def load_data(self):
        self.sanity_check()
        return self.imgs_name, self.centers, self.centers_name, self.weights