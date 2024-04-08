import os
from argparse import ArgumentParser
from src.report import Report
from src.utils.load_data import load_json


def generate(root:str, imported_data_dir:str, exported_data_dir:str, pdf_config:str, hash:str) -> None:
    ''' Load all the data and generate the report/s
    
    Args:
        root (str): Root path where the script es located
        imported_data_dir (str): Path of the folder where is all the data
        exported_data_dir (str): Path of the folder where is located the final PDF
        pdf_config (str): type of report, the options are
            - a: get all the report in 1 pdf: bitacora, lobera, pecera, tensores included
            - s: get all the report in different pdf's: bitacora, lobera, pecera, tensores included
            - b: get the bitacora pdf
            - l: get the lobera pdf
            - p: get the pecera pdf
            - t: get the tensores pdf
            - It is possible to combine all configurations in the sense that: blpt = s
        hash (str): Hash associated to form request
    '''

    base_data_dir = os.path.join(root, os.path.normpath('src/resources/data/'))
    settings, load_settings = load_json(imported_data_dir, 'settings.json')
    images, load_images = load_json(imported_data_dir, 'images.json')
    centers, load_centers = load_json(base_data_dir, 'centers.json')
    params, load_params = load_json(base_data_dir, 'params.json')
    style, load_style = load_json(base_data_dir, 'style.json')

    center = centers[settings['centro'].upper()]
    style['front'] = os.path.join(base_data_dir, os.path.normpath('images/covers/back.jpeg'))
    style['back'] = os.path.join(base_data_dir, os.path.normpath('images/covers/front.jpg'))
    style['trichile_logo'] = os.path.join(base_data_dir, os.path.normpath('images/logos/trichile.png'))
    style['trichile_cover'] = os.path.join(base_data_dir, os.path.normpath('images/logos/trichile_cover.png'))
    style['client_cover'] = os.path.join(base_data_dir, os.path.normpath(f'images/logos/{settings["cliente"].lower()}.png'))
    style['errorType'] = {
        'correct': f"circle, draw={style['ocg']['color']['correct']}, minimum size=0.05cm, label=center: \{style['ocg']['label']['correct']}, ",
        'tear': f"circle, draw={style['ocg']['color']['tear']}, minimum size=0.05cm, label=center: \{style['ocg']['label']['tear']}, ",
        'anomaly': f"circle, draw={style['ocg']['color']['anomaly']}, minimum size=0.05cm, label=center: \{style['ocg']['label']['anomaly']}, ",
        'adherence': f"circle, draw={style['ocg']['color']['adherence']}, minimum size=0.05cm, label=center: \{style['ocg']['label']['adherence']}, ",
        'mortality': f"circle, draw={style['ocg']['color']['mortality']}, minimum size=0.05cm, label=center: \{style['ocg']['label']['mortality']}, ",
        'lack_tension': f"circle, draw={style['ocg']['color']['lack_tension']}, minimum size=0.05cm, label=center: \{style['ocg']['label']['lack_tension']}, ",
        'no_tension': f"circle, draw={style['ocg']['color']['no_tension']}, minimum size=0.05cm, label=center: \{style['ocg']['label']['no_tension']}, "
    }

    if load_settings and load_images and load_centers and load_params and load_style:
        print('All data is loaded!')
        report = Report(settings, images, center, params, style, imported_data_dir, exported_data_dir, pdf_config, hash)
        print('Generating PDF...')
        report.process()


if __name__=='__main__':

    parser = ArgumentParser()
    parser.add_argument("--root", type=str, help="Root path")
    parser.add_argument("--imported_data_dir", type=str, help="Data folder path")
    parser.add_argument("--exported_data_dir", type=str, help="PDF folder path")
    parser.add_argument("--pdf_config", type=str, help="PDF configuration")
    parser.add_argument("--hash", type=str, help="ID Hash")
    args = parser.parse_args()

    root = args.root
    imported_data_dir = args.imported_data_dir
    exported_data_dir = args.exported_data_dir
    pdf_config = args.pdf_config
    hash = args.hash
    generate(root, imported_data_dir, exported_data_dir, pdf_config, hash)