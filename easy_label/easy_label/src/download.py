from django.http import JsonResponse, HttpResponse
from django.conf import settings

from PIL import Image
import zipfile
import json

import os
import io


def download(request):
    if request.method == 'POST':

        request_metadata = json.loads(request.body)['imageMetaData']
        image_metadata = request_metadata['json']
        print(image_metadata)
        media_dir = os.path.join(settings.MEDIA_ROOT, request_metadata['hash'])

        generate_json(media_dir, image_metadata)

        zip_buffer = generate_zip(media_dir)
        response = HttpResponse(zip_buffer, content_type='application/zip')
        response['Content-Disposition'] = 'attachment; filename="easylabel.zip"'
        return response

    else:
        return JsonResponse({'error': 'Only POST requests are allowed'})


def get_IDs(image_metadata):
    system_count = {'L': 0, 'P': 0, 'T': 0}
    for image in image_metadata.keys():
        if image_metadata[image]['obs'] == '':
            image_metadata[image]['obs'] = 'Sin observación del piloto'
        system = image_metadata[image]['system'][0].upper()
        image_metadata[image]['id'] = system + str(system_count[system])
        system_count[system] += 1
    return image_metadata

def clean_json(image_metadata):
    for image, metadata in image_metadata.items():
        if metadata['type'] == None:
            del image_metadata[image]
    return image_metadata

def generate_json(media_dir, image_metadata):
    # image_metadata = clean_json(image_metadata)
    image_metadata = get_IDs(image_metadata)
    json_file_path = os.path.join(media_dir, 'images.json')
    with open(json_file_path, 'w', encoding='utf-8') as json_file:
        json.dump(image_metadata, json_file, indent=4, ensure_ascii=False)


def generate_zip(media_dir):
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'a', zipfile.ZIP_DEFLATED, False) as zip_file:
        for root, dirs, files in os.walk(media_dir):
            for file in files:
                file_path = os.path.join(root, file)
                zip_file.write(file_path, os.path.relpath(file_path, media_dir))
    zip_buffer.seek(0)
    return zip_buffer

