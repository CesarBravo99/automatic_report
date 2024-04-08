import json
from argparse import ArgumentParser
from src.report import Report
from src.utils.load_data import load_json


def generate(data_dir:str, hash:str, docker:bool) -> None:
    ''' Load all the data and generate the report/s
    
    Args:
        data_dir (str): Path of the folder where is all the data
        hash (str): Hash associated to form request
        docker (bool): True if the form request is proccesed by the Docker
    '''

    settings, load_settings = load_json(data_dir, 'settings.json')
    images, load_images = load_json(data_dir, 'images.json')
    style, load_style = load_json(data_dir, 'style.json')

    if load_settings and load_images and load_style:
        report = Report(settings, images, style, data_dir, hash, docker)
        report.process()


if __name__=='__main__':

    parser = ArgumentParser()
    parser.add_argument("--data_dir", type=str, help="Data folder path, ex: a/b/c/")
    parser.add_argument("--hash", type=str, help="Name of hashed json")
    parser.add_argument("--docker", type=str)
    args = parser.parse_args()

    data_dir = args.data_dir
    hash = args.hash
    docker = args.docker
    generate(data_dir, hash, json.loads(docker))