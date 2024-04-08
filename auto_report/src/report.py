import os
from abc import ABC, abstractmethod

from src.resources.template import Template
from src.resources.include.bitacora import Bitacora
from src.resources.include.loberas import Lobera
from src.resources.include.peceras import Pecera
from src.resources.include.tensores import TensorLobera

class Latex(ABC):
    ''' Base class for creating high-quality typesetting reports
    
    Args:
        imported_data_dir (str): Path of the folder where is all the data
        exported_data_dir (str): Path of the folder where is located the final PDF
        hash (str): Hash associated to form request
    '''

    @abstractmethod
    def __init__(self, imported_data_dir:str, exported_data_dir:str, hash:str) -> None:
        self.imported_data_dir = imported_data_dir
        self.exported_data_dir = exported_data_dir
        self.hash = hash

    @abstractmethod
    def process(self) -> str:
        pass

    def compile(self, output_filename:str = 'report') -> None:
        self.__compile(output_filename)

    def __compile(self, output_filename:str) -> None:

        tex_file_dir = os.path.join(self.imported_data_dir, os.path.normpath(self.hash + '.tex'))
        with open(tex_file_dir, 'w', encoding='utf-8') as tex_file:
            tex_file.write(self.latex)
        
        os.system(f'pdflatex -output-directory {self.imported_data_dir} -jobname={output_filename} {tex_file_dir} > /dev/null 2>&1')
        os.system(f'pdflatex -output-directory {self.imported_data_dir} -jobname={output_filename} {tex_file_dir} > /dev/null 2>&1')
        os.rename(f'{self.imported_data_dir}{output_filename}.pdf', f'{self.exported_data_dir}{output_filename}.pdf')


class Report(Latex):
    ''' Class for creating high-quality typesetting reports for Tri-Chile
    
    Args:
        settings (dict): Dictionary which contains all the information provided by Tri-Chile
        images (dict): Dictionary which contains all the information provided by EasyLabel
        center (dict): Dictionary which contains all the information of the centers
        params (dict): Dictionary which contains all the report parameters
        style (dict): Dictionary which contains all the style parameters
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

    def __init__(self, settings:dict, images:dict, center:dict, params:dict, style:dict, 
                 imported_data_dir:str, exported_data_dir:str, pdf_config, hash:str) -> None:
        super().__init__(imported_data_dir, exported_data_dir, hash)
        self.settings = settings
        self.images = images
        self.center = center
        self.params = params
        self.pdf_config = pdf_config
        self.style = style

    def process(self) -> str:

        # Init classes
        template = Template(self.settings, self.params, self.style)
        bitacora = Bitacora(self.settings, self.images, self.style)

        systems = set([img['system'] for img in self.images.values()])
        for system in systems:
            if system == 'lobero':
                lobera = Lobera(self.settings, self.images, self.params, self.center, self.style, self.imported_data_dir)
                flagLobera = True
            elif system == 'pecero':
                pecera = Pecera(self.settings, self.images, self.params, self.center, self.style, self.imported_data_dir)
                flagPecera = True
            elif system == 'tensor':
                tensor = TensorLobera(self.settings, self.images, self.params, self.center, self.style, self.imported_data_dir)
                flagTensorLobera = True

        if 'a' in self.pdf_config:
            self.latex = template.init_template()
            self.latex += template.front_page()
            self.latex += bitacora.process()
            self.latex += lobera.process() if flagLobera else ''
            self.latex += pecera.process() if flagPecera else ''
            self.latex += tensor.process() if flagTensorLobera else ''
            self.latex += template.back_page()
            self.latex += r'\end{document}'
            self.compile(f"{self.settings['fecha'].replace('-', '_')}_{self.settings['rut'].replace('-','')}_report")

        if 's' in self.pdf_config:
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

            if flagTensorLobera:
                self.latex = template.init_template()
                self.latex += template.front_page()
                self.latex += tensor.process()
                self.latex += template.back_page()
                self.latex += r'\end{document}'
                self.compile(f"{self.settings['fecha'].replace('-', '_')}_{self.settings['rut'].replace('-','')}_tensores")


        if 'b' in self.pdf_config:
            self.latex = template.init_template()
            self.latex += template.front_page()
            self.latex += bitacora.process()
            self.latex += template.back_page()
            self.latex += r'\end{document}'
            self.compile(f"{self.settings['fecha'].replace('-', '_')}_{self.settings['rut'].replace('-','')}_bitacora")

        if 'l' in self.pdf_config:
            self.latex = template.init_template()
            self.latex += template.front_page()
            self.latex += lobera.process()
            self.latex += template.back_page()
            self.latex += r'\end{document}'
            self.compile(f"{self.settings['fecha'].replace('-', '_')}_{self.settings['rut'].replace('-','')}_lobera")
            
        if 'p' in self.pdf_config:
            self.latex = template.init_template()
            self.latex += template.front_page()
            self.latex += pecera.process()
            self.latex += template.back_page()
            self.latex += r'\end{document}'
            self.compile(f"{self.settings['fecha'].replace('-', '_')}_{self.settings['rut'].replace('-','')}_pecera")

        if 't' in self.pdf_config:
            self.latex = template.init_template()
            self.latex += template.front_page()
            self.latex += tensor.process()
            self.latex += template.back_page()
            self.latex += r'\end{document}'
            self.compile(f"{self.settings['fecha'].replace('-', '_')}_{self.settings['rut'].replace('-','')}_tensores")

