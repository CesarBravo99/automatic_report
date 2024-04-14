import os
import random

from django.shortcuts import redirect

ALLOWED_EXTENSIONS = {
    'png', 'jpg', 'jpeg', 'svg', 'webp'
}

def upload_images(reques):
    return redirect('home')