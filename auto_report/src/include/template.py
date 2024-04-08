class Template:
    ''' Class for creating the LaTex template for the reports of Tri-Chile
    
    Args:
        settings (dict): Dictionary which contains all the information provided by Tri-Chile
        params (dict): Dictironary which contains internal information
        style (dict): Dictionary which contains all the style parameters provided by Tri-Chile
    '''
    def __init__(self, settings:dict, params:dict, style:dict) -> None:
        self.settings = settings
        self.params = params
        self.style = style


    def init_template(self) -> str:
        latex = r'''\documentclass[english]{article}''' + '\n'

        for pkg in self.params['template']['packages']:
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

        for name, color in self.style['template']['colors'].items():
            latex += r'\definecolor{' + name + r'}{RGB}{' + color + r'}'

        latex += r'''\newcommand*{\boldcheckmark}{%
        \textpdfrender{
            TextRenderingMode=FillStroke,
            LineWidth=1pt, % half of the line width is outside the normal glyph
        }{\color{''' + self.style['ocg']['color']['correct'] + r'''}\checkmark}%
        }

        \newcommand{\Crosscheck}{$\mathbin{\tikz [x=1.4ex,y=1.4ex,line width=.4ex, ''' + self.style['ocg']['color']['lack_tension'] + r'''] \draw (-0.1,0.3)--(0.1,0.1) -- (1,1) (0.1,0.9) -- (0.9,0.1);}$}%
        \newcommand*{\boldcrosscheck}{%
        \textpdfrender{
            TextRenderingMode=FillStroke,
            LineWidth=1.5pt, % half of the line width is outside the normal glyph
        }{\Crosscheck}%
        }

        \newcommand{\Cross}{$\mathbin{\tikz [x=1.4ex,y=1.4ex,line width=.4ex, ''' + self.style['ocg']['color']['tear'] + r'''] \draw (0,0) -- (1,1) (0,1) -- (1,0);}$}%
        \newcommand*{\boldcross}{%
        \textpdfrender{
            TextRenderingMode=FillStroke,
            LineWidth=1.5pt, % half of the line width is outside the normal glyph
        }{\Cross}%
        }

        \newcommand{\Triangle}{$\mathbin{\tikz [x=1.4ex,y=1.4ex,line width=.4ex, ''' + self.style['ocg']['color']['anomaly'] + r'''] \draw (0,0)--(1,0)--(60:1)--(0,0)--cycle;}$}%
        \newcommand*{\boldtriangle}{%
        \textpdfrender{
            TextRenderingMode=FillStroke,
            LineWidth=1.5pt, % half of the line width is outside the normal glyph
        }{\Triangle}%
        }

        \newcommand{\Cruz}{$\mathbin{\tikz [x=1.8ex,y=1.8ex,line width=.4ex, ''' + self.style['ocg']['color']['adherence'] + r'''] \draw (0.5,0) -- (0.5,1) (0,0.5) -- (1,0.5);}$}%
        \newcommand*{\boldcruz}{%
        \textpdfrender{
            TextRenderingMode=FillStroke,
            LineWidth=1.5pt, % half of the line width is outside the normal glyph
        }{\Cruz}%
        }

        \newcommand{\MyDiamond}{$\mathbin{\tikz [x=1.4ex, y=1.4ex, line width=.4ex, draw=''' + self.style['ocg']['color']['mortality'] + r''', fill=''' + self.style['ocg']['color']['mortality'] + r'''] \draw (0,0.5) -- (0.5,1) -- (1,0.5) -- (0.5,0) -- cycle;}$}%
        \newcommand*{\bolddiamond}{%
        \textpdfrender{
            TextRenderingMode=FillStroke,
            LineWidth=1.5pt, % half of the line width is outside the normal glyph
        }{\MyDiamond}%
        }

        
        \pagestyle{fancy}
        \fancyhf{}
        \fancyhead[L]{
            \vspace{-1cm}
            \begin{picture}(0,0) \put''' + self.style['template']['logo_position'] + r'''{
                \includegraphics[width=''' + self.style['template']['logo_width'] + r''']{''' + self.style['logo_user'] + r'''}
            } 
            \end{picture}
        }
        \fancyhead[C]{
        $\left.
        \begin{array}{c}
        $ $\\[4pt]
        \text{\Huge\textbf{\textit{\leftmark}}} \\[4pt]
        $ $
        \end{array}   
        \right.$
        }
        \fancyhead[R]{%
        $\left.
        \begin{array}{lr}
        \textit{\Large Fecha:} &\textit{\Large\textcolor{black}{''' +\
        self.settings['fecha'] + r'''}}\\ 
        \textit{\Large\textcolor{black}{Centro:}} &\textit{\Large\textcolor{black}{''' +\
        self.settings['centro'] + r'''}}
        \end{array}   
        \right.$
        }
        \fancyfoot[L]{%
        \Large
        \textcolor{black}{\textit{Nombre Piloto: '''
        nombre = self.settings['nombre'].split(' ')
        latex += nombre[2] + ' ' + nombre[0] +\
        r'''}}
        }
        \fancyfoot[C]{%
        \Large
        \textcolor{black}{\textit{Fono Piloto: ''' +\
        self.settings["fono_piloto"] +\
        r'''}}
        }
        \fancyfoot[R]{%
        \Large
        \textcolor{black}{\textit{Mail Piloto: ''' +\
        self.settings["mail_piloto"] +\
        r'''}}
        }
        \let\oldheadrule\headrule % Copy \headrule into \oldheadrule
        \let\oldfootrule\headrule % Copy \headrule into \oldheadrule
        
        \renewcommand{\oldheadrule}{\rule{12cm}{2pt} \vspace{-8pt}
        \raisebox{-2.1pt}{\hspace{0.375cm} \decofourleft\decoone\decofourright \hspace{0.375cm}}
        \rule{12cm}{2pt}}
        
        \renewcommand{\oldfootrule}{\rule{12cm}{2pt} \vspace{8pt}
        \raisebox{-2.1pt}{\hspace{0.375cm} \floweroneleft\floweroneright \hspace{0.375cm}}
        \rule{12cm}{2pt}}
        
        \renewcommand{\headrule}{\color{''' + self.style["template"]["headrule"] + r'''}\oldheadrule}
        \renewcommand{\headrulewidth}{2pt} 
        \renewcommand{\footrule}{\color{''' + self.style["template"]["footrule"] + r'''}\oldfootrule}
        \renewcommand{\footrulewidth}{2pt}

        \begin{document}
        '''
        return latex


    def stamps(self) -> str:
        latex = r'''
            \vspace{''' + self.style['cover_page']['vspace_logo_client'] + r'''}
            \begin{figure}[h!]
            \hspace{''' + self.style['cover_page']['hspace_logo_client'] + r'''}
            \includegraphics[width=''' + self.style['cover_page']['width_logo_client'] + r''']{''' + self.style['logo_client'] + r'''}
            \end{figure}
            '''
        latex += r'''
        \vspace{''' + self.style['cover_page']['vspace_logo_cover'] + r'''} 
        \begin{figure}[h!]
        \centering
        \includegraphics[width=''' + self.style['cover_page']['width_logo_cover'] + r''']{''' + self.style['logo_cover'] + r'''}\\ 
        \begin{Huge}
        \textcolor{white}{\textbf{\textit{Informe Diario \\ Inspección Submarina}}}
        \end{Huge}	  
        \end{figure}
        {\raggedleft\vfill\itshape\Longstack[l]{
        \textcolor{white}{\Huge \textbf{\textit{Centro ''' + self.settings['centro'].capitalize() + r'''
        }}} \hspace{''' + self.style['cover_page']['hspace_logo_cover'] + r'''}$ $
        }\par
        }
        \vspace{1cm}
        '''
        return latex


    def front_page(self) -> str:
        latex = r'''
        \clearpage
        \KOMAoptions{paper=landscape, DIV=last}
        \newgeometry{top=0cm, left=0cm, bottom=0cm, right=0cm, headsep=0cm}
        \fancyheadoffset{0pt}
        \thispagestyle{empty}
        \BackImage[width=\textwidth , height=\textheight]{''' + self.style['front'] + r'''}
        $ $
        '''
        latex += self.stamps()
        return latex


    def back_page(self) -> str:
        latex = r'''
        \newpage
        \newgeometry{top=0cm, left=0cm, bottom=0cm, right=0cm, headsep=0cm}
        \fancyheadoffset{0pt}
        \thispagestyle{empty}
        \BackImage[width=\textwidth , height=\textheight]{''' + self.style['back'] + r'''}
        $ $
        '''
        latex += self.stamps()
        return latex
