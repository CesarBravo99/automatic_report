import os
from pathlib import Path
import json 
import numpy as np
from PIL import Image
from pdf2image import convert_from_path


def crop(path):
    image = Image.open(path)
    img = np.asanyarray(image)
    x_max = np.amax(np.sum(img, 0))
    y_max = np.amax(np.sum(img, 1))
    x = [idx for idx, val in enumerate(np.sum(img[:, :, 0], 0)) if val != x_max]
    y = [idx for idx, val in enumerate(np.sum(img[:, :, 0], 1)) if val != y_max]
    crop = image.crop((x[0], y[0], x[-1], y[-1]))
    return crop.save(path, 'png')



def make_rectangle(x, y, w, h, label):
    rectange = f'''\draw {x,y} .. controls {x,y-3} and {x+3,y-6} .. {x+6,y-6} 
    -- {x+w,y-6} .. controls {x+w+3,y-6} and {x+w+6,y-3} .. {x+w+6,y} 
    -- {x+w+6,y+h-3} .. controls {x+w+6,y+h} and {x+w+3,y+h+3} .. {x+w,y+h+3}
    -- {x+6,y+h+3} .. controls {x+3,y+h+3} and {x,y+h} .. {x,y+h-3}
    -- cycle ;'''

    rectange += r'''
    \draw ''' +\
    f'{x + 0.55*w , y + h/3}' +\
    r''' node [anchor=north] [inner sep=0.75pt] [font=\large] [align=center] {''' + label + r'''};
    '''

    return rectange


def make_labels(jails, scope, x_flip, y_flip):
    labels = [(str(scope+i), str(scope+i+1)) if x_flip else (str(scope+i+1), str(scope+i)) for i in range(0, jails, 2)]
    if y_flip:
        return list(reversed(labels))
    else:
        return labels
    

def make_tensor_labels(jails, x_flip, y_flip):
    labels = [('L' + str(i+1), 'L' + str(i+2)) if x_flip else ('L' + str(i+2), 'L' + str(i+1)) for i in range(0, jails-2, 2)]
    if y_flip:
        return list(reversed(labels))
    else:
        return labels


def translate(label, head=False):
    if label[1:] == '01':
        if not head:
            return '1'
        else:
            return '1'
    elif label[1:] == '02':
        if not head:
            return '2'
        else:
            return '1'
    elif int(label[2:])%2 == 0:
        if not head:
            return '4'
        else:
            return '2'
    else:
        if not head:
            return '3'
        else:
            return '2'


def add_pontoon(pos, w, h, x, y, color):
    delta_x = 35
    delta_y = 35
    if pos == 'top':
        return f'\draw {x+w/2, y-delta_y} node[rectangle, fill={color}!50]' + r'{{\huge P}};' 
    elif pos == 'top left':
        return f'\draw {x-delta_x, y-delta_y} node[rectangle, fill={color}!50]' + r'{{\huge P}};' 
    elif pos == 'left':
        return f'\draw {x-delta_x, y+h/2} node[rectangle, fill={color}!50]' + r'{{\huge P}};' 
    elif pos == 'bottom left':
        return f'\draw {x-delta_x, y+h+delta_y} node[rectangle, fill={color}!50]' + r'{{\huge P}};' 
    elif pos == 'bottom':
        return f'\draw {x+w/2, y+h+delta_y} node[rectangle, fill={color}!50]' + r'{{\huge P}};' 
    elif pos == 'bottom right':
        return f'\draw {x+w+delta_x, y+h+delta_y} node[rectangle, fill={color}!50]' + r'{{\huge P}};' 
    elif pos == 'right':
        return f'\draw {x+w+delta_x, y+h/2} node[rectangle, fill={color}!50]' + r'{{\huge P}};' 
    elif pos == 'top right':
        # latex = f'\draw {x+w/2, y-delta_y} node[rectangle, fill={color}!50]' + r'{{\huge P}};' 
        # latex += f'\draw {x-delta_x, y-delta_y} node[rectangle, fill={color}!50]' + r'{{\huge P}};' 
        # latex += f'\draw {x-delta_x, y+h/2} node[rectangle, fill={color}!50]' + r'{{\huge P}};' 
        # latex += f'\draw {x-delta_x, y+h+delta_y} node[rectangle, fill={color}!50]' + r'{{\huge P}};' 
        # latex += f'\draw {x+w/2, y+h+delta_y} node[rectangle, fill={color}!50]' + r'{{\huge P}};' 
        # latex += f'\draw {x+w+delta_x, y+h+delta_y} node[rectangle, fill={color}!50]' + r'{{\huge P}};' 
        # latex += f'\draw {x+w+delta_x, y+h/2} node[rectangle, fill={color}!50]' + r'{{\huge P}};' 
        # latex +=  f'\draw {x+w+delta_x, y-delta_y} node[rectangle, fill={color}!50]' + r'{{\huge P}};' 
        # latex += f'\draw {x+w+delta_x, y-delta_y} node[rectangle, fill={color}!50]' + r'{{\huge P}};' 
        return f'\draw {x+w+delta_x, y-delta_y} node[rectangle, fill={color}!50]' + r'{{\huge P}};' 
    

def add_cardinals(cardinals, w, h, x, y):
    delta_x = 40
    delta_y = 55

    latex =  f'\draw {x+w/5, y-delta_y} ' +  r'node [anchor=north] [font=\Large' + style['seawolf']['font']['background'] + r'] {\textbf{' + cardinals[0] + r'}};'
    latex +=  f'\draw {x-delta_x, y+h/5} ' +  r'node [anchor=mid, rotate=90] [font=\Large' + style['seawolf']['font']['background'] + r'] {\textbf{' + cardinals[1] + r'}};'
    latex +=  f'\draw {x+4*w/5, y+h+delta_y} ' +  r'node [anchor=south] [font=\Large' + style['seawolf']['font']['background'] + r'] {\textbf{' + cardinals[2] + r'}};'
    latex +=  f'\draw {x+w+delta_x, y+4*h/5} ' +  r'node [anchor=mid, rotate=270] [font=\Large' + style['seawolf']['font']['background'] + r'] {\textbf{' + cardinals[3] + r'}};'
    
    return latex
    

