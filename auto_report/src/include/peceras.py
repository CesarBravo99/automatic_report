import os


class Pecera():
    ''' Class for creating the fishbowl system in the reports for Tri-Chile
    
    Args:
        settings (dict): Dictionary which contains all the information provided by Tri-Chile
        images (dict): Dictironary which contains all the information provided by EasyLabel
        params (dict): Dictironary which contains internal information
        center (dict): Dictionary wich contarins all the information of the salmon center
        style (dict): Dictionary which contains all the style parameters provided by Tri-Chile
        data_dir (str): Path of the folder where is all the data
    '''

    def __init__(self, settings:dict, images:dict, params:dict, center:dict, style:dict, data_dir:str) -> None:
        self.settings = settings
        self.images = images
        self.style = style
        self.params = params
        self.center = center
        self.img_path = os.path.join(data_dir, 'images/')
    

    def make_fishbowl_background(self) -> str:
        w = self.params['fishbowl']['background']['w']
        h = self.params['fishbowl']['background']['h']
        x = self.params['fishbowl']['background']['x']
        y = self.params['fishbowl']['background']['y']
        color = self.style['fishbowl']['points']
        # data, w, h, x, y, color
        latex = f'''
        \draw [line width=1] {x, y} -- {x, y+h} -- {x+w, y+h} -- {x+w, y} -- cycle;'''
        latex += f'''
        \draw [line width=1] {x+w/2, y+0.875*h/41.5} -- {x+0.5*6.55*w/41.5, y+0.5*6.55*h/41.5} -- 
        {x+0.875*w/41.5, y+h/2} -- {x+0.5*6.55*w/41.5, y+h-0.5*6.55*h/41.5} -- 
        {x+w/2, y+h-0.875*h/41.5} -- {x+w-0.5*6.55*w/41.5, y+h-0.5*6.55*h/41.5} --
        {x+w-0.875*w/41.5, y+h/2} -- {x+w-0.5*6.55*w/41.5, y+0.5*6.55*h/41.5} -- cycle;
        '''
        latex += f'''
        \draw [line width=1] {x+w/2, y+1.75*h/41.5} -- {x+6.55*w/41.5, y+6.55*h/41.5} -- 
        {x+1.75*w/41.5, y+h/2} -- {x+6.55*w/41.5, y+h-6.55*h/41.5} -- 
        {x+w/2, y+h-1.75*h/41.5} -- {x+w-6.55*w/41.5, y+h-6.55*h/41.5} --
        {x+w-1.75*w/41.5, y+h/2} -- {x+w-6.55*w/41.5, y+6.55*h/41.5} -- cycle;
        '''

        latex += f'''
        \draw [dashed][line width=1] {x+w/2-2, y} -- {x+w/2-2, y+h/2};''' +  f'''
        \draw [dashed][line width=1] {x+w/2+2, y} -- {x+w/2+2, y+h/2};''' +  f'''
        \draw {0.5*(x+w/2 + x+6.55*w/41.5), 0.5*(y+1.75*h/41.5 + y+6.55*h/41.5)} -- {x+w/2, y+h/2};''' + f'''
        \draw {x, y} -- {x+w/2, y+h/2};''' + f'''
        \draw {0.5*(x+6.55*w/41.5 + x+1.75*w/41.5), 0.5*(y+6.55*h/41.5 + y+h/2)} -- {x+w/2, y+h/2};''' + f'''
        \draw [dashed][line width=1] {x, y+h/2-2} -- {x+w/2-2, y+h/2-2};''' + f'''
        \draw [dashed][line width=1] {x, y+h/2+2} -- {x+w/2+2, y+h/2+2};''' + f'''
        \draw {0.5*(x+1.75*w/41.5 + x+6.55*w/41.5), 0.5*(y+h/2 + y+h-6.55*h/41.5)} -- {x+w/2, y+h/2};''' + f'''
        \draw {x, y+h} -- {x+w/2, y+h/2};''' + f'''
        \draw {0.5*(x+6.55*w/41.5 + x+w/2), 0.5*(y+h-6.55*h/41.5 + y+h-1.75*h/41.5)} -- {x+w/2, y+h/2};''' + f'''
        \draw [dashed][line width=1] {x+w/2-2, y+h} -- {x+w/2-2, y+h/2};''' + f'''
        \draw [dashed][line width=1] {x+w/2+2, y+h} -- {x+w/2+2, y+h/2};''' + f'''
        \draw {0.5*(x+w/2 + x+w-6.55*w/41.5), 0.5*(y+h-1.75*h/41.5 +  y+h-6.55*h/41.5)} -- {x+w/2, y+h/2};''' + f'''
        \draw {x+w, y+h} -- {x+w/2, y+h/2};''' + f'''
        \draw {0.5*(x+w-6.55*w/41.5 + x+w-1.75*w/41.5), 0.5*(y+h-6.55*h/41.5 +  y+h/2)} -- {x+w/2, y+h/2};''' + f'''
        \draw [dashed][line width=1] {x+w, y+h/2-2} -- {x+w/2, y+h/2-2};''' + f'''
        \draw [dashed][line width=1] {x+w, y+h/2+2} -- {x+w/2, y+h/2+2};''' + f'''
        \draw {0.5*(x+w-1.75*w/41.5 + x+w-6.55*w/41.5), 0.5*(y+h/2 + y+6.55*h/41.5)} -- {x+w/2, y+h/2};''' + f'''
        \draw {x+w, y} -- {x+w/2, y+h/2};''' + f'''
        \draw {0.5*(x+w-6.55*w/41.5 + x+w/2), 0.5*(y+6.55*h/41.5 + y+1.75*h/41.5)} -- {x+w/2, y+h/2};
        '''

        latex += f'''
        \draw {0.5*(x+w/2 + x+6.55*w/41.5), 0.5*(y+1.75*h/41.5 + y+6.55*h/41.5)} -- {0.5*(x+w/2 + x+6.55*w/41.5), y};''' + f'''
        \draw {x+6.55*w/41.5, y+6.55*h/41.5} -- {x, y+6.55*h/41.5};''' + f'''
        \draw {x+6.55*w/41.5, y+6.55*h/41.5} -- {x+6.55*w/41.5, y};''' + f'''
        \draw {0.5*(x+6.55*w/41.5 + x+1.75*w/41.5), 0.5*(y+6.55*h/41.5 + y+h/2)} -- {x, 0.5*(y+6.55*h/41.5 + y+h/2)};''' + f'''
        \draw {0.5*(x+1.75*w/41.5 + x+6.55*w/41.5), 0.5*(y+h/2 + y+h-6.55*h/41.5)} -- {x, 0.5*(y+h/2 + y+h-6.55*h/41.5)};''' + f'''
        \draw {x+6.55*w/41.5, y+h-6.55*h/41.5} -- {x, y+h-6.55*h/41.5};''' + f'''
        \draw {x+6.55*w/41.5, y+h-6.55*h/41.5} -- {x+6.55*w/41.5, y+h};''' + f'''
        \draw {0.5*(x+6.55*w/41.5 + x+w/2), 0.5*(y+h-6.55*h/41.5 + y+h-1.75*h/41.5)} -- {0.5*(x+6.55*w/41.5 + x+w/2), y+h};''' + f'''
        \draw {0.5*(x+w/2 + x+w-6.55*w/41.5), 0.5*(y+h-1.75*h/41.5 +  y+h-6.55*h/41.5)} -- {0.5*(x+w/2 + x+w-6.55*w/41.5), y+h};''' + f'''
        \draw {x+w-6.55*w/41.5, y+h-6.55*h/41.5} -- {x+w, y+h-6.55*h/41.5};''' + f'''
        \draw {x+w-6.55*w/41.5, y+h-6.55*h/41.5} -- {x+w-6.55*w/41.5, y+h};''' + f'''
        \draw {0.5*(x+w-6.55*w/41.5 + x+w-1.75*w/41.5), 0.5*(y+h-6.55*h/41.5 +  y+h/2)} -- {x+w, 0.5*(y+h-6.55*h/41.5 +  y+h/2)};''' + f'''
        \draw {0.5*(x+w-1.75*w/41.5 + x+w-6.55*w/41.5), 0.5*(y+h/2 + y+6.55*h/41.5)} -- {x+w, 0.5*(y+h/2 + y+6.55*h/41.5)};''' + f'''
        \draw {x+w-6.55*w/41.5, y+6.55*h/41.5} -- {x+w, y+6.55*h/41.5};''' + f'''
        \draw {x+w-6.55*w/41.5, y+6.55*h/41.5} -- {x+w-6.55*w/41.5, y};''' + f'''
        \draw {0.5*(x+w-6.55*w/41.5 + x+w/2), 0.5*(y+6.55*h/41.5 + y+1.75*h/41.5)} -- {0.5*(x+w-6.55*w/41.5 + x+w/2), y};
        '''

        latex += f'''
        \draw [fill={color}, fill opacity=1 ]''' + f'''{x+w/2, y+1.75*h/41.5} circle ({0.5*w/41.5});''' + f'''
        \draw [fill={color}, fill opacity=1 ]''' + f'''{0.5*(x+w/2 + x+6.55*w/41.5), 0.5*(y+1.75*h/41.5 + y+6.55*h/41.5)} circle ({0.5*w/41.5});''' + f'''
        \draw [fill={color}, fill opacity=1 ]''' + f'''{x+6.55*w/41.5, y+6.55*h/41.5} circle ({0.5*w/41.5});''' + f'''
        \draw [fill={color}, fill opacity=1 ]''' + f'''{0.5*(x+6.55*w/41.5 + x+1.75*w/41.5), 0.5*(y+6.55*h/41.5 + y+h/2)} circle ({0.5*w/41.5});''' + f'''
        \draw [fill={color}, fill opacity=1 ]''' + f'''{x+1.75*w/41.5, y+h/2} circle ({0.5*w/41.5});''' + f'''
        \draw [fill={color}, fill opacity=1 ]''' + f'''{0.5*(x+1.75*w/41.5 + x+6.55*w/41.5), 0.5*(y+h/2 + y+h-6.55*h/41.5)} circle ({0.5*w/41.5});''' + f'''
        \draw [fill={color}, fill opacity=1 ]''' + f'''{x+6.55*w/41.5, y+h-6.55*h/41.5} circle ({0.5*w/41.5});''' + f'''
        \draw [fill={color}, fill opacity=1 ]''' + f'''{0.5*(x+6.55*w/41.5 + x+w/2), 0.5*(y+h-6.55*h/41.5 + y+h-1.75*h/41.5)} circle ({0.5*w/41.5});''' + f'''
        \draw [fill={color}, fill opacity=1 ]''' + f'''{x+w/2, y+h-1.75*h/41.5} circle ({0.5*w/41.5});''' + f'''
        \draw [fill={color}, fill opacity=1 ]''' + f'''{0.5*(x+w/2 + x+w-6.55*w/41.5), 0.5*(y+h-1.75*h/41.5 +  y+h-6.55*h/41.5)} circle ({0.5*w/41.5});''' + f'''
        \draw [fill={color}, fill opacity=1 ]''' + f'''{x+w-6.55*w/41.5, y+h-6.55*h/41.5} circle ({0.5*w/41.5});''' + f'''
        \draw [fill={color}, fill opacity=1 ]''' + f'''{0.5*(x+w-6.55*w/41.5 + x+w-1.75*w/41.5), 0.5*(y+h-6.55*h/41.5 +  y+h/2)} circle ({0.5*w/41.5});''' + f'''
        \draw [fill={color}, fill opacity=1 ]''' + f'''{x+w-1.75*w/41.5, y+h/2} circle ({0.5*w/41.5});''' + f'''
        \draw [fill={color}, fill opacity=1 ]''' + f'''{0.5*(x+w-1.75*w/41.5 + x+w-6.55*w/41.5), 0.5*(y+h/2 + y+6.55*h/41.5)} circle ({0.5*w/41.5});''' + f'''
        \draw [fill={color}, fill opacity=1 ]''' + f'''{x+w-6.55*w/41.5, y+6.55*h/41.5} circle ({0.5*w/41.5});''' + f'''
        \draw [fill={color}, fill opacity=1 ]''' + f'''{0.5*(x+w-6.55*w/41.5 + x+w/2), 0.5*(y+6.55*h/41.5 + y+1.75*h/41.5)} circle ({0.5*w/41.5});''' + f'''
        '''

        latex += f'''\draw {x+15, y-30} ''' + r'''node [anchor=north] [align=center] [font=''' + self.style['fishbowl']['font']['background'] + r'''] {\textbf{Frontal}};''' 
        # latex += f'''\draw {x+w+15, y+h/2} ''' + r'''node [anchor=north] [rotate=-270] [align=center] {\textbf{Pared Oeste}};''' 
        # latex += f'''\draw {x-30, y+h/2} ''' + r'''node [anchor=north] [rotate=-270] [align=center] {\textbf{Pared Este}};''' 
        latex += f'''\draw {x+w-15, y+h+10} ''' + r'''node [anchor=north] [align=center] [font=''' + self.style['fishbowl']['font']['background'] + r''']{\textbf{Distal}};''' 

        return latex


    def make_fishbowl_lat(self, pos:int) -> str:
        w = self.params['fishbowl'][pos]['w']
        h = self.params['fishbowl'][pos]['h']
        x = self.params['fishbowl'][pos]['x']
        y = self.params['fishbowl'][pos]['y']
        latex = f'''
        \draw [line width=1] {x, y} -- {x, y+1.3*h/16.3} -- {x+w, y+1.3*h/16.3} -- {x+w, y} -- cycle;''' + f'''
        \draw [line width=1] {x+0.5*1.75*w/41.5, y+0.5*9.6*h/16.3} -- {x+w-0.5*1.75*w/41.5, y+0.5*9.6*h/16.3};''' + f'''
        \draw [line width=1] {x+1.75*w/41.5, y+9.6*h/16.3} -- {x+w-1.75*w/41.5, y+9.6*h/16.3};''' 

        latex += f'''
        \draw [line width=1] {x, y+1.3*h/16.3} -- {x + 1.75*w/41.5, y+9.6*h/16.3} --
        {x+w/2, y+h} -- {x+w-1.75*w/41.5, y+9.6*h/16.3} -- {x+w, y+1.3*h/16.3};''' + f'''
        \draw [line width=1] {x, y+1.3*h/16.3} -- {x+0.5*6.55*w/41.5, y+9.6*h/16.3} --
        {x+w/2, y+h} -- {x+w-0.5*6.55*w/41.5, y+9.6*h/16.3} -- {x+w, y+1.3*h/16.3};''' + f'''
        \draw [line width=1] {x, y+1.3*h/16.3} -- {x+6.55*w/41.5, y+9.6*h/16.3} --
        {x+w/2, y+h} -- {x+w-6.55*w/41.5, y+9.6*h/16.3} -- {x+w, y+1.3*h/16.3};''' + f'''
        \draw [line width=1] {x+13.65*w/41.5, y} -- {x+13.65*w/41.5, y+9.6*h/16.3} --
        {x+w/2, y+h} -- {x+w-13.65*w/41.5, y+9.6*h/16.3} -- {x+w-13.65*w/41.5, y};''' + f'''
        \draw [line width=1] {x+6.55*w/41.5, y} -- {x+6.55*w/41.5, y+9.6*h/16.3};''' + f'''
        \draw [line width=1] {x+w-6.55*w/41.5, y} -- {x+w-6.55*w/41.5, y+9.6*h/16.3};''' + f'''
        \draw [dashed] [line width=1] {x+w/2-2, y} -- {x+w/2-2, y+h};''' + f'''
        \draw [dashed] [line width=1] {x+w/2+2, y} -- {x+w/2+2, y+h};'''

        latex += f'''\draw {x+w/2, y-30} ''' + r'''node [anchor=north] [align=center] [font=''' + self.style['fishbowl']['font'][pos] + r''']{\textbf{''' + pos + r'''}};''' 

        return latex


    def fishbowl_points(self, jail:int) -> str:
        latex = ''
        for img, data in self.images.items():
            if data['system'] == 'pecero' and data['jail'] == jail:
                x, y = data['x'], data['y']
                latex += '\n' + r'''\node[] at ''' + f'{x,y}' + r''' (c1) {\tikz\node[''' + self.style['errorType'][data['type']]  + r'''switch ocg=''' + self.images[img]['id'] + r'''] {};}; '''

        ids = [data['id'] for data in self.images.values()]
        ids = ' '.join(ids)

        for img, data in self.images.items():
            latex += r''' 
            \begin{ocg}{}{''' + data['id'] + r'''}{0} 
            \node [] at ''' + self.style['fishbowl']['images']['pos_img'] + r''' {\hideocg{''' + ids +\
            r'''}{\includegraphics[''' + self.style['fishbowl']['images']['config'] + r''']{''' + os.path.join(self.img_path, img) + r'''}}};;
            \node [] at ''' + self.style['fishbowl']['images']['pos_obs'] + r''' [rectangle,draw, fill=white] {
            \huge Observación: ''' +\
            data['obs'] +\
            r'''
            };
            \end{ocg}'''

        return latex


    def process(self) -> None:
        self.latex = ''
        jails = sorted(list(set([data['jail'] for data in self.images.values() if data['system'] == 'pecero'])))
        for jail in jails:
            self.latex += r'''
            \newpage
            \newgeometry{top=3cm, left=1cm, bottom=2.5cm, right=1cm, headsep=1.5cm}
            \invisiblesection{Sistema Pecero}
            \begin{figure}[h!]
            \centering
            \scalebox{1}{
            \tikzset{every pictur"e/.style={line width=0.5pt}}        
            \begin{tikzpicture}[x=0.75pt,y=0.75pt,yscale=-1,xscale=1]''' 

            self.latex += self.make_fishbowl_background()
            self.latex += self.make_fishbowl_lat('frontal')
            self.latex += self.make_fishbowl_lat('distal')
            self.latex += self.make_fishbowl_lat('canal')
            self.latex += self.make_fishbowl_lat('costa')

            self.latex += f'''\draw {self.params['fishbowl']['titles']['title'][0], self.params['fishbowl']['titles']['title'][1]} ''' + r'''node [anchor=north] [font=\LARGE''' + self.style['fishbowl']['font']['title'] + r'''] [align=center] {\textbf{{\LARGE Pecera ''' + jail + r'''}}};''' 

            self.latex += self.fishbowl_points(jail)

            self.latex += r'''
            \end{tikzpicture}
            }
            \end{figure}
            '''
        return self.latex

