from django.http import JsonResponse, HttpResponse
from django.conf import settings

from PIL import Image
import zipfile
import json

import os
import io


def download(request):
    pass