def template(params, style):

    latex = r'''\documentclass[english]{article}''' + '\n'

    for pkg in params['template']['packages']:
        if len(pkg) == 1:
            latex += r'\usepackage{' + pkg[0] + r'}' + '\n'
        else:
            latex += r'\usepackage[' + pkg[0] + r']{' + pkg[1] + r'}' + '\n'

    latex += r'''\usetikzlibrary{intersections}
    \usetikzlibrary{positioning,calc}
    \usetikzlibrary{animations}
    \usetikzlibrary{backgrounds}
    \usetikzlibrary{shapes,snakes}
    \makeatletter
    \renewcommand{\sectionmark}[1]{\markboth{#1}{}}
    \newcommand\BackImage[2][scale=1]{%
    \BgThispage
    \backgroundsetup{
    contents={\includegraphics[#1]{#2}}
    }
    }
    \usepackage{tikz} % para dibujar
    \tikzset{
        use bounding box relative coordinates/.style={
            shift={(current bounding box.south west)},
            x={(current bounding box.south east)},
            y={(current bounding box.north west)}
        },
    }
    \newcommand\invisiblesection[1]{%
    \refstepcounter{section}
    \addcontentsline{toc}{section}{{\thesection}#1}
    \sectionmark{#1}}
    \makeatother'''

    for name, color in style['template']['colors'].items():
        latex += r'\definecolor{' + name + r'}{RGB}{' + color + r'}'

    latex += r'''\newcommand*{\boldcheckmark}{%
    \textpdfrender{
        TextRenderingMode=FillStroke,
        LineWidth=1pt, % half of the line width is outside the normal glyph
    }{\color{checkgreen}\checkmark}%
    }
    \newcommand{\Cross}{$\mathbin{\tikz [x=1.4ex,y=1.4ex,line width=.4ex, darkred] \draw (0,0) -- (1,1) (0,1) -- (1,0);}$}%
    \newcommand*{\boldcross}{%
    \textpdfrender{
        TextRenderingMode=FillStroke,
        LineWidth=1.5pt, % half of the line width is outside the normal glyph
    }{\Cross}%
    }

    \newcommand{\Triangle}{$\mathbin{\tikz [x=1.4ex,y=1.4ex,line width=.4ex, oceangreen] \draw (0,0)--(1,0)--(60:1)--(0,0)--cycle;}$}%
    \newcommand*{\boldtriangle}{%
    \textpdfrender{
        TextRenderingMode=FillStroke,
        LineWidth=1.5pt, % half of the line width is outside the normal glyph
    }{\Triangle}%
    }

    \newcommand{\Cruz}{$\mathbin{\tikz [x=1.8ex,y=1.8ex,line width=.4ex, golden] \draw (0.5,0) -- (0.5,1) (0,0.5) -- (1,0.5);}$}%
    \newcommand*{\boldcruz}{%
    \textpdfrender{
        TextRenderingMode=FillStroke,
        LineWidth=1.5pt, % half of the line width is outside the normal glyph
    }{\Cruz}%
    }

    \newcommand{\MyDiamond}{$\mathbin{\tikz [x=1.4ex, y=1.4ex, line width=.4ex, draw=mortality, fill=mortality] \draw (0,0.5) -- (0.5,1) -- (1,0.5) -- (0.5,0) -- cycle;}$}%
    \newcommand*{\bolddiamond}{%
    \textpdfrender{
        TextRenderingMode=FillStroke,
        LineWidth=1.5pt, % half of the line width is outside the normal glyph
    }{\MyDiamond}%
    }

    
    \pagestyle{fancy}
    \fancyhf{}
	 
    \renewcommand{\headrule}{\color{''' + style["template"]["headrule"] + r'''}\oldheadrule}
    \renewcommand{\headrulewidth}{0pt} 
    \renewcommand{\footrule}{\color{''' + style["template"]["footrule"] + r'''}\oldfootrule}
    \renewcommand{\footrulewidth}{0pt}

    \begin{document}
    \clearpage
    \KOMAoptions{paper=landscape, DIV=last}
    \newgeometry{top=0.2cm, left=0cm, bottom=0.2cm, right=0cm, headsep=0cm}
    \fancyheadoffset{0pt}
    \thispagestyle{empty}
    \begin{figure}[h!]'''
    latex += style['seawolf']['font']['numbers']
    latex += r'''
    \centering
    \scalebox{1}{
    \tikzset{every picture/.style={line width=0.5pt}}        
    \begin{tikzpicture}[x=0.75pt, y=0.75pt, yscale=-1, xscale=1]
    '''
    return latex


def make_seawolf_background(params, center, style, module, pontoon):
    w = params['seawolf']['background']['w']
    h = params['seawolf']['background']['h']
    x = params['seawolf']['background']['x']
    y = params['seawolf']['background']['y']
    net_color = style['seawolf']['net']

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

    if pontoon:
        latex += add_pontoon(center['pontoon'][module], w, h, x, y, style['seawolf']['pontoon'])
        latex += add_cardinals(center['cardinals'][module], w, h, x, y)

    jails = center['jails'][module]
    width = w/(jails/2)
    heigth = h / 2 - 12
    x_space = 2
    y_space = 1.5
    jail_labels = make_labels(jails, center['scopes'][module], center['x_flip'][module], center['y_flip'][module])
    for jail in range(int(jails/2)):
        latex += make_rectangle(x+jail*width+x_space, y+1+6+y_space, width-6-2*x_space, heigth-y_space, jail_labels[jail][0])
        latex += make_rectangle(x+jail*width+x_space, y+h/2+6+y_space, width-6-2*x_space, heigth-y_space, jail_labels[jail][1])
        for i in range(1,6):
            latex += f'''\draw [color={net_color}, draw opacity=0.5 ] [line width=1]'''+ f'''{x+jail*width+width*i/5, y-15} -- {x+jail*width+width*i/5, y+15+h*6/6}; '''
    return latex


def make_seawolf_lat(params, center, style, module, pos):
    w = params['seawolf']['lateral_' + str(pos)]['w']
    h = params['seawolf']['lateral_' + str(pos)]['h']
    x = params['seawolf']['lateral_' + str(pos)]['x']
    y = params['seawolf']['lateral_' + str(pos)]['y']
    hp = h*0.5 + 2
    net_color = style['seawolf']['net']
    jails = center['jails'][module]
    width = w/(jails/2)
    latex = f'''
    \draw {x-23-5, y+h*0/6} -- {x-23-5, y+h*7/7} ;
    \draw {x-23-5, y+h*0/6} -- {x-20-5, y+h*0/6} ;
    \draw {x-23-5, y+h*1/6} -- {x-20-5, y+h*1/6} ;
    \draw {x-23-5, y+h*2/6} -- {x-20-5, y+h*2/6} ;
    \draw {x-23-5, y+h*3/6} -- {x-20-5, y+h*3/6} ;
    \draw {x-23-5, y+h*4/6} -- {x-20-5, y+h*4/6} ;
    \draw {x-23-5, y+h*5/6} -- {x-20-5, y+h*5/6} ;
    \draw {x-23-5, y+h*6/6} -- {x-20-5, y+h*6/6} ;
    \draw {x-27-10, y+h*0/6-5} node [anchor=north][inner sep=0.75pt]  [align=left]''' + r''' {{\normalsize 0}};''' + f'''
    \draw {x-25-10, y+h*1/6-5} node [anchor=north east][inner sep=0.75pt]  [align=left]''' + r''' {{\normalsize 7}};''' + f'''
    \draw {x-25-10, y+h*2/6-5} node [anchor=north east][inner sep=0.75pt]  [align=left]''' + r''' {{\normalsize 14}};''' + f'''
    \draw {x-25-10, y+h*3/6-5} node [anchor=north east][inner sep=0.75pt]  [align=left]''' + r''' {{\normalsize 22}};''' + f'''
    \draw {x-25-10, y+h*4/6-5} node [anchor=north east][inner sep=0.75pt]  [align=left]''' + r''' {{\normalsize 29}};''' + f'''
    \draw {x-25-10, y+h*5/6-5} node [anchor=north east][inner sep=0.75pt]  [align=left]''' + r''' {{\normalsize 36}};''' + f'''
    \draw {x-25-10, y+h*6/6-5} node [anchor=north east][inner sep=0.75pt]  [align=left]''' + r''' {{\normalsize 43}};''' + f'''
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
    \draw {x+w+23+5,y+h*0/6} -- {x+w+23+5, y+h*7/7} ;
    \draw {x+w+23+5,y+h*0/6} -- {x+w+20+5, y+h*0/6} ;
    \draw {x+w+23+5,y+h*1/6} -- {x+w+20+5, y+h*1/6} ;
    \draw {x+w+23+5,y+h*2/6} -- {x+w+20+5, y+h*2/6} ;
    \draw {x+w+23+5,y+h*3/6} -- {x+w+20+5, y+h*3/6} ;
    \draw {x+w+23+5,y+h*4/6} -- {x+w+20+5, y+h*4/6} ;
    \draw {x+w+23+5,y+h*5/6} -- {x+w+20+5, y+h*5/6} ;
    \draw {x+w+23+5,y+h*6/6} -- {x+w+20+5, y+h*6/6} ;
    \draw {x+w+28+10,y+h*0/6-5} node [anchor=north][inner sep=0.75pt]  [align=left]''' + r''' {{\normalsize 0}};''' + f'''
    \draw {x+w+33+10,y+h*1/6-5} node [anchor=north east][inner sep=0.75pt]  [align=left]''' + r''' {{\normalsize 7}};''' + f'''
    \draw {x+w+36+10,y+h*2/6-5} node [anchor=north east][inner sep=0.75pt]  [align=left]''' + r''' {{\normalsize 14}};''' + f'''
    \draw {x+w+36+10,y+h*3/6-5} node [anchor=north east][inner sep=0.75pt]  [align=left]''' + r''' {{\normalsize 22}};''' + f'''
    \draw {x+w+36+10,y+h*4/6-5} node [anchor=north east][inner sep=0.75pt]  [align=left]''' + r''' {{\normalsize 29}};''' + f'''
    \draw {x+w+36+10,y+h*5/6-5} node [anchor=north east][inner sep=0.75pt]  [align=left]''' + r''' {{\normalsize 36}};''' + f'''
    \draw {x+w+36+10,y+h*6/6-5} node [anchor=north east][inner sep=0.75pt]  [align=left]''' + r''' {{\normalsize 43}};'''

    jail_labels = make_labels(jails, center['scopes'][module], center['x_flip'][module], center['y_flip'][module])
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


