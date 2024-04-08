def make_rectangle(x:int, y:int, w:int, h:int, label:str) -> str:
    ''' Make a rectangle with soft corners

    Args:
        x, y (int, int): top left corner of the rectangle
        w, h (int, int): width and height of the rectangle
        label: inside label of the rectangle
    '''
    rectange = f'''\draw {x,y} .. controls {x,y-3} and {x+3,y-6} .. {x+6,y-6} 
    -- {x+w,y-6} .. controls {x+w+3,y-6} and {x+w+6,y-3} .. {x+w+6,y} 
    -- {x+w+6,y+h-3} .. controls {x+w+6,y+h} and {x+w+3,y+h+3} .. {x+w,y+h+3}
    -- {x+6,y+h+3} .. controls {x+3,y+h+3} and {x,y+h} .. {x,y+h-3}
    -- cycle ;'''
    rectange += f'\draw {x + 0.55*w , y + h/3}' +\
    r'node [anchor=north] [inner sep=0.75pt] [font=\large] [align=center] {' + label + r'};'
    return rectange


def make_labels(jails:int, scope:int, x_flip:bool, y_flip:bool) -> str:
    '''Compute de jails label from left to right associated to a given center
    
    Args:
        jails (int): Number of jails of the center
        scope (int): Upper left jail label
        x_flip (bool): True if the enumeration goes from top to bottom
        y_flip (bool): True if the enumeration goes from right to left
    '''
    labels = [(str(scope+i), str(scope+i+1)) if x_flip else (str(scope+i+1), str(scope+i)) for i in range(0, jails, 2)]
    if y_flip:
        return list(reversed(labels))
    else:
        return labels


def make_tensor_labels(jails:int, x_flip:bool, y_flip:bool) -> str:
    '''Compute de jails label from left to right associated to a given center
    
    Args:
        jails (int): Number of jails of the center
        x_flip (bool): True if the enumeration goes from top to bottom
        y_flip (bool): True if the enumeration goes from right to left
    '''
    labels = [('L' + str(i+1), 'L' + str(i+2)) if x_flip else ('L' + str(i+2), 'L' + str(i+1)) for i in range(0, jails-2, 2)]
    if y_flip:
        return list(reversed(labels))
    else:
        return labels


def translate(label:str, head:bool = False) -> str:
    '''Convert a jail label to a tensor label
    
    Args:
        label (int): jail label
        head (bool): True if the tensor label correspond to a C1 or C2
    '''
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


def add_pontoon(pos:str, w:int, h:int, x:int, y:int, color:str) -> str:
    '''Add the pontoon icon in the seawolf background template on a given position
    
    Args:
        pos (str): position of the pontoon
        w, h, x, y (int, int, int, int): width, height, and coordinate of the pontoon icon
        color (str): color of the icon
    '''
    delta_x = 30
    delta_y = 25
    if pos == 'top':
        return f'\draw {x+w/2, y-delta_y} node[rectangle, fill={color}!50]' + r'{{\tiny P}};' 
    elif pos == 'top left':
        return f'\draw {x-delta_x, y-delta_y} node[rectangle, fill={color}!50]' + r'{{\tiny P}};' 
    elif pos == 'left':
        return f'\draw {x-delta_x, y+h/2} node[rectangle, fill={color}!50]' + r'{{\tiny P}};' 
    elif pos == 'bottom left':
        return f'\draw {x-delta_x, y+h+delta_y} node[rectangle, fill={color}!50]' + r'{{\tiny P}};' 
    elif pos == 'bottom':
        return f'\draw {x+w/2, y+h+delta_y} node[rectangle, fill={color}!50]' + r'{{\tiny P}};' 
    elif pos == 'bottom right':
        return f'\draw {x+w+delta_x, y+h+delta_y} node[rectangle, fill={color}!50]' + r'{{\tiny P}};' 
    elif pos == 'right':
        return f'\draw {x+w+delta_x, y+h/2} node[rectangle, fill={color}!50]' + r'{{\tiny P}};' 
    elif pos == 'top right':
        return f'\draw {x+w+delta_x, y-delta_y} node[rectangle, fill={color}!50]' + r'{{\tiny P}};' 


def add_cardinals(cardinals:list, w:int, h:int, x:int, y:int, style:dict) -> str:
    '''Add the cardinals labels in the seawolf background template

    Args:
        cardinals (list): cardinals ordered by top, left, bottom and right.
        w, h, x, y (int, int, int, int): width, height, and coordinate of the seawolf background
        style (dict): Dictionary which contains all the style parameters provided by Tri-Chile
    '''
    delta_x = 25
    delta_y = 35

    latex =  f'\draw {x+w/5, y-delta_y} ' +  r'node [anchor=north] [font=\small' + style['seawolf']['font']['background'] + r'] {\textbf{' + cardinals[0] + r'}};'
    latex +=  f'\draw {x-delta_x, y+h/5} ' +  r'node [anchor=mid, rotate=90] [font=\small' + style['seawolf']['font']['background'] + r'] {\textbf{' + cardinals[1] + r'}};'
    latex +=  f'\draw {x+4*w/5, y+h+delta_y} ' +  r'node [anchor=south] [font=\small' + style['seawolf']['font']['background'] + r'] {\textbf{' + cardinals[2] + r'}};'
    latex +=  f'\draw {x+w+delta_x, y+4*h/5} ' +  r'node [anchor=mid, rotate=270] [font=\small' + style['seawolf']['font']['background'] + r'] {\textbf{' + cardinals[3] + r'}};'
    
    return latex

