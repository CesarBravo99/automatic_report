# ./easy_label/DarkDjango/EasyLabel/custom_views/download.py

from django.http import JsonResponse, HttpResponse
from django.conf import settings

from PIL import Image
import zipfile
import json

import os
import io

def download(request):
    if request.method == 'POST':
        received_data = json.loads(request.body)
        status, message = is_data_complete(received_data)
        if not status:
            return JsonResponse({'error': message})
        print(received_data)
        formatted_data = clean_data(received_data)
        media_dir = os.path.join(settings.MEDIA_ROOT, received_data['images_dir'])
        json_file_path = os.path.join(media_dir, 'images.json')
        with open(json_file_path, 'w', encoding='utf-8') as json_file:
            json.dump(formatted_data, json_file, indent=4, ensure_ascii=False)
        print(json.dumps(formatted_data, indent=4, ensure_ascii=False))
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, 'a', zipfile.ZIP_DEFLATED, False) as zip_file:
            for root, dirs, files in os.walk(media_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    zip_file.write(file_path, os.path.relpath(file_path, media_dir))
        zip_buffer.seek(0)
        response = HttpResponse(zip_buffer, content_type='application/zip')
        response['Content-Disposition'] = 'attachment; filename="easylabel.zip"'
        return response
        # return JsonResponse(formatted_data)
    else:
        return JsonResponse({'error': 'Only POST requests are allowed'})
    
def is_data_complete(data):
    images = os.listdir(
        os.path.join(settings.MEDIA_ROOT, data['images_dir'], 'images')
    )
    if not all_images_exist(images, data['iconData'].keys()):
        status = False
        message = 'Some images are missing.'
        return status, message
    for image_name, icon_data in data['iconData'].items():
        status, message = is_image_complete(icon_data)
        if not status:
            return status, f"Image '{image_name}': {message}"
    status = True
    message = 'The data is complete.'
    return status, message

def is_image_complete(image_data):
    required_keys = ['x', 'y']
    for key in required_keys:
        if key not in image_data:
            return False, f"Missing '{key}' in image data"
    return True, 'The image is complete.'

def all_images_exist(images, icons):
    for image in images:
        if image not in icons:
            return False
    return True
    
        
def clean_data(data):
    system_replace = {
        'Lobera': 'lobero',
        'Tensores': 'tensor',
        'Peceras': 'pecero',
    }
    type_replace = {
        'Correcto': 'correct',
        'Rotura/Falla': 'tear',
        'Anomalía': 'anomaly',
        'Adherencia': 'adherence',
        'Mortalidad': 'mortality',
        'Falta Tensión': 'lack_tension',
        'Sin Tensión': 'no_tension',
    }
    with open(os.path.join(settings.STATICFILES_DIRS[0], 'easy-label', 'centers', 'weights.json'), 'r') as json_file:
        weights = json.load(json_file)
    image_comments = dict()
    for filename in data['imageComments'].keys():
        image_comments[os.path.split(filename)[-1]] = data['imageComments'][filename]['comment']
    clean = dict()
    system_count = {'pecero': 0, 'tensor': 0, 'lobero': 0}
    for filename in data['imageData'].keys():
        img = data['imageData'][filename]['icon']
        clean[filename] = dict()
        clean[filename]['module'] = img['module']
        clean[filename]['system'] = system_replace[img['activeTab']]
        system = clean[filename]['system']
        if system == 'pecero':
            clean[filename]['jail'] = img['peceras']
        if system == 'lobero':
            if 'seawolf_sep' in img['imageName']:
                separator = img['mamparos'].split(' - ')
            else:
                separator = 'None'
            clean[filename]['separator'] = separator
        img_type = img['type'].split('\n')[1]
        clean[filename]['type'] = type_replace.get(img_type, 'unknown')
        x, y = get_real_coordinates(
            px=img['px'],
            py=img['py'],
            filename=img['imageName'],
            img_class=img['imageClass']
        )
        x, y = transform_x_y(
            x=x,
            y=y,
            system=system,
            img_class=img['imageClass'],
            json_file=weights
        )
        clean[filename]['x'] = x
        clean[filename]['y'] = y
        if filename in image_comments:
            clean[filename]['obs'] = image_comments[filename]
        else:
            clean[filename]['obs'] = 'Sin observación del piloto'
        clean[filename]['id'] = system[0].upper()+str(system_count[system])
        system_count[system] += 1
    return clean

def get_real_coordinates(px: float, py: float, filename: str, img_class: str):
    folder_replace = {
        'img-loberas-fondo': 'background',
        'img-loberas-lateral': 'lateral',
        'img-tensores': 'tensor',
    }
    folder = folder_replace.get(img_class, 'fixed')
    img = Image.open(
        os.path.join(
            settings.STATICFILES_DIRS[0],
            'easy-label',
            'centers',
            folder,
            filename
        )
    )
    return px*img.size[0], py*img.size[1]

def transform_x_y(x, y, system: str, img_class: str, json_file=None):
    if json_file is None:
        path = os.path.join(
            settings.STATICFILES_DIRS[0], 'easy-label', 'centers', 'weights.json'
        )
        with open(path, 'r') as json_file:
            weights = json.load(json_file)
    else:
        weights = json_file
    if system == 'lobero':
        system = 'seawolf'
    elif system == 'pecero':
        system = 'fishbowl'
    else:
        system = 'tensors'
    image_class_replace = {
        'fondo': 'background',
        'cabeceras': 'head',
        'mamparos': 'separator',
        'lateral': 'lateral',
        'tensores': 'system',
        '1': 'frontal',
        '2': 'canal',
        '3': 'distal',
        '4': 'costa',
        'topview': 'background',
    }
    img_class = image_class_replace[img_class.split('-')[-1]]
    new_x = x*weights[system][img_class]['x'][1]+weights[system][img_class]['x'][0]
    new_y = y*weights[system][img_class]['y'][1]+weights[system][img_class]['y'][0]
    return new_x, new_y