def make_seawolf_head(params, center, style, module, pos):
    w = params['seawolf']['head_' + str(pos)]['w']
    h = params['seawolf']['head_' + str(pos)]['h']
    x = params['seawolf']['head_' + str(pos)]['x']
    y = params['seawolf']['head_' + str(pos)]['y']
    hp = h*0.5 + 2
    net_color = style['seawolf']['net']
    jails = center['jails'][module]
    latex = f'''
    \draw {x-5*w/50, y+h*0/6} -- {x-4*w/50, y+h*0/6} ;
    \draw {x-5*w/50, y+h*1/6} -- {x-4*w/50, y+h*1/6} ;
    \draw {x-5*w/50, y+h*2/6} -- {x-4*w/50, y+h*2/6} ;
    \draw {x-5*w/50, y+h*3/6} -- {x-4*w/50, y+h*3/6} ;
    \draw {x-5*w/50, y+h*0/6} -- {x-5*w/50, y+h*7/7} ;
    \draw {x-5*w/50, y+h*4/6} -- {x-4*w/50, y+h*4/6} ;
    \draw {x-5*w/50, y+h*5/6} -- {x-4*w/50, y+h*5/6} ;
    \draw {x-5*w/50, y+h*6/6} -- {x-4*w/50, y+h*6/6} ;
    \draw {x-6*w/50, y+h*0/6-w/50} node [anchor=north][inner sep=0.75pt]  [align=left]''' + r''' {{\huge 0}};''' + f'''
    \draw {x-6*w/50, y+h*1/6-w/50} node [anchor=north east][inner sep=0.75pt]  [align=left]''' + r''' {{\huge 7}};''' + f'''
    \draw {x-6*w/50, y+h*2/6-w/50} node [anchor=north east][inner sep=0.75pt]  [align=left]''' + r''' {{\huge 14}};''' + f'''
    \draw {x-6*w/50, y+h*3/6-w/50} node [anchor=north east][inner sep=0.75pt]  [align=left]''' + r''' {{\huge 22}};''' + f'''
    \draw {x-6*w/50, y+h*4/6-w/50} node [anchor=north east][inner sep=0.75pt]  [align=left]''' + r''' {{\huge 29}};''' + f'''
    \draw {x-6*w/50, y+h*5/6-w/50} node [anchor=north east][inner sep=0.75pt]  [align=left]''' + r''' {{\huge 36}};''' + f'''
    \draw {x-6*w/50, y+h*6/6-w/50} node [anchor=north east][inner sep=0.75pt]  [align=left]''' + r''' {{\huge 43}};''' + f'''
    \draw {x+w+5*w/50, y+h*0/6} -- {x+w+5*w/50, y+h*7/7} ;
    \draw {x+w+5*w/50, y+h*0/6} -- {x+w+4*w/50, y+h*0/6} ;
    \draw {x+w+5*w/50, y+h*1/6} -- {x+w+4*w/50, y+h*1/6} ;
    \draw {x+w+5*w/50, y+h*2/6} -- {x+w+4*w/50, y+h*2/6} ;
    \draw {x+w+5*w/50, y+h*3/6} -- {x+w+4*w/50, y+h*3/6} ;
    \draw {x+w+5*w/50, y+h*4/6} -- {x+w+4*w/50, y+h*4/6} ;
    \draw {x+w+5*w/50, y+h*5/6} -- {x+w+4*w/50, y+h*5/6} ;
    \draw {x+w+5*w/50, y+h*6/6} -- {x+w+4*w/50, y+h*6/6} ;
    \draw {x+w+6*w/50, y+h*0/6-w/50} node [anchor=north][inner sep=0.75pt]  [align=right]''' + r''' {{\huge 0}};''' + f'''
    \draw {x+w+6*w/50, y+h*1/6-w/50} node [anchor=north west][inner sep=0.75pt]  [align=right]''' + r''' {{\huge 7}};''' + f'''
    \draw {x+w+6*w/50, y+h*2/6-w/50} node [anchor=north west][inner sep=0.75pt]  [align=right]''' + r''' {{\huge 14}};''' + f'''
    \draw {x+w+6*w/50, y+h*3/6-w/50} node [anchor=north west][inner sep=0.75pt]  [align=right]''' + r''' {{\huge 22}};''' + f'''
    \draw {x+w+6*w/50, y+h*4/6-w/50} node [anchor=north west][inner sep=0.75pt]  [align=right]''' + r''' {{\huge 29}};''' + f'''
    \draw {x+w+6*w/50, y+h*5/6-w/50} node [anchor=north west][inner sep=0.75pt]  [align=right]''' + r''' {{\huge 36}};''' + f'''
    \draw {x+w+6*w/50, y+h*6/6-w/50} node [anchor=north west][inner sep=0.75pt]  [align=right]''' + r''' {{\huge 43}};'''

    latex += f'''
    \draw [color={net_color}, draw opacity=0.5 ] [line width=1]'''+ f'''{x, y} -- {x-3*w/50, y+h*1/6} -- {x-3*w/50, y+h*6/6} -- {x+w+3*w/50, y+h*6/6} -- {x+w+3*w/50, y+h*1/6} -- {x+w, y};''' + f'''
    \draw [color={net_color}, draw opacity=0.5 ] [line width=1]'''+ f'''{x-3*w/50, y+h*1/6} -- {x+w+3*w/50, y+h*1/6}; ''' + f'''
    \draw [color={net_color}, draw opacity=0.5 ] [line width=1]'''+ f'''{x-3*w/50, y+h*2/6} -- {x+w+3*w/50, y+h*2/6}; ''' + f'''
    \draw [color={net_color}, draw opacity=0.5 ] [line width=1]'''+ f'''{x-3*w/50, y+h*3/6} -- {x+w+3*w/50, y+h*3/6}; ''' + f'''
    \draw [color={net_color}, draw opacity=0.5 ] [line width=1]'''+ f'''{x-3*w/50, y+h*4/6} -- {x+w+3*w/50, y+h*4/6}; ''' + f'''
    \draw [color={net_color}, draw opacity=0.5 ] [line width=1]'''+ f'''{x-3*w/50, y+h*5/6} -- {x+w+3*w/50, y+h*5/6}; ''' + f'''
    \draw [color={net_color}, draw opacity=0.5 ] [line width=1]'''+ f'''{x, y} -- {x, y+h*6/6}; ''' #+ f'''
    width = w/2
    jail_labels = make_labels(jails, center['scopes'][module], center['x_flip'][module], center['y_flip'][module])
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

    latex += f'\draw {x, y-1.5*h/10}' + r'node [anchor=north] [inner sep=0.75pt] [font=\large] [align=center] {\huge LE' + label1 + r'};'
    latex += f'\draw {x+w, y-1.5*h/10}' + r'node [anchor=north] [inner sep=0.75pt] [font=\large] [align=center] {\huge LE' + label2 + r'};'
    return latex


