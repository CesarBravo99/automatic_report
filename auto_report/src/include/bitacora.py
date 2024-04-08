class Bitacora:
    ''' Class for creating the worklog in the reports for Tri-Chile
    
    Args:
        settings (dict): Dictionary which contains all the information provided by Tri-Chile
        images (dict): Dictironary which contains all the information provided by EasyLabel
        style (dict): Dictionary which contains all the style parameters provided by Tri-Chile
    '''

    def __init__(self, settings:dict, images:dict, style:dict) -> None:
        self.settings = settings
        self.images = images
        self.style = style


    def process(self) -> str:
        latex = r'''
        \newpage
        \newgeometry{top=3cm, left=1cm, bottom=2.5cm, right=1cm, headsep=1.5cm}
        \begin{adjustwidth}{0pt}{0pt}
        \invisiblesection{Bitácora}
        '''
        latex += self.style['worklog']['font']
        latex += r'''
        \large{
        \begin{equation*}
        \left.
        \begin{array}{c}
        \begin{tcolorbox}[width=0.94\textwidth, colframe=black, colback=white] \centering \huge
        \textit{\textbf{Datos}} \end{tcolorbox} \\
        \begin{array}{lclc}
        \begin{tcolorbox}[width=0.2\textwidth, colframe=black,colback=''' + self.style['worklog']['colorbox'] + r''', equal height group=A] 
        \textit{\textbf{''' + self.style['worklog']['info_size'] + r''' Nombre del Operador}} \end{tcolorbox}  &  
        \begin{tcolorbox}[width=0.25\textwidth, colframe=black, equal height group=A] ''' +\
        self.settings['nombre'] +\
        r''' \end{tcolorbox} &
        \begin{tcolorbox}[width=0.2\textwidth, colframe=black, colback=''' + self.style['worklog']['colorbox'] + r''', equal height group=A] 
        \textit{\textbf{''' + self.style['worklog']['info_size'] + r''' Empresa Mandante}} \end{tcolorbox}  &  
        \begin{tcolorbox}[width=0.25\textwidth, colframe=black, equal height group=A] ''' +\
        self.settings['cliente'] +\
        r''' \end{tcolorbox} \\
        \begin{tcolorbox}[width=0.2\textwidth, colframe=black, colback=''' + self.style['worklog']['colorbox'] + r''', equal height group=B] 
        \textit{\textbf{''' + self.style['worklog']['info_size'] + r''' Equipo Empleado}} \end{tcolorbox}  &  
        \begin{tcolorbox}[width=0.25\textwidth, colframe=black, equal height group=B] ''' +\
        self.settings['equipo'].upper() +\
        r''' \end{tcolorbox} &
        \begin{tcolorbox}[width=0.2\textwidth, colframe=black, colback=''' + self.style['worklog']['colorbox'] + r''', equal height group=B] 
        \textit{\textbf{''' + self.style['worklog']['info_size'] + r''' Área}} \end{tcolorbox}  &  
        \begin{tcolorbox}[width=0.25\textwidth, colframe=black,  equal height group=B] ''' +\
        self.settings['area'].capitalize() +\
        r''' \end{tcolorbox}\\
        \begin{tcolorbox}[width=0.2\textwidth, colframe=black, colback=''' + self.style['worklog']['colorbox'] + r''', equal height group=C] 
        \textit{\textbf{''' + self.style['worklog']['info_size'] + r''' Hora inicio/término}} \end{tcolorbox}  &  
        \begin{tcolorbox}[width=0.25\textwidth, colframe=black,  equal height group=C] ''' +\
        self.settings['entrada'].capitalize() + ' / ' + self.settings['salida'] +\
        r''' \end{tcolorbox} &
        \begin{tcolorbox}[width=0.2\textwidth, colframe=black, colback=''' + self.style['worklog']['colorbox'] + r''', equal height group=C] 
        \textit{\textbf{''' + self.style['worklog']['info_size'] + r''' Centro de cultivo}} \end{tcolorbox}  &  
        \begin{tcolorbox}[width=0.25\textwidth, colframe=black,  equal height group=C] ''' +\
        self.settings['centro'].capitalize() +\
        r''' \end{tcolorbox}\\
        \begin{tcolorbox}[width=0.2\textwidth, colframe=black, colback=''' + self.style['worklog']['colorbox'] + r''', equal height group=D] 
        \textit{\textbf{''' + self.style['worklog']['info_size'] + r''' Jefe de Team}} \end{tcolorbox}  &  
        \begin{tcolorbox}[width=0.25\textwidth, colframe=black,  equal height group=D] ''' +\
        self.settings['jefe_team'].capitalize() +\
        r''' \end{tcolorbox} &
        \begin{tcolorbox}[width=0.2\textwidth, colframe=black, colback=''' + self.style['worklog']['colorbox'] + r''', equal height group=D] 
        \textit{\textbf{''' + self.style['worklog']['info_size'] + r''' Encargado de Centro}} \end{tcolorbox}  &  
        \begin{tcolorbox}[width=0.25\textwidth, colframe=black,  equal height group=D] ''' +\
        self.settings['encargado_centro'].capitalize() +\
        r'''\end{tcolorbox}\\
        \begin{tcolorbox}[width=0.2\textwidth, colframe=black, colback=''' + self.style['worklog']['colorbox'] + r''', equal height group=E] 
        \textit{\textbf{''' + self.style['worklog']['info_size'] + r''' Condición del Puerto}} \end{tcolorbox}  &  
        \begin{tcolorbox}[width=0.25\textwidth, colframe=black,  equal height group=E] ''' +\
        self.settings['estado_puerto'].capitalize() +\
        r''' \end{tcolorbox} &
        \begin{tcolorbox}[width=0.2\textwidth, colframe=black, colback=''' + self.style['worklog']['colorbox'] + r''', equal height group=E] 
        \textit{\textbf{''' + self.style['worklog']['info_size'] + r''' Ataque lobero}} \end{tcolorbox}  &  
        \begin{tcolorbox}[width=0.25\textwidth, colframe=black,  equal height group=E] ''' +\
        self.settings['ataque'] +\
        r'''\end{tcolorbox}
        \end{array}
        \end{array}
        \right.
        \end{equation*}
    
        \begin{equation*}
        \left. \begin{array}{lr}
        \begin{tcolorbox}[colbacktitle=''' + self.style['worklog']['colorbox'] + r''', coltitle=black, colframe=black, title=\Large\textit{\textbf{\Large Observaciones}}] 
        \begin{center} \textit{\Large Faena Realizada} \end{center}'''

        obsPecera = ''
        obsLobera = ''
        obsCabecera = ''
        obsSeparador = ''
        obsAdherencia = ''
        obsTensor = ''
        obsMortalidad = ''

        for data in self.images.values():
            if data['type'] == 'mortality':
                    obsMortalidad += data['obs'] + ', ' if data['obs'] != 'Sin observación del piloto' else ''
            elif data['type'] == 'adherence':
                obsAdherencia += data['obs'] + ', ' if data['obs'] != 'Sin observación del piloto' else ''
            elif data['system'] == 'lobero':
                if data['separator'] == 'None':
                    obsLobera += data['obs'] + ', ' if data['obs'] != 'Sin observación del piloto' else ''
                else:
                    obsSeparador += data['obs'] + ', ' if data['obs'] != 'Sin observación del piloto' else ''
            elif data['system'] == 'pecero':
                obsPecera += data['obs'] + ', ' if data['obs'] != 'Sin observación del piloto' else ''
            elif data['system'] == 'tensor':
                obsTensor += data['obs'] + ', ' if data['obs'] != 'Sin observación del piloto' else ''


        observaciones = ''
        if obsPecera != '':
            observaciones += r'''\item  ''' + '\n' + 'Pecera: ' + obsPecera[:-2]
        if obsLobera != '':
            observaciones += r'''\item  ''' + '\n' + 'Lobera: ' + obsLobera[:-2]
        if obsCabecera != '':
            observaciones += r'''\item  ''' + '\n' + 'Cabecera: ' + obsCabecera[:-2]
        if obsSeparador != '':
            observaciones += r'''\item  ''' + '\n' + 'Separador: ' + obsSeparador[:-2]
        if obsAdherencia != '':
            observaciones += r'''\item  ''' + '\n' + 'Adherancia: ' + obsAdherencia[:-2]
        if obsTensor != '':
            observaciones += r'''\item  ''' + '\n' + 'Tensor: ' + obsTensor[:-2]
        if obsMortalidad != '':
            observaciones += r'''\item  ''' + '\n' + 'Mortalidad: ' + obsMortalidad[:-2]
        if observaciones != '':
            latex += r'\begin{enumerate}[$\star$] ' + self.style['worklog']['obs_size'] + '{\n '+ observaciones +  r'}\end{enumerate}'
        else: 
            latex += r'\begin{enumerate}[$\star$] \item No hay observaciones \end{enumerate}'


        latex += r'''\end{tcolorbox}
        \end{array}\right.
        \end{equation*}

        }
        \end{adjustwidth}'''

        return latex
