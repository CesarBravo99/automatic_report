from django.http import JsonResponse, HttpResponse
from django.conf import settings

from PIL import Image
import zipfile
import json

import os
import io


def download(request):
    if request.method == 'POST':
        # response = HttpResponse('aaaaaaa')
        


        image_metadata = json.loads(request.body)
        media_dir = os.path.join(settings.MEDIA_ROOT, image_metadata['hash'])
        generate_json(media_dir, image_metadata['json'])

        response = HttpResponse("<html><body>It is now.</body></html>")
        return response

        zip_buffer = generate_zip(media_dir)
        response = HttpResponse(zip_buffer, content_type='application/zip')
        response['Content-Disposition'] = 'attachment; filename="easylabel.zip"'
        return response

    else:
        return JsonResponse({'error': 'Only POST requests are allowed'})

def generate_json(media_dir, image_metadata):
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