def make_seawolf_sep(params, center, style, module):
    w = params['seawolf']['separator']['w']
    h = params['seawolf']['separator']['h']
    x = params['seawolf']['separator']['x']
    y = params['seawolf']['separator']['y']
    hp = h*0.5 + 2
    net_color = style['seawolf']['net']
    jails = center['jails'][module]
    latex = f'''
    \draw {x-5*w/50, y+h*0/6} -- {x-4*w/50, y+h*0/6} ;
    \draw {x-5*w/50, y+h*1/6} -- {x-4*w/50, y+h*1/6} ;
    \draw {x-5*w/50, y+h*2/6} -- {x-4*w/50, y+h*2/6} ;
    \draw {x-5*w/50, y+h*3/6} -- {x-4*w/50, y+h*3/6} ;
    \draw {x-5*w/50, y+h*0/6} -- {x-5*w/50, y+h*7/7} ;
    \draw {x-5*w/50, y+h*4/6} -- {x-4*w/50, y+h*4/6} ;
    \draw {x-5*w/50, y+h*5/6} -- {x-4*w/50, y+h*5/6} ;
    \draw {x-5*w/50, y+h*6/6} -- {x-4*w/50, y+h*6/6} ;
    \draw {x-6*w/50, y+h*0/6-w/50} node [anchor=north][inner sep=0.75pt]  [align=left]''' + r''' {{\huge 0}};''' + f'''
    \draw {x-6*w/50, y+h*1/6-w/50} node [anchor=north east][inner sep=0.75pt]  [align=left]''' + r''' {{\huge 7}};''' + f'''
    \draw {x-6*w/50, y+h*2/6-w/50} node [anchor=north east][inner sep=0.75pt]  [align=left]''' + r''' {{\huge 14}};''' + f'''
    \draw {x-6*w/50, y+h*3/6-w/50} node [anchor=north east][inner sep=0.75pt]  [align=left]''' + r''' {{\huge 22}};''' + f'''
    \draw {x-6*w/50, y+h*4/6-w/50} node [anchor=north east][inner sep=0.75pt]  [align=left]''' + r''' {{\huge 29}};''' + f'''
    \draw {x-6*w/50, y+h*5/6-w/50} node [anchor=north east][inner sep=0.75pt]  [align=left]''' + r''' {{\huge 36}};''' + f'''
    \draw {x-6*w/50, y+h*6/6-w/50} node [anchor=north east][inner sep=0.75pt]  [align=left]''' + r''' {{\huge 43}};''' + f'''
    \draw {x+w+5*w/50, y+h*0/6} -- {x+w+5*w/50, y+h*7/7} ;
    \draw {x+w+5*w/50, y+h*0/6} -- {x+w+4*w/50, y+h*0/6} ;
    \draw {x+w+5*w/50, y+h*1/6} -- {x+w+4*w/50, y+h*1/6} ;
    \draw {x+w+5*w/50, y+h*2/6} -- {x+w+4*w/50, y+h*2/6} ;
    \draw {x+w+5*w/50, y+h*3/6} -- {x+w+4*w/50, y+h*3/6} ;
    \draw {x+w+5*w/50, y+h*4/6} -- {x+w+4*w/50, y+h*4/6} ;
    \draw {x+w+5*w/50, y+h*5/6} -- {x+w+4*w/50, y+h*5/6} ;
    \draw {x+w+5*w/50, y+h*6/6} -- {x+w+4*w/50, y+h*6/6} ;
    \draw {x+w+6*w/50, y+h*0/6-w/50} node [anchor=north][inner sep=0.75pt]  [align=right]''' + r''' {{\huge 0}};''' + f'''
    \draw {x+w+6*w/50, y+h*1/6-w/50} node [anchor=north west][inner sep=0.75pt]  [align=right]''' + r''' {{\huge 7}};''' + f'''
    \draw {x+w+6*w/50, y+h*2/6-w/50} node [anchor=north west][inner sep=0.75pt]  [align=right]''' + r''' {{\huge 14}};''' + f'''
    \draw {x+w+6*w/50, y+h*3/6-w/50} node [anchor=north west][inner sep=0.75pt]  [align=right]''' + r''' {{\huge 22}};''' + f'''
    \draw {x+w+6*w/50, y+h*4/6-w/50} node [anchor=north west][inner sep=0.75pt]  [align=right]''' + r''' {{\huge 29}};''' + f'''
    \draw {x+w+6*w/50, y+h*5/6-w/50} node [anchor=north west][inner sep=0.75pt]  [align=right]''' + r''' {{\huge 36}};''' + f'''
    \draw {x+w+6*w/50, y+h*6/6-w/50} node [anchor=north west][inner sep=0.75pt]  [align=right]''' + r''' {{\huge 43}};'''

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


def make_fishbowl_background(params, style):
    w = params['fishbowl']['background']['w']
    h = params['fishbowl']['background']['h']
    x = params['fishbowl']['background']['x']
    y = params['fishbowl']['background']['y']
    color = style['fishbowl']['points']
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

    latex += f'''\draw {x+15, y-30} ''' + r'''node [anchor=north] [align=center] [font=''' + style['fishbowl']['font']['background'] + r'''] {\textbf{\huge Frontal}};''' 
    # latex += f'''\draw {x+w+15, y+h/2} ''' + r'''node [anchor=north] [rotate=-270] [align=center] {\textbf{Pared Oeste}};''' 
    # latex += f'''\draw {x-30, y+h/2} ''' + r'''node [anchor=north] [rotate=-270] [align=center] {\textbf{Pared Este}};''' 
    latex += f'''\draw {x+w-15, y+h+10} ''' + r'''node [anchor=north] [align=center] [font=''' + style['fishbowl']['font']['background'] + r''']{\textbf{\huge Distal}};''' 

    return latex


