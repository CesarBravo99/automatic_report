import os
from dotenv import load_dotenv

from django.shortcuts import render

def tutorial(request):
    load_dotenv()
    hash = os.getenv('HASH')
    context = {
        "hash": hash
    }
    return render(request, 'tutorial.html', context=context)