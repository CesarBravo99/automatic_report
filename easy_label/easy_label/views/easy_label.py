# ./easy_label/DarkDjango/EasyLabel/custom_views/easy_label.py

from django.shortcuts import render, redirect
from django.conf import settings
from django.http import Http404

import json # Delete this line
import sys
import os


def load_centers():
    centers_json = load_centers_json()
    centers_names = get_centers_names(centers_json)
    centers_data = get_centers_data(centers_json)
    return centers_names, centers_data
    
def load_centers_json():
    path = os.path.join(
        settings.BASE_DIR, os.path.normpath('easy_label/data/centers.json')
    )
    with open(path, 'r', encoding='latin-1') as f:
        centers = json.load(f)
    return centers

def get_centers_names(centers_json: dict):
    names = list(centers_json.keys())
    sorted_names = sorted(names)
    return sorted_names

def get_centers_data(centers_json: dict):
    centers_data = {}
    for center_name, center_data in centers_json.items():
        filename = center_name.replace(' ', '')
        centers_data[center_name] = {**center_data, 'filename': filename}
    return json.dumps(centers_data)


def easy_label(request, images_dir):
    media_path = os.path.join(settings.MEDIA_ROOT, str(images_dir))
    if not os.path.exists(media_path) and images_dir.isdigit():
        return redirect('/')
    image_files = os.listdir(os.path.join(media_path, 'images'))
    centers_names, centers_data = load_centers()
    peceras_options = [f'Pecera {i}' for i in range(101, 110)]
    context = dict(
        media_url=settings.MEDIA_URL,
        images_dir=images_dir,
        media_path=media_path,
        image_files=image_files,
        centers_names=centers_names,
        centers_data=centers_data,
        peceras_options=peceras_options
    )
    print( f"{media_path}/{image_files[0]}")
    return render(request, 'easy-label.html', context=context)