def make_fishbowl_lat(params, style):
    w = params['fishbowl']["frontal"]['w']
    h = params['fishbowl']["frontal"]['h']
    x = params['fishbowl']["frontal"]['x']
    y = params['fishbowl']["frontal"]['y']
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
    return latex


def make_tensor_mooring(w, h, x, y):
    buoy_color = style['tensors']['buoy']
    tensor_color = style['tensors']['tensor']


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


def make_tensor_system(params, center, style, module):
    w = params['tensors']['system']['w']
    h = params['tensors']['system']['h']
    x = params['tensors']['system']['x']
    y = params['tensors']['system']['y']
    tensor_color = style['tensors']['tensor']
    net_color = style['tensors']['net']

    latex = f'''
    \draw {x, y} -- {x + w, y} -- {x + w, y + h} -- {x, y + h} -- cycle ;'''

    latex += f'''
    \draw [color={net_color}, draw opacity=0.5 ] [line width=1]'''+ f'''{x-15, y-15} -- {x-15, y+h+15} -- {x+w+15, y+h+15} -- {x+w+15, y-15} -- cycle;'''
    latex += f'''\draw [color={net_color}, draw opacity=0.5 ] [line width=1]'''+ f'''{x-15, y-15} -- {x, y}; '''
    latex += f'''\draw [color={net_color}, draw opacity=0.5 ] [line width=1]'''+ f'''{x-15, y+h+15} -- {x, y+h}; '''
    latex += f'''\draw [color={net_color}, draw opacity=0.5 ] [line width=1]'''+ f'''{x+w+15, y-15} -- {x+w, y}; '''
    latex += f'''\draw [color={net_color}, draw opacity=0.5 ] [line width=1]'''+ f'''{x+w+15, y+h+15} -- {x+w, y+h}; '''

    latex += f'''\draw [color={net_color}, draw opacity=0.5 ] [line width=1]'''+ f'''{x, y-15} -- {x,y}; ''' 
    latex += f'''\draw [color={net_color}, draw opacity=0.5 ] [line width=1]'''+ f'''{x, y+h+15} -- {x, y+h}; ''' 
        
    jails = center['jails'][module]
    width = w/(jails/2)

    heigth = h / 2 - 12
    x_space = 2
    y_space = 1.5
    jail_labels = make_labels(jails, center['scopes'][module], center['x_flip'][module], center['y_flip'][module])
    tensor_labels = make_tensor_labels(jails, center['x_flip'][module], center['y_flip'][module])
    for jail in range(int(jails/2)):
        latex += make_rectangle(x+jail*width+x_space, y+1+6+y_space, width-6-2*x_space, heigth-y_space, jail_labels[jail][0])
        latex += make_rectangle(x+jail*width+x_space, y+h/2+6+y_space, width-6-2*x_space, heigth-y_space, jail_labels[jail][1])
        for i in range(1, 6):
            latex += f'''\draw [color={net_color}, draw opacity=0.5 ] [line width=1]'''+ f'''{x+jail*width+width*i/5, y-15} -- {x+jail*width+width*i/5,y}; ''' 
            latex += f'''\draw [color={net_color}, draw opacity=0.5 ] [line width=1]'''+ f'''{x+jail*width+width*i/5, y+h} -- {x+jail*width+width*i/5,y+15+h}; '''
            if i == 2 or i == 3: 
                latex += f'''\draw [fill={style['tensors']['dots']}, fill opacity=1 ]''' + f'''{x+jail*width+width*i/5, y+1} circle ({0.005*w});''' 
                latex += f'''\draw [fill={style['tensors']['dots']}, fill opacity=1 ]''' + f'''{x+jail*width+width*i/5, y+h/2} circle ({0.005*w});''' 
                latex += f'''\draw [fill={style['tensors']['dots']}, fill opacity=1 ]''' + f'''{x+jail*width+width*i/5, y+h-1} circle ({0.005*w});''' 
            elif i == 5 and jail != int(jails/2)-1:
                latex += f'''\draw [color={tensor_color}, draw opacity=0.5 ] [line width=1]'''+ f'''{x+jail*width+width*i/5, y-15} -- {x+jail*width+width*i/5,y-60}; ''' 
                latex += f'''\draw [color={tensor_color}, draw opacity=0.5 ] [line width=1]'''+ f'''{x+jail*width+width*(i-2)/5, y-15} -- {x+jail*width+width*i/5,y-60}; ''' 
                latex += f'''\draw [color={tensor_color}, draw opacity=0.5 ] [line width=1]'''+ f'''{x+(jail+1)*width+width*2/5, y-15} -- {x+jail*width+width*i/5,y-60}; ''' 
                latex += f'''\draw [fill={style['tensors']['buoy']}, fill opacity=1 ]''' + f'''{x+jail*width+width*i/5, y-60} circle ({0.005*w});''' 
                latex += f'''\draw {x+jail*width+width*i/5, y-70} ''' + r'''node [anchor=south] [font=\large''' + style['tensors']['font']['labels'] + r'''] [align=center] {''' +  tensor_labels[jail][0] + r'''};''' 
                latex += make_tensor_mooring(0.8*width, h, x+jail*width+width*i/5, y-70-1.5*h)

                latex += f'''\draw [color={tensor_color}, draw opacity=0.5 ] [line width=1]'''+ f'''{x+jail*width+width*i/5, y+h+15} -- {x+jail*width+width*i/5,y+h+60}; ''' 
                latex += f'''\draw [color={tensor_color}, draw opacity=0.5 ] [line width=1]'''+ f'''{x+jail*width+width*(i-2)/5, y+h+15} -- {x+jail*width+width*i/5,y+h+60}; ''' 
                latex += f'''\draw [color={tensor_color}, draw opacity=0.5 ] [line width=1]'''+ f'''{x+(jail+1)*width+width*2/5, y+h+15} -- {x+jail*width+width*i/5,y+h+60}; ''' 
                latex += f'''\draw [fill={style['tensors']['buoy']}, fill opacity=1 ]''' + f'''{x+jail*width+width*i/5, y+h+60} circle ({0.005*w});''' 
                latex += f'''\draw {x+jail*width+width*i/5, y+h+70} ''' + r'''node [anchor=north] [font=\large''' + style['tensors']['font']['labels'] + r'''] [align=center] {''' + tensor_labels[jail][1] + r'''};''' 
                latex += make_tensor_mooring(0.8*width, h, x+jail*width+width*i/5, y+h+70+0.5*h)


    latex += f'''\draw [color={tensor_color}, draw opacity=0.5 ] [line width=1]'''+ f'''{x, y-15} -- {x,y-60}; ''' 
    latex += f'''\draw [color={tensor_color}, draw opacity=0.5 ] [line width=1]'''+ f'''{x-15, y-15} -- {x,y-60}; ''' 
    latex += f'''\draw [color={tensor_color}, draw opacity=0.5 ] [line width=1]'''+ f'''{x+width*2/5, y-15} -- {x,y-60}; ''' 
    latex += f'''\draw [fill={style['tensors']['buoy']}, fill opacity=1 ]''' + f'''{x, y-60} circle ({0.005*w});''' 
    latex += f'''\draw {x, y-70} ''' + r'''node [anchor=south] [font=\large''' + style['tensors']['font']['labels'] + r'''] [align=center] {LE''' + translate(jail_labels[0][0]) + r'};'
    latex += make_tensor_mooring(0.1*w, h, x, y-70-1.5*h)

    latex += f'''\draw [color={tensor_color}, draw opacity=0.5 ] [line width=1]'''+ f'''{x+w, y-15} -- {x+w, y-60}; ''' 
    latex += f'''\draw [color={tensor_color}, draw opacity=0.5 ] [line width=1]'''+ f'''{x+w+15, y-15} -- {x+w, y-60}; ''' 
    latex += f'''\draw [color={tensor_color}, draw opacity=0.5 ] [line width=1]'''+ f'''{x+w-width*2/5, y-15} -- {x+w, y-60}; ''' 
    latex += f'''\draw [fill={style['tensors']['buoy']}, fill opacity=1 ]''' + f'''{x+w, y-60} circle ({0.005*w});''' 
    latex += f'''\draw {x+w, y-70} ''' + r'''node [anchor=south] [font=\large''' + style['tensors']['font']['labels'] + r'''] [align=center] {LE''' + translate(jail_labels[-1][0]) + r'};'
    latex += make_tensor_mooring(0.1*w, h, x+w, y-70-1.5*h)

    latex += f'''\draw [color={tensor_color}, draw opacity=0.5 ] [line width=1]'''+ f'''{x, y+h+15} -- {x,y+h+60}; ''' 
    latex += f'''\draw [color={tensor_color}, draw opacity=0.5 ] [line width=1]'''+ f'''{x-15, y+h+15} -- {x,y+h+60}; ''' 
    latex += f'''\draw [color={tensor_color}, draw opacity=0.5 ] [line width=1]'''+ f'''{x+width*2/5, y+h+15} -- {x,y+h+60}; ''' 
    latex += f'''\draw [fill={style['tensors']['buoy']}, fill opacity=1 ]''' + f'''{x, y+h+60} circle ({0.005*w});''' 
    latex += f'''\draw {x, y+h+70} ''' + r'''node [anchor=north] [font=\large''' + style['tensors']['font']['labels'] + r'''] [align=center] {LE''' + translate(jail_labels[0][1]) + r'};'
    latex += make_tensor_mooring(0.1*w, h, x, y+h+70+0.5*h)

    latex += f'''\draw [color={tensor_color}, draw opacity=0.5 ] [line width=1]'''+ f'''{x+w, y+h+15} -- {x+w, y+h+60}; ''' 
    latex += f'''\draw [color={tensor_color}, draw opacity=0.5 ] [line width=1]'''+ f'''{x+w+15, y+h+15} -- {x+w, y+h+60}; ''' 
    latex += f'''\draw [color={tensor_color}, draw opacity=0.5 ] [line width=1]'''+ f'''{x+w-width*2/5, y+h+15} -- {x+w, y+h+60}; ''' 
    latex += f'''\draw [fill={style['tensors']['buoy']}, fill opacity=1 ]''' + f'''{x+w, y+h+60} circle ({0.005*w});''' 
    latex += f'''\draw {x+w, y+h+70} ''' + r'''node [anchor=north] [font=\large''' + style['tensors']['font']['labels'] + r'''] [align=center] {LE''' + translate(jail_labels[-1][1]) + r'};'
    latex += make_tensor_mooring(0.1*w, h, x+w, y+h+70+0.5*h)
        
    for i in range(11):
        latex += f'''\draw [color={net_color}, draw opacity=0.5 ] [line width=1]'''+ f'''{x-15, y+h*i/10} -- {x, y+h*i/10}; '''
        latex += f'''\draw [color={net_color}, draw opacity=0.5 ] [line width=1]'''+ f'''{x+w, y+h*i/10} -- {x+w+15, y+h*i/10}; '''
        if i == 0 or i == 10:
            pass
        elif i%2 == 0 or i == 5:
            latex += f'''\draw [fill={style['tensors']['dots']}, fill opacity=1 ]''' + f'''{x+1, y+h*i/10} circle ({0.005*w});''' 
            latex += f'''\draw [fill={style['tensors']['dots']}, fill opacity=1 ]''' + f'''{x+w-1, y+h*i/10} circle ({0.005*w});''' 

        latex += f'''\draw [fill={style['tensors']['dots']}, fill opacity=1 ]''' + f'''{x+2, y+2} circle ({0.005*w});''' 
        latex += f'''\draw [fill={style['tensors']['dots']}, fill opacity=1 ]''' + f'''{x+w-2, y+2} circle ({0.005*w});''' 
        latex += f'''\draw [fill={style['tensors']['dots']}, fill opacity=1 ]''' + f'''{x+2, y+h-2} circle ({0.005*w});''' 
        latex += f'''\draw [fill={style['tensors']['dots']}, fill opacity=1 ]''' + f'''{x+w-2, y+h-2} circle ({0.005*w});''' 
    
    latex += f'''\draw [color={tensor_color}, draw opacity=0.5 ] [line width=1]'''+ f'''{x-15, y} -- {x-60, y}; ''' 
    latex += f'''\draw [color={tensor_color}, draw opacity=0.5 ] [line width=1]'''+ f'''{x-15, y-15} -- {x-60, y}; ''' 
    latex += f'''\draw [color={tensor_color}, draw opacity=0.5 ] [line width=1]'''+ f'''{x-15, y+h*2/10} -- {x-60, y}; ''' 
    latex += f'''\draw [fill={style['tensors']['buoy']}, fill opacity=1 ]''' + f'''{x-60, y} circle ({0.005*w});''' 
    latex += f'''\draw {x-70, y} ''' + r'''node [anchor=south] [font=\large''' + style['tensors']['font']['labels'] + r'''] [align=center] {CE''' + translate(jail_labels[0][0]) + r'};'
    latex += make_tensor_mooring(0.1*w, h, x-70-(0.1*w)/2, y-70-1*h)

    latex += f'''\draw [color={tensor_color}, draw opacity=0.5 ] [line width=1]'''+ f'''{x+w+15, y} -- {x+w+60, y}; ''' 
    latex += f'''\draw [color={tensor_color}, draw opacity=0.5 ] [line width=1]'''+ f'''{x+w+15, y-15} -- {x+w+60, y}; ''' 
    latex += f'''\draw [color={tensor_color}, draw opacity=0.5 ] [line width=1]'''+ f'''{x+w+15, y+h*2/10} -- {x+w+60, y}; ''' 
    latex += f'''\draw [fill={style['tensors']['buoy']}, fill opacity=1 ]''' + f'''{x+w+60, y} circle ({0.005*w});''' 
    latex += f'''\draw {x+w+70, y} ''' + r'''node [anchor=south] [font=\large''' + style['tensors']['font']['labels'] + r'''] [align=center] {CE''' + translate(jail_labels[-1][0]) + r'};'
    latex += make_tensor_mooring(0.1*w, h, x+w+70+0.6*(0.1*w), y-70-1*h)

    latex += f'''\draw [color={tensor_color}, draw opacity=0.5 ] [line width=1]'''+ f'''{x-15, y+h} -- {x-60, y+h}; ''' 
    latex += f'''\draw [color={tensor_color}, draw opacity=0.5 ] [line width=1]'''+ f'''{x-15, y+h+15} -- {x-60, y+h}; ''' 
    latex += f'''\draw [color={tensor_color}, draw opacity=0.5 ] [line width=1]'''+ f'''{x-15, y+h-h*2/10} -- {x-60, y+h}; ''' 
    latex += f'''\draw [fill={style['tensors']['buoy']}, fill opacity=1 ]''' + f'''{x-60, y+h} circle ({0.005*w});''' 
    latex += f'''\draw {x-70, y+h} ''' + r'''node [anchor=north] [font=\large''' + style['tensors']['font']['labels'] + r'''] [align=center] {CE''' + translate(jail_labels[0][1]) + r'};'
    latex += make_tensor_mooring(0.1*w, h, x-70-(0.1*w)/2, y+h+70+0*h)

    latex += f'''\draw [color={tensor_color}, draw opacity=0.5 ] [line width=1]'''+ f'''{x+w+15, y+h} -- {x+w+60, y+h}; ''' 
    latex += f'''\draw [color={tensor_color}, draw opacity=0.5 ] [line width=1]'''+ f'''{x+w+15, y+h+15} -- {x+w+60, y+h}; ''' 
    latex += f'''\draw [color={tensor_color}, draw opacity=0.5 ] [line width=1]'''+ f'''{x+w+15, y+h-h*2/10} -- {x+w+60, y+h}; ''' 
    latex += f'''\draw [fill={style['tensors']['buoy']}, fill opacity=1 ]''' + f'''{x+w+60, y+h} circle ({0.005*w});''' 
    latex += f'''\draw {x+w+70, y+h} ''' + r'''node [anchor=north] [font=\large''' + style['tensors']['font']['labels'] + r'''] [align=center] {CE''' + translate(jail_labels[-1][1]) + r'};'
    latex += make_tensor_mooring(0.1*w, h, x+w+70+0.6*(0.1*w), y+h+70+0*h)

    latex += f'''\draw [color={tensor_color}, draw opacity=0.5 ] [line width=1]'''+ f'''{x-15, y+h/2} -- {x-60, y+h/2}; ''' 
    latex += f'''\draw [color={tensor_color}, draw opacity=0.5 ] [line width=1]'''+ f'''{x-15, y+h/2-h/10} -- {x-60, y+h/2}; ''' 
    latex += f'''\draw [color={tensor_color}, draw opacity=0.5 ] [line width=1]'''+ f'''{x-15, y+h/2+h/10} -- {x-60, y+h/2}; ''' 
    latex += f'''\draw [fill={style['tensors']['buoy']}, fill opacity=1 ]''' + f'''{x-60, y+h/2} circle ({0.005*w});''' 
    latex += f'''\draw {x-70, y+h/2} ''' + r'''node [anchor=south] [font=\large''' + style['tensors']['font']['labels'] + r'''] [align=center] {C''' + translate(jail_labels[0][0], True) + r'};'
    latex += make_tensor_mooring(0.1*w, h, x-70-(0.1*w)/2-20, y)

    latex += f'''\draw [color={tensor_color}, draw opacity=0.5 ] [line width=1]'''+ f'''{x+w+15, y+h/2} -- {x+w+60, y+h/2}; ''' 
    latex += f'''\draw [color={tensor_color}, draw opacity=0.5 ] [line width=1]'''+ f'''{x+w+15, y+h/2-h/10} -- {x+w+60, y+h/2}; ''' 
    latex += f'''\draw [color={tensor_color}, draw opacity=0.5 ] [line width=1]'''+ f'''{x+w+15, y+h/2+h/10} -- {x+w+60, y+h/2}; ''' 
    latex += f'''\draw [fill={style['tensors']['buoy']}, fill opacity=1 ]''' + f'''{x+w+60, y+h/2} circle ({0.005*w});''' 
    latex += f'''\draw {x+w+70, y+h/2} ''' + r'''node [anchor=north] [font=\large''' + style['tensors']['font']['labels'] + r'''] [align=center] {C''' + translate(jail_labels[-1][0],  True) + r'};'
    latex += make_tensor_mooring(0.1*w, h, x+w+70+0.6*(0.1*w)+20, y)
    return latex


