import os
from src.include.utils import make_rectangle, make_labels, translate, add_pontoon, add_cardinals


class Lobera():
    ''' Class for creating the seawolf system in the reports for Tri-Chile
    
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


    def make_seawolf_background(self, module:str) -> str:
        w = self.params['seawolf']['background']['w']
        h = self.params['seawolf']['background']['h']
        x = self.params['seawolf']['background']['x']
        y = self.params['seawolf']['background']['y']
        net_color = self.style['seawolf']['net']

        latex = f'''
        \draw {x, y} -- {x+w, y} -- {x+w, y+h} -- {x, y+h} -- cycle ;'''

        latex += f'''
        \draw [color={net_color}, draw opacity=0.5 ] [line width=1]'''+ f'''{x-15, y-15} -- {x-15, y+h+15} -- {x+w+15, y+h+15} -- {x+w+15, y-15} -- cycle;''' + f'''
        \draw [color={net_color}, draw opacity=0.5 ] [line width=1]'''+ f'''{x, y-15} -- {x, y+15+h}; ''' #+ f'''
        for i in range(11):
            if i == 5:
                latex += f'''\draw [color={net_color}, draw opacity=0.5 ] [line width=1]'''+ f'''{x-15, y+h*i/10-2} -- {x+w+15, y+h*i/10-2}; ''' #+ f'''
                latex += f'''\draw [color={net_color}, draw opacity=0.5 ] [line width=1]'''+ f'''{x-15, y+h*i/10+2} -- {x+w+15, y+h*i/10+2}; ''' #+ f'''
            else:
                latex += f'''\draw [color={net_color}, draw opacity=0.5 ] [line width=1]'''+ f'''{x-15, y+h*i/10} -- {x+w+15, y+h*i/10}; ''' #+ f'''

        latex += add_pontoon(self.center['pontoon'][module], w, h, x, y, self.style['seawolf']['pontoon'])
        latex += add_cardinals(self.center['cardinals'][module], w, h, x, y, self.style)

        jails = self.center['jails'][module]
        width = w/(jails/2)
        heigth = h / 2 - 12
        x_space = 2
        y_space = 1.5
        jail_labels = make_labels(jails, self.center['scopes'][module], self.center['x_flip'][module], self.center['y_flip'][module])
        for jail in range(int(jails/2)):
            latex += make_rectangle(x+jail*width+x_space, y+1+6+y_space, width-6-2*x_space, heigth-y_space, jail_labels[jail][0])
            latex += make_rectangle(x+jail*width+x_space, y+h/2+6+y_space, width-6-2*x_space, heigth-y_space, jail_labels[jail][1])
            for i in range(1,6):
                latex += f'''\draw [color={net_color}, draw opacity=0.5 ] [line width=1]'''+ f'''{x+jail*width+width*i/5, y-15} -- {x+jail*width+width*i/5, y+15+h*6/6}; ''' #+ f'''

        return latex
            

    def make_seawolf_lat(self, module:str, pos:int) -> str:
        w = self.params['seawolf']['lateral_' + str(pos)]['w']
        h = self.params['seawolf']['lateral_' + str(pos)]['h']
        x = self.params['seawolf']['lateral_' + str(pos)]['x']
        y = self.params['seawolf']['lateral_' + str(pos)]['y']
        hp = h*0.5 + 2
        net_color = self.style['seawolf']['net']
        jails = self.center['jails'][module]
        width = w/(jails/2)
        latex = f'''
        \draw {x-23, y+h*0/6} -- {x-23, y+h*7/7} ;
        \draw {x-23, y+h*0/6} -- {x-20, y+h*0/6} ;
        \draw {x-23, y+h*1/6} -- {x-20, y+h*1/6} ;
        \draw {x-23, y+h*2/6} -- {x-20, y+h*2/6} ;
        \draw {x-23, y+h*3/6} -- {x-20, y+h*3/6} ;
        \draw {x-23, y+h*4/6} -- {x-20, y+h*4/6} ;
        \draw {x-23, y+h*5/6} -- {x-20, y+h*5/6} ;
        \draw {x-23, y+h*6/6} -- {x-20, y+h*6/6} ;
        \draw {x-27, y+h*0/6-5} node [anchor=north][inner sep=0.75pt]  [align=left]''' + r''' {{\tiny 0}};''' + f'''
        \draw {x-25, y+h*1/6-5} node [anchor=north east][inner sep=0.75pt]  [align=left]''' + r''' {{\tiny 7}};''' + f'''
        \draw {x-25, y+h*2/6-5} node [anchor=north east][inner sep=0.75pt]  [align=left]''' + r''' {{\tiny 14}};''' + f'''
        \draw {x-25, y+h*3/6-5} node [anchor=north east][inner sep=0.75pt]  [align=left]''' + r''' {{\tiny 22}};''' + f'''
        \draw {x-25, y+h*4/6-5} node [anchor=north east][inner sep=0.75pt]  [align=left]''' + r''' {{\tiny 29}};''' + f'''
        \draw {x-25, y+h*5/6-5} node [anchor=north east][inner sep=0.75pt]  [align=left]''' + r''' {{\tiny 36}};''' + f'''
        \draw {x-25, y+h*6/6-5} node [anchor=north east][inner sep=0.75pt]  [align=left]''' + r''' {{\tiny 43}};''' + f'''
        \draw [color={net_color}, draw opacity=0.5 ] [line width=1]''' + f''' 
        {x, y} -- {x-15, y+h*1/6} -- {x-15, y+h*6/6} -- 
        {x+w+15, y+h*6/6} -- {x+w+15, y+h*1/6} -- {x+w, y};
        ''' + f'''\draw [color={net_color}, draw opacity=0.5 ] [line width=1]''' + f'''{x-15, y+h*1/6} -- {x+w+15, y+h*1/6}; ''' + f'''
        \draw [color={net_color}, draw opacity=0.5 ] [line width=1]'''+ f'''{x-15, y+h*2/6} -- {x+w+15, y+h*2/6}; ''' + f'''
        \draw [color={net_color}, draw opacity=0.5 ] [line width=1]'''+ f'''{x-15, y+h*3/6} -- {x+w+15, y+h*3/6}; ''' + f'''
        \draw [color={net_color}, draw opacity=0.5 ] [line width=1]'''+ f'''{x-15, y+h*4/6} -- {x+w+15, y+h*4/6}; ''' + f'''
        \draw [color={net_color}, draw opacity=0.5 ] [line width=1]'''+ f'''{x-15, y+h*5/6} -- {x+w+15, y+h*5/6}; ''' + f'''
        \draw [color={net_color}, draw opacity=0.5 ] [line width=1]'''+ f'''{x, y} -- {x, y+h*6/6}; ''' 

        latex += f'''
        \draw {x+w+23,y+h*0/6} -- {x+w+23, y+h*7/7} ;
        \draw {x+w+23,y+h*0/6} -- {x+w+20, y+h*0/6} ;
        \draw {x+w+23,y+h*1/6} -- {x+w+20, y+h*1/6} ;
        \draw {x+w+23,y+h*2/6} -- {x+w+20, y+h*2/6} ;
        \draw {x+w+23,y+h*3/6} -- {x+w+20, y+h*3/6} ;
        \draw {x+w+23,y+h*4/6} -- {x+w+20, y+h*4/6} ;
        \draw {x+w+23,y+h*5/6} -- {x+w+20, y+h*5/6} ;
        \draw {x+w+23,y+h*6/6} -- {x+w+20, y+h*6/6} ;
        \draw {x+w+28,y+h*0/6-5} node [anchor=north][inner sep=0.75pt]  [align=left]''' + r''' {{\tiny 0}};''' + f'''
        \draw {x+w+33,y+h*1/6-5} node [anchor=north east][inner sep=0.75pt]  [align=left]''' + r''' {{\tiny 7}};''' + f'''
        \draw {x+w+36,y+h*2/6-5} node [anchor=north east][inner sep=0.75pt]  [align=left]''' + r''' {{\tiny 14}};''' + f'''
        \draw {x+w+36,y+h*3/6-5} node [anchor=north east][inner sep=0.75pt]  [align=left]''' + r''' {{\tiny 22}};''' + f'''
        \draw {x+w+36,y+h*4/6-5} node [anchor=north east][inner sep=0.75pt]  [align=left]''' + r''' {{\tiny 29}};''' + f'''
        \draw {x+w+36,y+h*5/6-5} node [anchor=north east][inner sep=0.75pt]  [align=left]''' + r''' {{\tiny 36}};''' + f'''
        \draw {x+w+36,y+h*6/6-5} node [anchor=north east][inner sep=0.75pt]  [align=left]''' + r''' {{\tiny 43}};'''

        jail_labels = make_labels(jails, self.center['scopes'][module], self.center['x_flip'][module], self.center['y_flip'][module])
        for jail in range(int(jails/2)):
            latex += f'''\draw {x+jail*width, y} -- {x+jail*width, y+1.3*hp/16.3} --
            {x+jail*width+1.55*width/41.5, y+9.3*hp/16.3} -- {x+jail*width+width/2, y+hp} --
            {x+jail*width+width-1.55*width/41.5, y+9.3*hp/16.3} -- 
            {x+jail*width+width, y+1.3*hp/16.3} -- {x+jail*width+width, y} -- cycle;
            '''
            latex += r'''
            \draw ''' +\
            f'{x+jail*width+width/2, y-15}' +\
            r''' node [anchor=north] [inner sep=0.75pt] [font=\large] [align=center] {''' + jail_labels[jail][pos] + r'''};'''
            for i in range(1,6):
                latex += f'''\draw [color={net_color}, draw opacity=0.5 ] [line width=1]'''+ f'''{x+jail*width+width*i/5, y} -- {x+jail*width+width*i/5, y+h*6/6}; ''' #+ f'''

        return latex


    def make_seawolf_head(self, module:str, pos:int) -> str:
        w = self.params['seawolf']['head_' + str(pos)]['w']
        h = self.params['seawolf']['head_' + str(pos)]['h']
        x = self.params['seawolf']['head_' + str(pos)]['x']
        y = self.params['seawolf']['head_' + str(pos)]['y']
        hp = h*0.5 + 2
        net_color = self.style['seawolf']['net']
        jails = self.center['jails'][module]
        latex = f'''
        \draw {x-5*w/50, y+h*0/6} -- {x-4*w/50, y+h*0/6} ;
        \draw {x-5*w/50, y+h*1/6} -- {x-4*w/50, y+h*1/6} ;
        \draw {x-5*w/50, y+h*2/6} -- {x-4*w/50, y+h*2/6} ;
        \draw {x-5*w/50, y+h*3/6} -- {x-4*w/50, y+h*3/6} ;
        \draw {x-5*w/50, y+h*0/6} -- {x-5*w/50, y+h*7/7} ;
        \draw {x-5*w/50, y+h*4/6} -- {x-4*w/50, y+h*4/6} ;
        \draw {x-5*w/50, y+h*5/6} -- {x-4*w/50, y+h*5/6} ;
        \draw {x-5*w/50, y+h*6/6} -- {x-4*w/50, y+h*6/6} ;
        \draw {x-6*w/50, y+h*0/6-w/50} node [anchor=north][inner sep=0.75pt]  [align=left]''' + r''' {{\tiny 0}};''' + f'''
        \draw {x-6*w/50, y+h*1/6-w/50} node [anchor=north east][inner sep=0.75pt]  [align=left]''' + r''' {{\tiny 7}};''' + f'''
        \draw {x-6*w/50, y+h*2/6-w/50} node [anchor=north east][inner sep=0.75pt]  [align=left]''' + r''' {{\tiny 14}};''' + f'''
        \draw {x-6*w/50, y+h*3/6-w/50} node [anchor=north east][inner sep=0.75pt]  [align=left]''' + r''' {{\tiny 22}};''' + f'''
        \draw {x-6*w/50, y+h*4/6-w/50} node [anchor=north east][inner sep=0.75pt]  [align=left]''' + r''' {{\tiny 29}};''' + f'''
        \draw {x-6*w/50, y+h*5/6-w/50} node [anchor=north east][inner sep=0.75pt]  [align=left]''' + r''' {{\tiny 36}};''' + f'''
        \draw {x-6*w/50, y+h*6/6-w/50} node [anchor=north east][inner sep=0.75pt]  [align=left]''' + r''' {{\tiny 43}};''' + f'''
        \draw {x+w+5*w/50, y+h*0/6} -- {x+w+5*w/50, y+h*7/7} ;
        \draw {x+w+5*w/50, y+h*0/6} -- {x+w+4*w/50, y+h*0/6} ;
        \draw {x+w+5*w/50, y+h*1/6} -- {x+w+4*w/50, y+h*1/6} ;
        \draw {x+w+5*w/50, y+h*2/6} -- {x+w+4*w/50, y+h*2/6} ;
        \draw {x+w+5*w/50, y+h*3/6} -- {x+w+4*w/50, y+h*3/6} ;
        \draw {x+w+5*w/50, y+h*4/6} -- {x+w+4*w/50, y+h*4/6} ;
        \draw {x+w+5*w/50, y+h*5/6} -- {x+w+4*w/50, y+h*5/6} ;
        \draw {x+w+5*w/50, y+h*6/6} -- {x+w+4*w/50, y+h*6/6} ;
        \draw {x+w+6*w/50, y+h*0/6-w/50} node [anchor=north][inner sep=0.75pt]  [align=right]''' + r''' {{\tiny 0}};''' + f'''
        \draw {x+w+6*w/50, y+h*1/6-w/50} node [anchor=north west][inner sep=0.75pt]  [align=right]''' + r''' {{\tiny 7}};''' + f'''
        \draw {x+w+6*w/50, y+h*2/6-w/50} node [anchor=north west][inner sep=0.75pt]  [align=right]''' + r''' {{\tiny 14}};''' + f'''
        \draw {x+w+6*w/50, y+h*3/6-w/50} node [anchor=north west][inner sep=0.75pt]  [align=right]''' + r''' {{\tiny 22}};''' + f'''
        \draw {x+w+6*w/50, y+h*4/6-w/50} node [anchor=north west][inner sep=0.75pt]  [align=right]''' + r''' {{\tiny 29}};''' + f'''
        \draw {x+w+6*w/50, y+h*5/6-w/50} node [anchor=north west][inner sep=0.75pt]  [align=right]''' + r''' {{\tiny 36}};''' + f'''
        \draw {x+w+6*w/50, y+h*6/6-w/50} node [anchor=north west][inner sep=0.75pt]  [align=right]''' + r''' {{\tiny 43}};'''

        latex += f'''
        \draw [color={net_color}, draw opacity=0.5 ] [line width=1]'''+ f'''{x, y} -- {x-3*w/50, y+h*1/6} -- {x-3*w/50, y+h*6/6} -- {x+w+3*w/50, y+h*6/6} -- {x+w+3*w/50, y+h*1/6} -- {x+w, y};''' + f'''
        \draw [color={net_color}, draw opacity=0.5 ] [line width=1]'''+ f'''{x-3*w/50, y+h*1/6} -- {x+w+3*w/50, y+h*1/6}; ''' + f'''
        \draw [color={net_color}, draw opacity=0.5 ] [line width=1]'''+ f'''{x-3*w/50, y+h*2/6} -- {x+w+3*w/50, y+h*2/6}; ''' + f'''
        \draw [color={net_color}, draw opacity=0.5 ] [line width=1]'''+ f'''{x-3*w/50, y+h*3/6} -- {x+w+3*w/50, y+h*3/6}; ''' + f'''
        \draw [color={net_color}, draw opacity=0.5 ] [line width=1]'''+ f'''{x-3*w/50, y+h*4/6} -- {x+w+3*w/50, y+h*4/6}; ''' + f'''
        \draw [color={net_color}, draw opacity=0.5 ] [line width=1]'''+ f'''{x-3*w/50, y+h*5/6} -- {x+w+3*w/50, y+h*5/6}; ''' + f'''
        \draw [color={net_color}, draw opacity=0.5 ] [line width=1]'''+ f'''{x, y} -- {x, y+h*6/6}; ''' #+ f'''
            
        width = w/2
        jail_labels = make_labels(jails, self.center['scopes'][module], self.center['x_flip'][module], self.center['y_flip'][module])
        for jail in range(2):
            latex += f'''\draw {x+jail*width, y} -- {x+jail*width, y+1.3*hp/16.3} --
            {x+jail*width+1.55*width/41.5, y+9.3*hp/16.3} -- {x+jail*width+width/2, y+hp} --
            {x+jail*width+width-1.55*width/41.5, y+9.3*hp/16.3} -- 
            {x+jail*width+width, y+1.3*hp/16.3} -- {x+jail*width+width, y} -- cycle;
            '''
            for i in range(1,6):
                if jail == 0 and i == 5:
                    latex += f'''\draw [color={net_color}, draw opacity=0.5 ] [line width=1]'''+ f'''{x+jail*width+width*i/5-1.5*w/100,y} -- {x+jail*width+width*i/5-1.5*w/100, y+h*6/6}; ''' #+ f'''
                    latex += f'''\draw [color={net_color}, draw opacity=0.5 ] [line width=1]'''+ f'''{x+width+1.5*w/100,y} -- {x+width+1.5*w/100, y+h*6/6}; ''' 
                else:
                    latex += f'''\draw [color={net_color}, draw opacity=0.5 ] [line width=1]'''+ f'''{x+jail*width+width*i/5,y} -- {x+jail*width+width*i/5, y+h*6/6}; ''' #+ f'''

        if pos == 0:
            label1 = translate(jail_labels[0][0])
            label2 = translate(jail_labels[0][1])
        else:
            label1 = translate(jail_labels[-1][0])
            label2 = translate(jail_labels[-1][1])

        latex += f'\draw {x, y-1.5*h/10}' + r'node [anchor=north] [inner sep=0.75pt] [font=\large] [align=center] {LE' + label1 + r'};'
        latex += f'\draw {x+w, y-1.5*h/10}' + r'node [anchor=north] [inner sep=0.75pt] [font=\large] [align=center] {LE' + label2 + r'};'

        return latex


    def make_seawolf_sep(self) -> str:
        w = self.params['seawolf']['separator']['w']
        h = self.params['seawolf']['separator']['h']
        x = self.params['seawolf']['separator']['x']
        y = self.params['seawolf']['separator']['y']
        hp = h*0.5 + 2
        net_color = self.style['seawolf']['net']
        latex = f'''
        \draw {x-5*w/50, y+h*0/6} -- {x-4*w/50, y+h*0/6} ;
        \draw {x-5*w/50, y+h*1/6} -- {x-4*w/50, y+h*1/6} ;
        \draw {x-5*w/50, y+h*2/6} -- {x-4*w/50, y+h*2/6} ;
        \draw {x-5*w/50, y+h*3/6} -- {x-4*w/50, y+h*3/6} ;
        \draw {x-5*w/50, y+h*0/6} -- {x-5*w/50, y+h*7/7} ;
        \draw {x-5*w/50, y+h*4/6} -- {x-4*w/50, y+h*4/6} ;
        \draw {x-5*w/50, y+h*5/6} -- {x-4*w/50, y+h*5/6} ;
        \draw {x-5*w/50, y+h*6/6} -- {x-4*w/50, y+h*6/6} ;
        \draw {x-6*w/50, y+h*0/6-w/50} node [anchor=north][inner sep=0.75pt]  [align=left]''' + r''' {{\tiny 0}};''' + f'''
        \draw {x-6*w/50, y+h*1/6-w/50} node [anchor=north east][inner sep=0.75pt]  [align=left]''' + r''' {{\tiny 7}};''' + f'''
        \draw {x-6*w/50, y+h*2/6-w/50} node [anchor=north east][inner sep=0.75pt]  [align=left]''' + r''' {{\tiny 14}};''' + f'''
        \draw {x-6*w/50, y+h*3/6-w/50} node [anchor=north east][inner sep=0.75pt]  [align=left]''' + r''' {{\tiny 22}};''' + f'''
        \draw {x-6*w/50, y+h*4/6-w/50} node [anchor=north east][inner sep=0.75pt]  [align=left]''' + r''' {{\tiny 29}};''' + f'''
        \draw {x-6*w/50, y+h*5/6-w/50} node [anchor=north east][inner sep=0.75pt]  [align=left]''' + r''' {{\tiny 36}};''' + f'''
        \draw {x-6*w/50, y+h*6/6-w/50} node [anchor=north east][inner sep=0.75pt]  [align=left]''' + r''' {{\tiny 43}};''' + f'''
        \draw {x+w+5*w/50, y+h*0/6} -- {x+w+5*w/50, y+h*7/7} ;
        \draw {x+w+5*w/50, y+h*0/6} -- {x+w+4*w/50, y+h*0/6} ;
        \draw {x+w+5*w/50, y+h*1/6} -- {x+w+4*w/50, y+h*1/6} ;
        \draw {x+w+5*w/50, y+h*2/6} -- {x+w+4*w/50, y+h*2/6} ;
        \draw {x+w+5*w/50, y+h*3/6} -- {x+w+4*w/50, y+h*3/6} ;
        \draw {x+w+5*w/50, y+h*4/6} -- {x+w+4*w/50, y+h*4/6} ;
        \draw {x+w+5*w/50, y+h*5/6} -- {x+w+4*w/50, y+h*5/6} ;
        \draw {x+w+5*w/50, y+h*6/6} -- {x+w+4*w/50, y+h*6/6} ;
        \draw {x+w+6*w/50, y+h*0/6-w/50} node [anchor=north][inner sep=0.75pt]  [align=right]''' + r''' {{\tiny 0}};''' + f'''
        \draw {x+w+6*w/50, y+h*1/6-w/50} node [anchor=north west][inner sep=0.75pt]  [align=right]''' + r''' {{\tiny 7}};''' + f'''
        \draw {x+w+6*w/50, y+h*2/6-w/50} node [anchor=north west][inner sep=0.75pt]  [align=right]''' + r''' {{\tiny 14}};''' + f'''
        \draw {x+w+6*w/50, y+h*3/6-w/50} node [anchor=north west][inner sep=0.75pt]  [align=right]''' + r''' {{\tiny 22}};''' + f'''
        \draw {x+w+6*w/50, y+h*4/6-w/50} node [anchor=north west][inner sep=0.75pt]  [align=right]''' + r''' {{\tiny 29}};''' + f'''
        \draw {x+w+6*w/50, y+h*5/6-w/50} node [anchor=north west][inner sep=0.75pt]  [align=right]''' + r''' {{\tiny 36}};''' + f'''
        \draw {x+w+6*w/50, y+h*6/6-w/50} node [anchor=north west][inner sep=0.75pt]  [align=right]''' + r''' {{\tiny 43}};'''

        latex += f'''
        \draw [color={net_color}, draw opacity=0.5 ] [line width=1]'''+ f'''{x, y} -- {x-3*w/50, y+h*1/6} -- {x-3*w/50, y+h*6/6} -- {x+w+3*w/50, y+h*6/6} -- {x+w+3*w/50, y+h*1/6} -- {x+w, y};''' + f'''
        \draw [color={net_color}, draw opacity=0.5 ] [line width=1]'''+ f'''{x-3*w/50, y+h*1/6} -- {x+w+3*w/50, y+h*1/6}; ''' + f'''
        \draw [color={net_color}, draw opacity=0.5 ] [line width=1]'''+ f'''{x-3*w/50, y+h*2/6} -- {x+w+3*w/50, y+h*2/6}; ''' + f'''
        \draw [color={net_color}, draw opacity=0.5 ] [line width=1]'''+ f'''{x-3*w/50, y+h*3/6} -- {x+w+3*w/50, y+h*3/6}; ''' + f'''
        \draw [color={net_color}, draw opacity=0.5 ] [line width=1]'''+ f'''{x-3*w/50, y+h*4/6} -- {x+w+3*w/50, y+h*4/6}; ''' + f'''
        \draw [color={net_color}, draw opacity=0.5 ] [line width=1]'''+ f'''{x-3*w/50, y+h*5/6} -- {x+w+3*w/50, y+h*5/6}; ''' + f'''
        \draw [color={net_color}, draw opacity=0.5 ] [line width=1]'''+ f'''{x, y} -- {x, y+h*6/6}; ''' #+ f'''

        width = w/2
        for jail in range(2):
            latex += f'''\draw {x+jail*width, y} -- {x+jail*width, y+1.3*hp/16.3} --
            {x+jail*width+1.55*width/41.5, y+9.3*hp/16.3} -- {x+jail*width+width/2, y+hp} --
            {x+jail*width+width-1.55*width/41.5, y+9.3*hp/16.3} -- 
            {x+jail*width+width, y+1.3*hp/16.3} -- {x+jail*width+width, y} -- cycle;
            '''
            for i in range(1,6):
                if jail == 0 and i == 5:
                    latex += f'''\draw [color={net_color}, draw opacity=0.5 ] [line width=1]'''+ f'''{x+jail*width+width*i/5-1.5*w/100, y} -- {x+jail*width+width*i/5-1.5*w/100, y+h*6/6}; ''' #+ f'''
                    latex += f'''\draw [color={net_color}, draw opacity=0.5 ] [line width=1]'''+ f'''{x+width+1.5*w/100, y} -- {x+width+1.5*w/100, y+h*6/6}; ''' 
                else:
                    latex += f'''\draw [color={net_color}, draw opacity=0.5 ] [line width=1]'''+ f'''{x+jail*width+width*i/5, y} -- {x+jail*width+width*i/5, y+h*6/6}; ''' #+ f'''

        return latex


    def seawolf_points(self, module:str) -> str:
        w_bg = self.params['seawolf']['background']['w']
        h_bg = self.params['seawolf']['background']['h']
        x_bg = self.params['seawolf']['background']['x']
        y_bg = self.params['seawolf']['background']['y']
        w_sep = self.params['seawolf']['separator']['w']
        h_sep = self.params['seawolf']['separator']['h']
        x_sep = self.params['seawolf']['separator']['x']
        y_sep = self.params['seawolf']['separator']['y']
        jails = self.center['jails'][module]
        w_rl = w_bg/(jails/2)

        latex = ''
        separators = {}
        for img, data in self.images.items():
            if data['system'] == 'lobero' and data['module'] == module:
                if data['separator'] == 'None':
                    x, y = data['x'], data['y']
                    latex += '\n' + r'''\node[scale=1] at ''' + f'{x,y}' + r''' (c1) {\tikz\node[''' + self.style['errorType'][data['type']]  + r'''switch ocg=''' + data['id'] + r'''] {};}; '''
                elif data['separator'] != 'None':
                    if '_'.join(data['separator']) not in separators: separators['_'.join(data['separator'])] = [img]
                    else: separators['_'.join(data['separator'])].append(img)

        for separator in separators.keys():
            labels = separator.split('_')
            aux = float(labels[1][1:]) if float(labels[1][1:]) >= float(labels[0][1:]) else float(labels[0][1:])
            xline = x_bg + (aux//2)*w_rl
            latex += f'''
            \draw[line width=2pt, color={self.style['ocg']['color']['separator_bar']}, fill={self.style['ocg']['color']['separator_bar']}!100]''' + f'{xline, y_bg} -- {xline, y_bg+h_bg};' + r'''
            \node[] at ''' + f'{xline, y_bg+h_bg/2}' + r''' (c1) {\tikz\node[circle, draw=''' + f'''{self.style['ocg']['color']['separator_dot']}, fill={self.style['ocg']['color']['separator_dot']}!20, minimum size=0.05cm, switch ocg = S''' + str(separator) + r'''] {};};'''

        for separator, imgs in separators.items():
            latex += r'''\begin{ocg}[radiobtngrp=myRadioButtons]{}{S''' + separator + r'''}{0}'''
            labels = separator.split('_')
            latex += '\n' + r'''\node [scale=1] [font=\large] at ''' + f'{x_sep, y_sep-10}' + r''' (c1) {\tikz\node[switch ocg=''' + separator + r'''] {''' + labels[0] + r'''};}; '''
            latex += '\n' + r'''\node [scale=1] [font=\large] at ''' + f'{x_sep+w_sep, y_sep-10}' + r''' (c1) {\tikz\node[switch ocg=''' + separator + r'''] {''' + labels[1] + r'''};}; '''
            for img in imgs:
                x, y = self.images[img]['x'], self.images[img]['y']
                latex += '\n' + r'''\node[scale=1] at ''' + f'{x,y}' + r''' (c1) {\tikz\node[''' + self.style['errorType'][self.images[img]['type']]  + r'''switch ocg=''' + self.images[img]['id'] + r'''] {};}; '''
            latex += r'''\end{ocg} '''     


        ids = [data['id'] for data in self.images.values()]
        ids = ' '.join(ids)

        for img, data in self.images.items():
            latex += r''' 
            \begin{ocg}{}{''' + data['id'] + r'''}{0} 
            \node [] at ''' + self.style['seawolf']['images']['pos_img'] + r''' {\hideocg{''' + ids +\
            r'''}{\includegraphics[''' + self.style['seawolf']['images']['config'] + r''']{''' + os.path.join(self.img_path, img) + r'''}}};;
            \node [] at ''' + self.style['seawolf']['images']['pos_obs'] + r''' [rectangle,draw, fill=white] {
            \huge Observación: ''' +\
            data['obs'] +\
            r'''
            };
            \end{ocg}'''

        return latex


    def process(self) -> None:
        self.latex = ''       
        for module in range(self.center['modules']):
            module = str(module)
            self.latex += r'''
            \newpage
            \newgeometry{top=3cm, left=1cm, bottom=2.5cm, right=1cm, headsep=1.5cm}
            \vspace{0.1cm}
            \invisiblesection{Sistema Lobero}
            \begin{figure}[h!]'''
            self.latex += self.style['seawolf']['font']['numbers']
            self.latex += r'''
            \centering
            \scalebox{1}{
            \tikzset{every picture/.style={line width=0.5pt}}        
            \begin{tikzpicture}[x=0.75pt, y=0.75pt, yscale=-1, xscale=1]''' 

            self.latex += f'''\draw {self.params['seawolf']['titles']['background'][0], self.params['seawolf']['titles']['background'][1]} ''' +  r'''node [anchor=north] [font=\large''' + self.style['seawolf']['font']['background'] + r'''] [align=center] {\textbf{INSPECCIÓN FONDO LOBERO}};'''
            self.latex += self.make_seawolf_background(module)

            self.latex += f'''\draw {self.params['seawolf']['titles']['lateral'][0], self.params['seawolf']['titles']['lateral'][1]} ''' +  r'''node [anchor=north] [font=\large''' + self.style['seawolf']['font']['lateral'] + r'''] [align=center] {\textbf{INSPECCIÓN LATERAL LOBERO}};'''
            self.latex += self.make_seawolf_lat(module, 0)
            self.latex += self.make_seawolf_lat(module, 1)

            self.latex += f'''\draw {self.params['seawolf']['titles']['head'][0], self.params['seawolf']['titles']['head'][1]} ''' + r'''node [anchor=north] [font=\large''' + self.style['seawolf']['font']['head'] + r'''] [align=center] {\textbf{INSPECCIÓN CABECERAS}};'''
            self.latex += self.make_seawolf_head(module, 0)
            self.latex += self.make_seawolf_head(module, 1)

            self.latex += f'''\draw {self.params['seawolf']['titles']['separator'][0], self.params['seawolf']['titles']['separator'][1]} ''' + r'''node [anchor=north] [font=\large''' + self.style['seawolf']['font']['separator'] + r'''] [align=center] {\textbf{INSPECCIÓN DE MAMPAROS}};''' 
            self.latex += self.make_seawolf_sep()

            self.latex += self.seawolf_points(module)


            self.latex += r'''
            \end{tikzpicture}
            }
            \end{figure}
            '''

        return self.latex
