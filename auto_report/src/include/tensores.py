import os
from src.include.utils import make_rectangle, make_labels, make_tensor_labels, translate


class Tensor():
    ''' Class for creating the tensor system in the reports for Tri-Chile
    
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


    def make_tensor_mooring(self, w:int, h:int, x:int, y:int) -> str:
        buoy_color = self.style['tensors']['buoy']
        tensor_color = self.style['tensors']['tensor']

        latex = r'''
        \draw [fill={''' + buoy_color + r'''}  ,fill opacity=1 ]''' + f''' {x,y} -- {x-w/10, y-h/20} -- {x-w/10, y-h*2/20} -- {x-w/20, y-h*2.5/20} -- {x+w/20, y-h*2.5/20} -- {x+w/10, y-h*2/20} -- {x+w/10, y-h/20} -- cycle;
        '''
        latex += f'''\draw [line width=1] {x, y+4} -- {x, y+h/4-2};'''
        latex += f'''\draw [line width=1] {x, y+h/4+2} -- {x, y+h*2/4-2};'''
        latex += f'''\draw [line width=1] {x, y+h*2/4+2} -- {x, y+h*3/4-2};'''
        latex += f'''\draw [line width=1] {x, y+h*3/4+2} -- {x, y+h*4/4-2};'''
        latex += r'''\draw [fill={rgb, 255:red, 0; green, 0; blue, 0}, fill opacity=1] ''' + f'''{x-w/20, y+h+3} -- {x+w/20, y+h+3} -- {x+w/10, y+h+3+h/10} -- {x-w/10, y+h+3+h/10} -- cycle;'''
        latex += f'''\draw [color={tensor_color}, draw opacity=0.5 ] [line width=1]'''+ f'''{x-2, y+h*1/4} -- {x-w*0.6, y+h*1/4+0.3*h/4};'''
        latex += f'''\draw [color={tensor_color}, draw opacity=0.5 ] [line width=1]'''+ f'''{x-2, y+h*1/4} -- {x-w*0.6, y+h*1/4};'''
        latex += f'''\draw [color={tensor_color}, draw opacity=0.5 ] [line width=1]'''+ f'''{x-2, y+h*1/4} -- {x-w*0.6, y+h*1/4-0.3*h/4};'''
        latex += f'''\draw [color={tensor_color}, draw opacity=0.5 ] [line width=1]'''+ f'''{x+2, y+h*1/4} -- {x+w/2, y+h*1/4-0.8*h/4};'''
        latex += f'''\draw [color={tensor_color}, draw opacity=0.5 ] [line width=1]'''+ f'''{x-2, y+h*2/4} -- {x-w*0.6, y+h*2/4+0.3*h/4};'''
        latex += f'''\draw [color={tensor_color}, draw opacity=0.5 ] [line width=1]'''+ f'''{x-2, y+h*2/4} -- {x-w*0.6, y+h*2/4};'''
        latex += f'''\draw [color={tensor_color}, draw opacity=0.5 ] [line width=1]'''+ f'''{x-2, y+h*2/4} -- {x-w*0.6, y+h*2/4-0.3*h/4};'''
        latex += f'''\draw [color={tensor_color}, draw opacity=0.5 ] [line width=1]'''+ f'''{x+2, y+h*2/4} -- {x+w/2, y+h*2/4-0.8*h/4};'''
        latex += f'''\draw [color={tensor_color}, draw opacity=0.5 ] [line width=1]'''+ f'''{x-2, y+h*3/4} -- {x-w*0.6, y+h*3/4+0.3*h/4};'''
        latex += f'''\draw [color={tensor_color}, draw opacity=0.5 ] [line width=1]'''+ f'''{x-2, y+h*3/4} -- {x-w*0.6, y+h*3/4};'''
        latex += f'''\draw [color={tensor_color}, draw opacity=0.5 ] [line width=1]'''+ f'''{x-2, y+h*3/4} -- {x-w*0.6, y+h*3/4-0.3*h/4};'''
        latex += f'''\draw [color={tensor_color}, draw opacity=0.5 ] [line width=1]'''+ f'''{x+2, y+h*3/4} -- {x+w/2, y+h*3/4-0.8*h/4};'''
        latex += f'''\draw [color={tensor_color}, draw opacity=0.5 ] [line width=1]'''+ f'''{x-2, y+h*4/4} -- {x-w*0.6, y+h*4/4+0.3*h/4};'''
        latex += f'''\draw [color={tensor_color}, draw opacity=0.5 ] [line width=1]'''+ f'''{x-2, y+h*4/4} -- {x-w*0.6, y+h*4/4};'''
        latex += f'''\draw [color={tensor_color}, draw opacity=0.5 ] [line width=1]'''+ f'''{x-2, y+h*4/4} -- {x-w*0.6, y+h*4/4-0.3*h/4};'''
        latex += f'''\draw [color={tensor_color}, draw opacity=0.5 ] [line width=1]'''+ f'''{x+2, y+h*4/4} -- {x+w/2, y+h*4/4-0.8*h/4};'''
        latex += f'''\draw {x, y+2} circle ({0.02*h});''' 
        latex += f'''\draw {x, y+h/4} circle ({0.02*h});''' 
        latex += f'''\draw {x, y+h*2/4} circle ({0.02*h});''' 
        latex += f'''\draw {x, y+h*3/4} circle ({0.02*h});''' 
        latex += f'''\draw {x, y+h} circle ({0.02*h});''' 

        return latex


    def make_tensor_system(self, module:str) -> str:
        w = self.params['tensors']['system']['w']
        h = self.params['tensors']['system']['h']
        x = self.params['tensors']['system']['x']
        y = self.params['tensors']['system']['y']
        tensor_color = self.style['tensors']['tensor']
        net_color = self.style['tensors']['net']

        latex = f'''\draw {x, y} -- {x + w, y} -- {x + w, y + h} -- {x, y + h} -- cycle ;'''
        latex += f''' \draw [color={net_color}, draw opacity=0.5 ] [line width=1]'''+ f'''{x-15, y-15} -- {x-15, y+h+15} -- {x+w+15, y+h+15} -- {x+w+15, y-15} -- cycle;'''
        latex += f'''\draw [color={net_color}, draw opacity=0.5 ] [line width=1]'''+ f'''{x-15, y-15} -- {x, y}; '''
        latex += f'''\draw [color={net_color}, draw opacity=0.5 ] [line width=1]'''+ f'''{x-15, y+h+15} -- {x, y+h}; '''
        latex += f'''\draw [color={net_color}, draw opacity=0.5 ] [line width=1]'''+ f'''{x+w+15, y-15} -- {x+w, y}; '''
        latex += f'''\draw [color={net_color}, draw opacity=0.5 ] [line width=1]'''+ f'''{x+w+15, y+h+15} -- {x+w, y+h}; '''
        latex += f'''\draw [color={net_color}, draw opacity=0.5 ] [line width=1]'''+ f'''{x, y-15} -- {x,y}; ''' 
        latex += f'''\draw [color={net_color}, draw opacity=0.5 ] [line width=1]'''+ f'''{x, y+h+15} -- {x, y+h}; ''' 
            
        jails = self.center['jails'][module]
        width = w/(jails/2)

        heigth = h / 2 - 12
        x_space = 2
        y_space = 1.5
        jail_labels = make_labels(jails, self.center['scopes'][module], self.center['x_flip'][module], self.center['y_flip'][module])
        tensor_labels = make_tensor_labels(jails, self.center['x_flip'][module], self.center['y_flip'][module])
        for jail in range(int(jails/2)):
            latex += make_rectangle(x+jail*width+x_space, y+1+6+y_space, width-6-2*x_space, heigth-y_space, jail_labels[jail][0])
            latex += make_rectangle(x+jail*width+x_space, y+h/2+6+y_space, width-6-2*x_space, heigth-y_space, jail_labels[jail][1])
            for i in range(1, 6):
                latex += f'''\draw [color={net_color}, draw opacity=0.5 ] [line width=1]'''+ f'''{x+jail*width+width*i/5, y-15} -- {x+jail*width+width*i/5,y}; ''' 
                latex += f'''\draw [color={net_color}, draw opacity=0.5 ] [line width=1]'''+ f'''{x+jail*width+width*i/5, y+h} -- {x+jail*width+width*i/5,y+15+h}; '''
                if i == 2 or i == 3: 
                    latex += f'''\draw [fill={self.style['tensors']['dots']}, fill opacity=1 ]''' + f'''{x+jail*width+width*i/5, y+1} circle ({0.005*w});''' 
                    latex += f'''\draw [fill={self.style['tensors']['dots']}, fill opacity=1 ]''' + f'''{x+jail*width+width*i/5, y+h/2} circle ({0.005*w});''' 
                    latex += f'''\draw [fill={self.style['tensors']['dots']}, fill opacity=1 ]''' + f'''{x+jail*width+width*i/5, y+h-1} circle ({0.005*w});''' 
                elif i == 5 and jail != int(jails/2)-1:
                    latex += f'''\draw [color={tensor_color}, draw opacity=0.5 ] [line width=1]'''+ f'''{x+jail*width+width*i/5, y-15} -- {x+jail*width+width*i/5,y-60}; ''' 
                    latex += f'''\draw [color={tensor_color}, draw opacity=0.5 ] [line width=1]'''+ f'''{x+jail*width+width*(i-2)/5, y-15} -- {x+jail*width+width*i/5,y-60}; ''' 
                    latex += f'''\draw [color={tensor_color}, draw opacity=0.5 ] [line width=1]'''+ f'''{x+(jail+1)*width+width*2/5, y-15} -- {x+jail*width+width*i/5,y-60}; ''' 
                    latex += f'''\draw [fill={self.style['tensors']['buoy']}, fill opacity=1 ]''' + f'''{x+jail*width+width*i/5, y-60} circle ({0.005*w});''' 
                    latex += f'''\draw {x+jail*width+width*i/5, y-70} ''' + r'''node [anchor=south] [font=\large''' + self.style['tensors']['font']['labels'] + r'''] [align=center] {''' + tensor_labels[jail][0] + r'''};''' 
                    latex += self.make_tensor_mooring(0.8*width, h, x+jail*width+width*i/5, y-70-1.5*h)

                    latex += f'''\draw [color={tensor_color}, draw opacity=0.5 ] [line width=1]'''+ f'''{x+jail*width+width*i/5, y+h+15} -- {x+jail*width+width*i/5,y+h+60}; ''' 
                    latex += f'''\draw [color={tensor_color}, draw opacity=0.5 ] [line width=1]'''+ f'''{x+jail*width+width*(i-2)/5, y+h+15} -- {x+jail*width+width*i/5,y+h+60}; ''' 
                    latex += f'''\draw [color={tensor_color}, draw opacity=0.5 ] [line width=1]'''+ f'''{x+(jail+1)*width+width*2/5, y+h+15} -- {x+jail*width+width*i/5,y+h+60}; ''' 
                    latex += f'''\draw [fill={self.style['tensors']['buoy']}, fill opacity=1 ]''' + f'''{x+jail*width+width*i/5, y+h+60} circle ({0.005*w});''' 
                    latex += f'''\draw {x+jail*width+width*i/5, y+h+70} ''' + r'''node [anchor=north] [font=\large''' + self.style['tensors']['font']['labels'] + r'''] [align=center] {''' + tensor_labels[jail][1] + r'''};''' 
                    latex += self.make_tensor_mooring(0.8*width, h, x+jail*width+width*i/5, y+h+70+0.5*h)


        latex += f'''\draw [color={tensor_color}, draw opacity=0.5 ] [line width=1]'''+ f'''{x, y-15} -- {x,y-60}; ''' 
        latex += f'''\draw [color={tensor_color}, draw opacity=0.5 ] [line width=1]'''+ f'''{x-15, y-15} -- {x,y-60}; ''' 
        latex += f'''\draw [color={tensor_color}, draw opacity=0.5 ] [line width=1]'''+ f'''{x+width*2/5, y-15} -- {x,y-60}; ''' 
        latex += f'''\draw [fill={self.style['tensors']['buoy']}, fill opacity=1 ]''' + f'''{x, y-60} circle ({0.005*w});''' 
        latex += f'''\draw {x, y-70} ''' + r'''node [anchor=south] [font=\large''' + self.style['tensors']['font']['labels'] + r'''] [align=center] {LE''' + translate(jail_labels[0][0]) + r'};'
        latex += self.make_tensor_mooring(0.1*w, h, x, y-70-1.5*h)

        latex += f'''\draw [color={tensor_color}, draw opacity=0.5 ] [line width=1]'''+ f'''{x+w, y-15} -- {x+w, y-60}; ''' 
        latex += f'''\draw [color={tensor_color}, draw opacity=0.5 ] [line width=1]'''+ f'''{x+w+15, y-15} -- {x+w, y-60}; ''' 
        latex += f'''\draw [color={tensor_color}, draw opacity=0.5 ] [line width=1]'''+ f'''{x+w-width*2/5, y-15} -- {x+w, y-60}; ''' 
        latex += f'''\draw [fill={self.style['tensors']['buoy']}, fill opacity=1 ]''' + f'''{x+w, y-60} circle ({0.005*w});''' 
        latex += f'''\draw {x+w, y-70} ''' + r'''node [anchor=south] [font=\large''' + self.style['tensors']['font']['labels'] + r'''] [align=center] {LE''' + translate(jail_labels[-1][0]) + r'};'
        latex += self.make_tensor_mooring(0.1*w, h, x+w, y-70-1.5*h)

        latex += f'''\draw [color={tensor_color}, draw opacity=0.5 ] [line width=1]'''+ f'''{x, y+h+15} -- {x,y+h+60}; ''' 
        latex += f'''\draw [color={tensor_color}, draw opacity=0.5 ] [line width=1]'''+ f'''{x-15, y+h+15} -- {x,y+h+60}; ''' 
        latex += f'''\draw [color={tensor_color}, draw opacity=0.5 ] [line width=1]'''+ f'''{x+width*2/5, y+h+15} -- {x,y+h+60}; ''' 
        latex += f'''\draw [fill={self.style['tensors']['buoy']}, fill opacity=1 ]''' + f'''{x, y+h+60} circle ({0.005*w});''' 
        latex += f'''\draw {x, y+h+70} ''' + r'''node [anchor=north] [font=\large''' + self.style['tensors']['font']['labels'] + r'''] [align=center] {LE''' + translate(jail_labels[0][1]) + r'};'
        latex += self.make_tensor_mooring(0.1*w, h, x, y+h+70+0.5*h)

        latex += f'''\draw [color={tensor_color}, draw opacity=0.5 ] [line width=1]'''+ f'''{x+w, y+h+15} -- {x+w, y+h+60}; ''' 
        latex += f'''\draw [color={tensor_color}, draw opacity=0.5 ] [line width=1]'''+ f'''{x+w+15, y+h+15} -- {x+w, y+h+60}; ''' 
        latex += f'''\draw [color={tensor_color}, draw opacity=0.5 ] [line width=1]'''+ f'''{x+w-width*2/5, y+h+15} -- {x+w, y+h+60}; ''' 
        latex += f'''\draw [fill={self.style['tensors']['buoy']}, fill opacity=1 ]''' + f'''{x+w, y+h+60} circle ({0.005*w});''' 
        latex += f'''\draw {x+w, y+h+70} ''' + r'''node [anchor=north] [font=\large''' + self.style['tensors']['font']['labels'] + r'''] [align=center] {LE''' + translate(jail_labels[-1][1]) + r'};'
        latex += self.make_tensor_mooring(0.1*w, h, x+w, y+h+70+0.5*h)
            
        for i in range(11):
            latex += f'''\draw [color={net_color}, draw opacity=0.5 ] [line width=1]'''+ f'''{x-15, y+h*i/10} -- {x, y+h*i/10}; '''
            latex += f'''\draw [color={net_color}, draw opacity=0.5 ] [line width=1]'''+ f'''{x+w, y+h*i/10} -- {x+w+15, y+h*i/10}; '''
            if i == 0 or i == 10:
                pass
            elif i%2 == 0 or i == 5:
                latex += f'''\draw [fill={self.style['tensors']['dots']}, fill opacity=1 ]''' + f'''{x+1, y+h*i/10} circle ({0.005*w});''' 
                latex += f'''\draw [fill={self.style['tensors']['dots']}, fill opacity=1 ]''' + f'''{x+w-1, y+h*i/10} circle ({0.005*w});''' 

            latex += f'''\draw [fill={self.style['tensors']['dots']}, fill opacity=1 ]''' + f'''{x+2, y+2} circle ({0.005*w});''' 
            latex += f'''\draw [fill={self.style['tensors']['dots']}, fill opacity=1 ]''' + f'''{x+w-2, y+2} circle ({0.005*w});''' 
            latex += f'''\draw [fill={self.style['tensors']['dots']}, fill opacity=1 ]''' + f'''{x+2, y+h-2} circle ({0.005*w});''' 
            latex += f'''\draw [fill={self.style['tensors']['dots']}, fill opacity=1 ]''' + f'''{x+w-2, y+h-2} circle ({0.005*w});''' 
        
        latex += f'''\draw [color={tensor_color}, draw opacity=0.5 ] [line width=1]'''+ f'''{x-15, y} -- {x-60, y}; ''' 
        latex += f'''\draw [color={tensor_color}, draw opacity=0.5 ] [line width=1]'''+ f'''{x-15, y-15} -- {x-60, y}; ''' 
        latex += f'''\draw [color={tensor_color}, draw opacity=0.5 ] [line width=1]'''+ f'''{x-15, y+h*2/10} -- {x-60, y}; ''' 
        latex += f'''\draw [fill={self.style['tensors']['buoy']}, fill opacity=1 ]''' + f'''{x-60, y} circle ({0.005*w});''' 
        latex += f'''\draw {x-70, y} ''' + r'''node [anchor=south] [font=\large''' + self.style['tensors']['font']['labels'] + r'''] [align=center] {CE''' + translate(jail_labels[0][0]) + r'};'
        latex += self.make_tensor_mooring(0.1*w, h, x-70-(0.1*w)/2, y-70-1*h)

        latex += f'''\draw [color={tensor_color}, draw opacity=0.5 ] [line width=1]'''+ f'''{x+w+15, y} -- {x+w+60, y}; ''' 
        latex += f'''\draw [color={tensor_color}, draw opacity=0.5 ] [line width=1]'''+ f'''{x+w+15, y-15} -- {x+w+60, y}; ''' 
        latex += f'''\draw [color={tensor_color}, draw opacity=0.5 ] [line width=1]'''+ f'''{x+w+15, y+h*2/10} -- {x+w+60, y}; ''' 
        latex += f'''\draw [fill={self.style['tensors']['buoy']}, fill opacity=1 ]''' + f'''{x+w+60, y} circle ({0.005*w});''' 
        latex += f'''\draw {x+w+70, y} ''' + r'''node [anchor=south] [font=\large''' + self.style['tensors']['font']['labels'] + r'''] [align=center] {CE''' + translate(jail_labels[-1][0]) + r'};'
        latex += self.make_tensor_mooring(0.1*w, h, x+w+70+0.6*(0.1*w), y-70-1*h)

        latex += f'''\draw [color={tensor_color}, draw opacity=0.5 ] [line width=1]'''+ f'''{x-15, y+h} -- {x-60, y+h}; ''' 
        latex += f'''\draw [color={tensor_color}, draw opacity=0.5 ] [line width=1]'''+ f'''{x-15, y+h+15} -- {x-60, y+h}; ''' 
        latex += f'''\draw [color={tensor_color}, draw opacity=0.5 ] [line width=1]'''+ f'''{x-15, y+h-h*2/10} -- {x-60, y+h}; ''' 
        latex += f'''\draw [fill={self.style['tensors']['buoy']}, fill opacity=1 ]''' + f'''{x-60, y+h} circle ({0.005*w});''' 
        latex += f'''\draw {x-70, y+h} ''' + r'''node [anchor=north] [font=\large''' + self.style['tensors']['font']['labels'] + r'''] [align=center] {CE''' + translate(jail_labels[0][1]) + r'};'
        latex += self.make_tensor_mooring(0.1*w, h, x-70-(0.1*w)/2, y+h+70+0*h)

        latex += f'''\draw [color={tensor_color}, draw opacity=0.5 ] [line width=1]'''+ f'''{x+w+15, y+h} -- {x+w+60, y+h}; ''' 
        latex += f'''\draw [color={tensor_color}, draw opacity=0.5 ] [line width=1]'''+ f'''{x+w+15, y+h+15} -- {x+w+60, y+h}; ''' 
        latex += f'''\draw [color={tensor_color}, draw opacity=0.5 ] [line width=1]'''+ f'''{x+w+15, y+h-h*2/10} -- {x+w+60, y+h}; ''' 
        latex += f'''\draw [fill={self.style['tensors']['buoy']}, fill opacity=1 ]''' + f'''{x+w+60, y+h} circle ({0.005*w});''' 
        latex += f'''\draw {x+w+70, y+h} ''' + r'''node [anchor=north] [font=\large''' + self.style['tensors']['font']['labels'] + r'''] [align=center] {CE''' + translate(jail_labels[-1][1]) + r'};'
        latex += self.make_tensor_mooring(0.1*w, h, x+w+70+0.6*(0.1*w), y+h+70+0*h)

        latex += f'''\draw [color={tensor_color}, draw opacity=0.5 ] [line width=1]'''+ f'''{x-15, y+h/2} -- {x-60, y+h/2}; ''' 
        latex += f'''\draw [color={tensor_color}, draw opacity=0.5 ] [line width=1]'''+ f'''{x-15, y+h/2-h/10} -- {x-60, y+h/2}; ''' 
        latex += f'''\draw [color={tensor_color}, draw opacity=0.5 ] [line width=1]'''+ f'''{x-15, y+h/2+h/10} -- {x-60, y+h/2}; ''' 
        latex += f'''\draw [fill={self.style['tensors']['buoy']}, fill opacity=1 ]''' + f'''{x-60, y+h/2} circle ({0.005*w});''' 
        latex += f'''\draw {x-70, y+h/2} ''' + r'''node [anchor=south] [font=\large''' + self.style['tensors']['font']['labels'] + r'''] [align=center] {C''' + translate(jail_labels[0][0],  True) + r'};'
        latex += self.make_tensor_mooring(0.1*w, h, x-70-(0.1*w)/2-20, y)

        latex += f'''\draw [color={tensor_color}, draw opacity=0.5 ] [line width=1]'''+ f'''{x+w+15, y+h/2} -- {x+w+60, y+h/2}; ''' 
        latex += f'''\draw [color={tensor_color}, draw opacity=0.5 ] [line width=1]'''+ f'''{x+w+15, y+h/2-h/10} -- {x+w+60, y+h/2}; ''' 
        latex += f'''\draw [color={tensor_color}, draw opacity=0.5 ] [line width=1]'''+ f'''{x+w+15, y+h/2+h/10} -- {x+w+60, y+h/2}; ''' 
        latex += f'''\draw [fill={self.style['tensors']['buoy']}, fill opacity=1 ]''' + f'''{x+w+60, y+h/2} circle ({0.005*w});''' 
        latex += f'''\draw {x+w+70, y+h/2} ''' + r'''node [anchor=north] [font=\large''' + self.style['tensors']['font']['labels'] + r'''] [align=center] {C''' + translate(jail_labels[-1][0],  True) + r'};'
        latex += self.make_tensor_mooring(0.1*w, h, x+w+70+0.6*(0.1*w)+20, y)

        return latex


    def tensor_points(self, module:str) -> str:
        latex = ''
        for img, data in self.images.items():
            if data['system'] == 'tensor' and data['module'] == module:
                x, y = data['x'], data['y']
                latex += '\n' + r'''\node[scale=1] at ''' + f'{x,y}' + r''' (c1) {\tikz\node[''' + self.style['errorType'][data['type']]  + r'''switch ocg=''' + self.images[img]['id'] + r'''] {};}; '''

        ids = [data['id'] for data in self.images.values()]
        ids = ' '.join(ids)

        for img, data in self.images.items():
            latex += r''' 
            \begin{ocg}{}{''' + data['id'] + r'''}{0} 
            \node [] at ''' + self.style['tensors']['images']['pos_img'] + r''' {\hideocg{''' + ids +\
            r'''}{\includegraphics[''' + self.style['tensors']['images']['config'] + r''']{''' + os.path.join(self.img_path, img) + r'''}}};;
            \node [] at ''' + self.style['tensors']['images']['pos_obs'] + r''' [rectangle,draw, fill=white] {
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
            \invisiblesection{Sistema de Tensores}
            \begin{figure}[h]'''
            self.latex += self.style['tensors']['font']['numbers']
            self.latex += r'''
            \centering
            \tikzset{every picture/.style={line width=0.5pt}}        
            \begin{tikzpicture}[x=0.75pt,y=0.75pt,yscale=-1,xscale=1]''' 


            self.latex += self.make_tensor_system(module)
            self.latex += self.tensor_points(module)
            self.latex += r'''
            \end{tikzpicture}
            \end{figure}
            '''   

        return self.latex