def compile(latex):
    BASE_DIR = Path(__file__).resolve().parent.parent
    file = os.path.join(BASE_DIR, 'static', 'imgs', 'assets', 'temp.tex')
    path = os.path.join(BASE_DIR, 'static', 'imgs', 'assets')
    with open(file, 'w', encoding='utf-8') as tex_file:
            tex_file.write(latex)
        
    output_filename = 'temp'
    os.system(f"pdflatex -output-directory '{path}' -jobname='{output_filename}' '{file}'")
    os.system(f"pdflatex -output-directory '{path}' -jobname='{output_filename}' '{file}'")


def background(params, centers, style):
    BASE_DIR = Path(__file__).resolve().parent.parent
    path = os.path.join(BASE_DIR, 'static', 'imgs', 'assets')

    params['seawolf']['background']['w'] = 550*1.5
    params['seawolf']['background']['h'] = 200*1.5
    for center_name, center in centers.items():
        for module in range(center['modules']):
            module = str(module)
            # name = str(int(center['x_flip'][module])) + str(int(center['y_flip'][module])) + str(int(center['double'][module])) + f"_{str(center['jails'][module])}"
            name = center_name.replace(' ', '') + f'_{module}'
            latex = template(params, style)
            latex += make_seawolf_background(params, center, style, module, True)
            latex += r'''
            \end{tikzpicture}
            }
            \end{figure}
            \end{document}'''
            compile(latex)
            pages = convert_from_path(os.path.join(path, 'temp.pdf'))
            for page in pages:
                # path = f'auto_report/dark-ignore/plantillas/background/{name}.png'
                # path = os.path.join(path, 'background', name + '.png')
                page.save(os.path.join(path, 'background', name + '.png'), 'PNG') 
            crop(os.path.join(path, 'background', name + '.png'))


