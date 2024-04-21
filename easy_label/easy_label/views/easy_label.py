import os
import json
from dotenv import load_dotenv

from django.shortcuts import render, redirect
from django.conf import settings

from easy_label.src import DataLoader


def easy_label(request, hash):
    data_loader = DataLoader(hash)
    imgs_name, centers, centers_name, weights = data_loader.load_data()
    center = 'AMPARO GRANDE'
    module = "0"
    modules = centers[center]['modules']
    filename = centers[center]['filename']
    jaulas = centers[center]['jails'][module]
    scope = str(centers[center]['scopes'][module])
    x_flip = int(centers[center]['x_flip'][module])
    y_flip = int(centers[center]['y_flip'][module])
    double = int(centers[center]['double'][module])
    
    templates = {
        "lobera_fondo": os.path.join(os.path.normpath('imgs/assets/background/'), f'{filename}_{module}.png'),
        "lobera_lateral": os.path.join(os.path.normpath('imgs/assets/lateral/'), f'{filename}_{module}.png'),
        "lobera_cabecera": os.path.join(os.path.normpath('imgs/assets/fixed/'), f'seawolf_head_{x_flip}{y_flip}{double}.png'),
        "tensor": os.path.join(os.path.normpath('imgs/assets/tensor/'), f'{filename}_{module}.png')
    }

    mamparo_labels = ["L" + str(i+1) + " - " + "L" + str(i+2) if x_flip else "L" + str(i+2) + " - " + "L" + str(i+1) for i in range(0, jaulas-2, 2)]
    if y_flip: mamparo_labels = list(reversed(mamparo_labels))
    pecera_labels = [str(scope)[0] + "0" + str(i+1) if i < 9 else str(scope)[0] + str(i+1) for i in range(jaulas)]

    load_dotenv()
    os.environ["HASH"] = hash

    init_easylabel = {
        "center": center,
        "centers_name": centers_name,
        "templates": templates,
        "modules": range(1, modules+1),
        "mamparo_labels": mamparo_labels,
        "pecera_labels": pecera_labels,
    }
    context = {
        "hash": hash,
        "imgs_name": imgs_name,
        "centers": json.dumps(centers),
        "weights": json.dumps(weights),
        "init_easylabel": init_easylabel,
    }
    return render(request, 'easylabel.html', context=context)