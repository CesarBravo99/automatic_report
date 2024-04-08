import os
from abc import ABC, abstractmethod

from src.include.template import Template
from src.include.bitacora import Bitacora
from src.include.loberas import Lobera
from src.include.peceras import Pecera
from src.include.tensores import Tensor
from src.utils.load_data import load_json

class Latex(ABC):
    ''' Base class for creating high-quality typesetting reports
    
    Args:
        data_dir (str): Path of the folder where is all the data
        hash (str): Hash associated to form request
        docker (bool): True if the form request is proccesed by the Docker
    '''

    @abstractmethod
    def __init__(self, data_dir:str, hash:str, docker:bool) -> None:
        self.data_dir = data_dir
        self.hash = hash
        self.docker = docker

    @abstractmethod
    def process(self) -> str:
        pass

    def compile(self, output_filename:str = 'report') -> None:
        self.__compile(output_filename)

    def __compile(self, output_filename:str) -> None:

        with open(self.data_dir + self.hash + '.tex', 'w', encoding='utf-8') as tex_file:
            tex_file.write(self.latex)
        
        if self.docker:
            os.system(f'/root/.TinyTeX/bin/x86_64-linux/pdflatex -output-directory {self.data_dir} -jobname={output_filename} {self.data_dir}{self.hash}.tex')
            os.system(f'/root/.TinyTeX/bin/x86_64-linux/pdflatex -output-directory {self.data_dir} -jobname={output_filename} {self.data_dir}{self.hash}.tex')
            output_name = os.path.join(os.path.join(os.path.normpath('./data/results/'), self.hash), output_filename)
        else:
            os.system(f'pdflatex -output-directory {self.data_dir} -jobname={output_filename} {self.data_dir}{self.hash}.tex')
            os.system(f'pdflatex -output-directory {self.data_dir} -jobname={output_filename} {self.data_dir}{self.hash}.tex')
            output_name = os.path.join(os.path.join(os.path.normpath('./auto_report/data/results/'), self.hash), output_filename)
        os.rename(f'{self.data_dir}{output_filename}.pdf', f'{output_name}.pdf')


class Report(Latex):
    ''' Class for creating high-quality typesetting reports for Tri-Chile
    
    Args:
        settings (dict): Dictionary which contains all the information provided by Tri-Chile
        images (dict): Dictironary which contains all the information provided by EasyLabel
        style (dict): Dictionary which contains all the style parameters provided by Tri-Chile
        data_dir (str): Path of the folder where is all the data
        hash (str): Hash associated to form request
        docker (bool): True if the form request is proccesed by the Docker
    '''

    def __init__(self, settings:dict, images:dict, style:dict, data_dir:str, hash:str, docker:bool) -> None:
        super().__init__(data_dir, hash, docker)
        self.settings = settings
        self.images = images
        self.style = style
        self.data_dir = data_dir
        self.style['front'] = os.path.join(self.data_dir, os.path.normpath('style/covers/back.jpeg'))
        self.style['back'] = os.path.join(self.data_dir, os.path.normpath('style/covers/front.jpg'))
        self.style['logo_client'] = os.path.join(self.data_dir, os.path.normpath('style/logos/client.png'))
        self.style['logo_cover'] = os.path.join(self.data_dir, os.path.normpath('style/logos/cover.png'))
        self.style['logo_user'] = os.path.join(self.data_dir, os.path.normpath('style/logos/user.png'))
        self.style['errorType'] = {
            'correct': f"circle, draw={self.style['ocg']['color']['correct']}, minimum size=0.05cm, label=center: \{self.style['ocg']['label']['correct']}, ",
            'tear': f"circle, draw={self.style['ocg']['color']['tear']}, minimum size=0.05cm, label=center: \{self.style['ocg']['label']['tear']}, ",
            'anomaly': f"circle, draw={self.style['ocg']['color']['anomaly']}, minimum size=0.05cm, label=center: \{self.style['ocg']['label']['anomaly']}, ",
            'adherence': f"circle, draw={self.style['ocg']['color']['adherence']}, minimum size=0.05cm, label=center: \{self.style['ocg']['label']['adherence']}, ",
            'mortality': f"circle, draw={self.style['ocg']['color']['mortality']}, minimum size=0.05cm, label=center: \{self.style['ocg']['label']['mortality']}, ",
            'lack_tension': f"circle, draw={self.style['ocg']['color']['lack_tension']}, minimum size=0.05cm, label=center: \{self.style['ocg']['label']['lack_tension']}, ",
            'no_tension': f"circle, draw={self.style['ocg']['color']['no_tension']}, minimum size=0.05cm, label=center: \{self.style['ocg']['label']['no_tension']}, "
            }
        centers, _ = load_json(os.path.normpath('auto_report/src/add_ons/trichile/'), 'centers.json')
        self.center = centers[settings['centro']]
        self.params, _ = load_json(os.path.normpath('auto_report/src/add_ons/trichile/'), 'params.json')
        print("All data is loaded!")


    def process(self) -> str:

        template = Template(self.settings, self.params, self.style)
        bitacora = Bitacora(self.settings, self.images, self.style)

        for img in self.images.values():
            if img['system'] == 'lobero':
                lobera = Lobera(self.settings, self.images, self.params, self.center, self.style, self.data_dir)
                flagLobera = True
            elif img['system'] == 'pecero':
                pecera = Pecera(self.settings, self.images, self.params, self.center, self.style, self.data_dir)
                flagPecera = True
            elif img['system'] == 'tensor':
                tensor = Tensor(self.settings, self.images, self.params, self.center, self.style, self.data_dir)
                flagTensoresLobera = True

        if self.settings['complete']:
            self.latex = template.init_template()
            self.latex += template.front_page()
            self.latex += bitacora.process()
            self.latex += lobera.process() if flagLobera else ''
            self.latex += pecera.process() if flagPecera else ''
            self.latex += tensor.process() if flagTensoresLobera else ''
            self.latex += template.back_page()
            self.latex += r'\end{document}'
            self.compile(f"{self.settings['fecha'].replace('-', '_')}_{self.settings['rut'].replace('-','')}_report")

        else:
            self.latex = template.init_template()
            self.latex += template.front_page()
            self.latex += bitacora.process()
            self.latex += template.back_page()
            self.latex += r'\end{document}'
            self.compile(f"{self.settings['fecha'].replace('-', '_')}_{self.settings['rut'].replace('-','')}_bitacora")

            if flagLobera:
                self.latex = template.init_template()
                self.latex += template.front_page()
                self.latex += lobera.process()
                self.latex += template.back_page()
                self.latex += r'\end{document}'
                self.compile(f"{self.settings['fecha'].replace('-', '_')}_{self.settings['rut'].replace('-','')}_lobera")
            
            if flagPecera:
                self.latex = template.init_template()
                self.latex += template.front_page()
                self.latex += pecera.process()
                self.latex += template.back_page()
                self.latex += r'\end{document}'
                self.compile(f"{self.settings['fecha'].replace('-', '_')}_{self.settings['rut'].replace('-','')}_pecera")

            if flagTensoresLobera:
                self.latex = template.init_template()
                self.latex += template.front_page()
                self.latex += tensor.process()
                self.latex += template.back_page()
                self.latex += r'\end{document}'
                self.compile(f"{self.settings['fecha'].replace('-', '_')}_{self.settings['rut'].replace('-','')}_tensores")

