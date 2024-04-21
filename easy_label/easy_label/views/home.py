import os
from dotenv import load_dotenv

from django.shortcuts import render

def home(request):
    load_dotenv()
    hash = os.getenv('HASH')
    context = {
        "hash": hash
    }
    return render(request, 'home.html', context=context)