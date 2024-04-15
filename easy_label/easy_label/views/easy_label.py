import os

from django.shortcuts import render, redirect
from django.conf import settings

from easy_label.src import DataLoader


def easy_label(request, hash):
    data_loader = DataLoader(hash)
    data = data_loader.load_data()
    center = 'AMPARO GRANDE'
    modules = data['centers'][center]['modules']
    print(modules)
    context = {
        "data": data,
        "center": center,
        "modules": { 
            "value": modules,
            "iterator": range(1, modules+1)
        }
    }
    return render(request, 'easy-label.html', context=context)