def lateral(params, centers, style):
    BASE_DIR = Path(__file__).resolve().parent.parent
    path = os.path.join(BASE_DIR, 'static', 'imgs', 'assets')

    params['seawolf']['lateral_0']['w'] = 550*1.7
    params['seawolf']['lateral_0']['h'] = 100*1.7
    params['seawolf']['lateral_0']['y'] = 370*1.7
    params['seawolf']['lateral_1']['w'] = 550*1.7
    params['seawolf']['lateral_1']['h'] = 100*1.7
    params['seawolf']['lateral_1']['y'] = 490*1.7
    for center_name, center in centers.items():
        for module in range(center['modules']):
            module = str(module)
            # name = str(int(center['x_flip'][module])) + str(int(center['y_flip'][module])) + f"_{str(center['jails'][module])}"
            name = center_name.replace(' ', '') + f'_{module}'
            latex = template(params, style)
            latex += make_seawolf_lat(params, center, style, module, 0)
            latex += make_seawolf_lat(params, center, style, module, 1)
            latex += r'''
            \end{tikzpicture}
            }
            \end{figure}
            \end{document}'''
            compile(latex)
            pages = convert_from_path(os.path.join(path, 'temp.pdf'))
            for page in pages:
                page.save(os.path.join(path, 'lateral', name + '.png'), 'PNG') 
            crop(os.path.join(path, 'lateral', name + '.png'))


