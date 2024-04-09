# ./easy_label/DarkDjango/EasyLabel/custom_views/upload_images.py

from django.shortcuts import redirect
from django.http import JsonResponse
from django.contrib import messages
from django.conf import settings

import random
import shutil
import os

# from quality_check import QualityCheck

ALLOWED_EXTENSIONS = {
    'png', 'jpg', 'jpeg', 'svg', 'webp'
}


def upload_images(request):
    if request.method == 'POST':
        files = request.FILES.getlist('images')
        images, message = check_if_images(files)
        if not images:
            messages.error(
                request,
                message=message
            )
            return redirect('home')
        random_dir = str(random.randint(100000, 999999))
        while check_if_random_dir_exists(random_dir):
            random_dir = str(random.randint(100000, 999999))
        save_path = os.path.join(settings.MEDIA_ROOT, random_dir)
        os.makedirs(save_path, exist_ok=True)
        os.makedirs(os.path.join(save_path, 'images'), exist_ok=True)
        for i, img in enumerate(images):
            img_name, img_ext = os.path.splitext(img.name)
            img_path = os.path.join(save_path, 'images', f'{i}{img_ext}')
            with open(img_path, 'wb+') as f:
                for chunk in img.chunks():
                    f.write(chunk)
        status, message = run_quality_check(save_path)
        if not status:
            shutil.rmtree(save_path)
            messages.error(
                request,
                message=message
            )
            return redirect('home')
        else:
            request.session['folder_to_delete'] = save_path
            return redirect(f'/{random_dir}')


def check_if_images(files):
    for file in files:
        ext = os.path.splitext(file.name)[1].lower()[1:]
        if ext not in ALLOWED_EXTENSIONS:
            message = f'''
                Formato de imagen no soportado.
                <hr>
                Formatos soportados:
                <br>
                <ul>
            '''
            for ext in ALLOWED_EXTENSIONS:
                message += f'<li>{ext}</li>'
            message += '</ul>'
            return False, message
    return files, None


def check_if_random_dir_exists(random_dir):
    dir_path = os.path.join(settings.MEDIA_ROOT, random_dir)
    return os.path.exists(dir_path)

def run_quality_check(path):
    qc = QualityCheck(path=path, add_images_path=False)
    response= qc.quality_control()
    print('Quality check response:', response)
    status = response['status']
    message = response['msg']
    return status, message