import os
import json
from dotenv import load_dotenv

from django.shortcuts import render, redirect
from django.conf import settings

from easy_label.src import DataLoader


def easy_label(request, hash):
    data_loader = DataLoader(hash)
    data = data_loader.load_data()
    center = 'CARMEN'
    module = "0"
    modules = data['centers'][center]['modules']
    filename = data['centers'][center]['filename']
    jaulas = data['centers'][center]['jails'][module]
    scope = str(data['centers'][center]['scopes'][module])
    x_flip = int(data['centers'][center]['x_flip'][module])
    y_flip = int(data['centers'][center]['y_flip'][module])
    double = int(data['centers'][center]['double'][module])
    
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
    context = {
        "hash": hash,
        "imgs": data['imgs'],
        "data": data,
        "centers": json.dumps(data['centers']),
        "center": center,
        "modules": range(1, modules+1),
        "filename": filename,
        "templates": templates,
        "mamparo_labels": mamparo_labels,
        "pecera_labels": pecera_labels,
        "x_flip": x_flip,
        "y_flip": y_flip,
        "double": double,
    }
    return render(request, 'easy-label.html', context=context)