def head(params, centers, style):
    BASE_DIR = Path(__file__).resolve().parent.parent
    path = os.path.join(BASE_DIR, 'static', 'imgs', 'assets')

    params['seawolf']['head_0']['w'] = 250*2.5
    params['seawolf']['head_0']['h'] = 130*2.5
    params['seawolf']['head_0']['y'] = 80*2.5
    params['seawolf']['head_1']['w'] = 250*2.5
    params['seawolf']['head_1']['h'] = 130*2.5
    params['seawolf']['head_1']['y'] = 250*2.5
    center = centers['CATALINA']
    combination_params = {
        "00": {
            "x_flip": False,
            "y_flip": False
        }, 
        "10": {
            "x_flip": True,
            "y_flip": False
        },
        "01": {
            "x_flip": False,
            "y_flip": True
        },
        "11": {
            "x_flip": True,
            "y_flip": True
        }
    }
    for combination in ['00', '10', '01', '11']:
        module = "0"
        center['x_flip'][module] = combination_params[combination]['x_flip']
        center['y_flip'][module] = combination_params[combination]['y_flip']
        module = "0"
        latex = template(params, style)
        latex += make_seawolf_head(params, center, style, module, 0)
        latex += make_seawolf_head(params, center, style, module, 1)
        latex += r'''
        \end{tikzpicture}
        }
        \end{figure}
        \end{document}'''
        compile(latex)
        pages = convert_from_path(os.path.join(path, 'temp.pdf'))
        for page in pages:
            # path = r'auto_report\dark-ignore\plantillas\seawolf_head_' + combination + str(int(center['double'][module])) + f'.png'
            page.save(os.path.join(path, 'fixed', 'seawolf_head_' + combination + str(int(center['double'][module])) + '.png'), 'PNG') 
        crop(os.path.join(path, 'fixed', 'seawolf_head_' + combination + str(int(center['double'][module])) + '.png'))


def separator(params, centers, style):
    BASE_DIR = Path(__file__).resolve().parent.parent
    path = os.path.join(BASE_DIR, 'static', 'imgs', 'assets')

    params['seawolf']['separator']['w'] = 250*3.1
    params['seawolf']['separator']['h'] = 130*3.1
    for center_name, center in centers.items():
        for module in range(center['modules']):
            module = str(module)
            latex = template(params, style)
            latex += make_seawolf_sep(params, center, style, module)
            latex += r'''
            \end{tikzpicture}
            }
            \end{figure}
            \end{document}'''
            compile(latex)
            pages = convert_from_path(os.path.join(path, 'temp.pdf'))
            for page in pages:
                # path = r'auto_report\dark-ignore\plantillas\seawolf_sep' + str(int(center['double'][module])) + '.png'
                page.save(os.path.join(path, 'fixed', 'seawolf_sep' + str(int(center['double'][module])) + '.png'), 'PNG') 
            crop(os.path.join(path, 'fixed', 'seawolf_sep' + str(int(center['double'][module])) + '.png'))
            break
        break


def pecera_background(params, style):
    BASE_DIR = Path(__file__).resolve().parent.parent
    path = os.path.join(BASE_DIR, 'static', 'imgs', 'assets')

    params['fishbowl']['background']['w'] = 350*2
    params['fishbowl']['background']['h'] = 350*2
    latex = template(params, style)
    latex += make_fishbowl_background(params, style)
    latex += r'''
    \end{tikzpicture}
    }
    \end{figure}
    \end{document}'''
    compile(latex)
    pages = convert_from_path(os.path.join(path, 'temp.pdf'))
    for page in pages:
        # path = os.path.normpath(r'auto_report\dark-ignore\plantillas\fishbowl_background.png')
        page.save(os.path.join(path, 'fixed', 'fishbowl_background.png'), 'PNG') 
    crop(os.path.join(path, 'fixed', 'fishbowl_background.png'))


def pecera_lateral(params, style):
    BASE_DIR = Path(__file__).resolve().parent.parent
    path = os.path.join(BASE_DIR, 'static', 'imgs', 'assets')

    params['fishbowl']['frontal']['w'] = 250*4
    params['fishbowl']['frontal']['h'] = 130*4
    latex = template(params, style)
    latex += make_fishbowl_lat(params, style)
    latex += r'''
    \end{tikzpicture}
    }
    \end{figure}
    \end{document}'''
    compile(latex)
    pages = convert_from_path(os.path.join(path, 'temp.pdf'))
    for page in pages:
        # path = r'auto_report\dark-ignore\plantillas\fishbowl_lateral.png'
        page.save(os.path.join(path, 'fixed', 'fishbowl_lateral.png'), 'PNG') 
    crop(os.path.join(path, 'fixed', 'fishbowl_lateral.png'))


def tensor(params, centers, style):
    BASE_DIR = Path(__file__).resolve().parent.parent
    path = os.path.join(BASE_DIR, 'static', 'imgs', 'assets')

    for center_name, center in centers.items():
        for module in range(center['modules']):
            module = str(module)
            params['tensors']['system']['w'] = 560*1.25
            params['tensors']['system']['h'] = 100*1.25
            # name = str(int(center['x_flip'][module])) + str(int(center['y_flip'][module])) + str(int(center['double'][module])) + f"_{str(center['jails'][module])}"
            name = center_name.replace(' ', '') + f'_{module}'
            latex = template(params, style)
            latex += make_tensor_system(params, center, style, module)
            latex += r'''
            \end{tikzpicture}
            }
            \end{figure}
            \end{document}'''
            compile(latex)
            pages = convert_from_path(os.path.join(path, 'temp.pdf'))
            for page in pages:
                # path = f'auto_report/dark-ignore/plantillas/tensor/{name}.png'
                page.save(os.path.join(path, 'tensor', name + '.png'), 'PNG') 
            crop(os.path.join(path, 'tensor', name + '.png'))
            


if __name__ == '__main__':
    BASE_DIR = Path(__file__).resolve().parent.parent
    print(BASE_DIR)
    with open(os.path.join(BASE_DIR, 'data', 'params.json')) as f:
        params = json.load(f)
    with open(os.path.join(BASE_DIR, 'data', 'centers.json')) as f:
        centers = json.load(f)
    with open(os.path.join(BASE_DIR, 'data', 'style.json')) as f:
        style = json.load(f)

    background(params, centers, style)
    lateral(params, centers, style)
    head(params, centers, style)
    separator(params, centers, style)
    pecera_background(params, style)
    pecera_lateral(params, style)
    tensor(params, centers, style)

    os.remove(os.path.join(BASE_DIR, 'static', 'imgs', 'assets', 'temp.aux'))
    os.remove(os.path.join(BASE_DIR, 'static', 'imgs', 'assets', 'temp.log'))
    os.remove(os.path.join(BASE_DIR, 'static', 'imgs', 'assets', 'temp.tex'))
    os.remove(os.path.join(BASE_DIR, 'static', 'imgs', 'assets', 'temp.pdf'))
