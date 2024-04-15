import os
import time
import random
import hashlib

from django.shortcuts import redirect
from django.contrib import messages
from django.conf import settings

ALLOWED_EXTENSIONS = [
    '.png', '.jpg', '.jpeg', '.svg', '.webp'
]

def check_extensions(request, files):
    ''' Check if the files extensions are allowed

    Args:
        request: POST request made by the user
        files: List of all the files with an upload reques
    '''

    for file in files:
        ext = os.path.splitext(file.name)[1].lower()
        if ext not in ALLOWED_EXTENSIONS:
            message = f'''
                Formato de arhivo no soportado.
                <hr>
                Formatos soportados:
                <br>
                <ul>
            '''
            for ext in ALLOWED_EXTENSIONS:
                message += f'<li>{ext}</li>'
            message += '</ul>'
            messages.error(
                request,
                message=message
            )
            return None
    return files


def save_media(images):
    ''' Create a random directory and save the uploaded files

    Args:
        images: Images uploaded by the user
    '''

    hash_temp = hashlib.shake_256(str(time.time() + random.random()).encode('UTF-8')).hexdigest(25)
    media_dir = os.path.join(settings.MEDIA_ROOT, hash_temp)
    os.makedirs(media_dir, exist_ok=True)
    os.makedirs(os.path.join(media_dir, 'imgs'), exist_ok=True)

    for i, img in enumerate(images):
        img_name, img_ext = os.path.splitext(img.name)
        img_path = os.path.join(media_dir, 'imgs', f'{i}{img_ext}')
        with open(img_path, 'wb+') as f:
            for chunk in img.chunks():
                f.write(chunk)
    return media_dir, hash_temp


def upload_images(request):
    ''' Take the upload post request and proccess it
    
    Args:
        request: POST request made by the user
    '''

    if request.method == 'POST':
        files = request.FILES.getlist('images')
        images = check_extensions(request, files)
        if not images:
            return redirect('home')
        media_dir, hash_temp = save_media(images)
        # status, message = run_quality_check(media_dir)
        request.session['folder_to_delete'] = media_dir
        return redirect(f'/{hash_temp}')
        
    return redirect('tutorial')