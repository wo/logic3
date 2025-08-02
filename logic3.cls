% !TEX program = xelatex
\ProvidesClass{logic3}
\NeedsTeXFormat{LaTeX2e}

% parent class scrbook:
\DeclareOption*{\PassOptionsToClass{\CurrentOption}{scrbook}}
\ProcessOptions
\LoadClass[12pt, twoside=false, a4paper, DIV=10, headsepline, footnotes=multiple]{scrbook}

\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}

% ============= math packages =============

\usepackage{amsthm}
\usepackage[fleqn, leqno]{amsmath}
\usepackage{fitch}
\setlength\mathindent{1.6cm}
\everydisplay{\displayindent=1cm}
% \usepackage{amsfonts}
% \usepackage{amssymb}

% ============= additional packages =============
% 
\usepackage{enumerate} % for enumerate with roman and alphabetical labels
\usepackage{fancyvrb,paralist}
\usepackage{multirow,rotating}
\usepackage{eqlist}
\usepackage{mdwlist}
\usepackage[english]{babel} % English language/hyphenation
\usepackage{graphicx} % for including pictures
\usepackage[table,xcdraw]{xcolor}
\usepackage{tikz}
\usepackage{scalerel} % \scaleto for tiny letters
% ============= fonts ==============
% 
\usepackage{fontspec}
\usepackage{unicode-math}
\defaultfontfeatures{Scale=MatchLowercase, Ligatures=TeX}
\setmainfont{TeX Gyre Termes}[Scale=1.0]
\setmathfont{TeX Gyre Termes Math}
\newfontfamily{\headerfont}{Utopia}
\addtokomafont{chapter}{\headerfont\mdseries}
\addtokomafont{section}{\headerfont\mdseries}

% math packages:
% \usepackage{amsthm}
% \usepackage[fleqn, leqno]{amsmath}
% \setlength\mathindent{1.6cm}
% \everydisplay{\displayindent=1cm}
% \usepackage{amsfonts}
% \usepackage{amssymb}

% \setkomafont{disposition}{\normalfont}

% \RedeclareSectionCommands[%
%   tocentrynumberformat=\headerfont\bfseries,
%   tocentryformat=\headerfont\bfseries,%
%   tocpagenumberformat=\headerfont\bfseries,%
% ]{chapter}

% \RedeclareSectionCommands[%
%   tocentrynumberformat=\headerfont,%
%   tocentryformat=\headerfont,%
%   tocpagenumberformat=\headerfont,%
% ]{section}

% \usepackage[osf,sc]{mathpazo} % Palatino for main text and math
%\usepackage[scaled=0.90]{helvet} % Helvetica for sans serif (scaled to match size of Palatino)
%\usepackage{newtxtext}
%\usepackage{newtxmath}
%\usepackage[scaled=0.90]{helvet} % Helvetica for sans serif (scaled to match size of Palatino)
%\usepackage{newtxmath}
%\usepackage{txfonts}
%\usepackage{fouriernc}
%\usepackage[onlytext]{MinionPro}
%\renewcommand{\sfdefault}{Myriad-LF}
%\usepackage{lmodern}
%\usepackage{libertine}
%\usepackage[libertine]{newtxmath}
%\usepackage{kpfonts}
%\usepackage{mathpazo}
%\usepackage{mathpazo}
%\usepackage{eulervm}
%\usepackage{charter}
%\usepackage[bitstream-charter]{mathdesign}

% ============= chapter/section headings =============
% 
% \setkomafont{chapter}{%
% \renewcommand{\bfdefault}{sb}%
% %\usefont{T1}{qhv}{b}{n}\selectfont
% \fontfamily{put}\bfseries\huge%
% %\rmfamily\huge
% \renewcommand{\bfdefault}{bx}%
% }
% \setkomafont{section}{%
% \renewcommand{\bfdefault}{sb}%
% %\usefont{T1}{qhv}{b}{n}\selectfont
% %\bfseries\Large
% \fontfamily{put}\bfseries\large%
% \renewcommand{\bfdefault}{bx}%
% }
% \setkomafont{subsection}{%
% \renewcommand{\bfdefault}{sb}%
% \fontfamily{put}\bfseries\large%
% \renewcommand{\bfdefault}{bx}%
% }
% \usepackage[grey,avantgarde]{quotchap}% For a nice grey number at each new chapter, also allows for chapter quotes

% ============= text formatting tweaks =============

\usepackage{url,ellipsis}
\usepackage[final=true,step=1]{microtype}
\usepackage{ragged2e}
\clubpenalty = 500
\widowpenalty = 1000
\urlstyle{sf}
\deffootnote[1.5em]{1.5em}{1.5em}{\thefootnotemark \hspace{0.2em}} 
% line spacing:
\usepackage{setspace}
\def\mynormalstretch{1.05}
\setstretch{\mynormalstretch}
\usepackage[nice]{nicefrac}
\usepackage{textcomp}

% ============= tables =============

\usepackage{booktabs}
% \renewcommand{\arraystretch}{1.1} % more space between table rows
\usepackage{tabularx}

% ============= page headers =============

% removes the header from odd empty pages at the end of chapters:
\makeatletter
\renewcommand{\cleardoublepage}{
\clearpage\ifodd\c@page\else
\hbox{}
\vspace*{\fill}
\thispagestyle{empty}
\newpage
\fi}

% ============= colors and links =============

\definecolor{linkcol}{rgb}{0,0.1,0.4}
\definecolor{citecol}{rgb}{0,0.2,0.2}
\usepackage[colorlinks=true,
            linkcolor=linkcol,
            urlcolor=linkcol,
            citecolor=citecol]{hyperref}

% ============= citations ==============

\usepackage{natbib}
\bibpunct[: ]{[}{]}{,}{A}{}{,~}
\renewcommand{\cite}[2][]{\citep[#1]{#2}}
\newcommand{\citey}[2][]{\citeyearpar[#1]{#2}}
\newcommand{\citeplain}[2][]{\citealt[#1]{#2}}
\newcommand{\citeyplain}[2][]{\citeyear[#1]{#2}}

% ============= Logic symbols ============

\renewcommand{\t}[1]{\ensuremath{\langle #1 \makebox[.2ex]{}\rangle}}

\let\polishL\L
\renewcommand{\L}{\ensuremath{\mathfrak{L}}\xspace}
\newcommand{\Cfr}{\ensuremath{\mathfrak{C}}\xspace}
\newcommand{\Mfr}{\ensuremath{M}\xspace}

% make box and diamond larger, and vdash (too small in newtxmath):
% \usepackage{scalerel}
% \let\oldbox\Box
% \renewcommand\Box{\scaleobj{1.2}{\oldbox}}
% \let\olddiamond\Diamond
% \renewcommand\Diamond{\scaleobj{1.2}{\olddiamond}}

% make \to smaller and with less spacing to the sides:
\let\oldto\to
\renewcommand\to{\scaleobj{0.95}{\,\oldto\,}}
\let\oldleftrightarrow\leftrightarrow
\renewcommand\leftrightarrow{\scaleobj{0.95}{\,\oldleftrightarrow\,}}

% define strictif and boxright:
\DeclareSymbolFont{symbolsC}{U}{txsyc}{m}{n}
\DeclareMathSymbol{\strictif}{\mathrel}{symbolsC}{74}
\DeclareMathSymbol{\boxright}{\mathrel}{symbolsC}{128}

% turnstiles:

% \let\oldvdash\vdash
% \renewcommand\vdash{\scaleobj{1.3}{\oldvdash}}

\newcommand{\proves}{\vdash}
\newcommand{\notproves}{\not\vdash}

% \AtBeginDocument{ % otherwise ignored by unicode-math
%   \renewcommand{\entails}{\mathrel{|}\joinrel=}
% }
% \newcommand{\nentails}{\mathrel{|}\joinrel\not=}

\AtBeginDocument{ % otherwise ignored by unicode-math
  \renewcommand{\models}{\vDash}
}
\newcommand{\notmodels}{\not\vDash}

\newcommand{\entails}{\Vdash}
\newcommand{\notentails}{\not\Vdash}

% inverted \entails:
\makeatletter
\providecommand*{\inventails}{%
  \mathrel{%
    \mathpalette\@inventails\entails
  }%
}
\newcommand*{\@inventails}[2]{%
  \reflectbox{$\m@th#1#2$}%
}
\makeatother




% better smallcaps:
\newcommand{\smallcaps}[1]{{\text{\footnotesize \MakeUppercase{#1}}}}

% compact enumerate environment for single-line items:
\newenvironment{cenumerate}[1][]
  {\begin{enumerate}[itemsep=2pt,parsep=0pt,topsep=6pt,partopsep=2pt,#1]}
  {\end{enumerate}}

%========= graphs for models ========

% adapted from http://www.actual.world/resources/tex/doc/TikZ.pdf

\usetikzlibrary{positioning,arrows,calc}
\tikzset{
modal/.style={>=stealth',shorten >=1pt,shorten <=1pt,auto,node distance=1.5cm,
semithick},
world/.style={circle,draw,minimum size=0.5cm,fill=gray!15,font=\small},
point/.style={circle,draw,inner sep=0.5mm,fill=black},
reflexive above/.style={->,loop,looseness=7,in=120,out=60},
reflexive below/.style={->,loop,looseness=7,in=240,out=300},
reflexive left/.style={->,loop,looseness=7,in=150,out=210},
reflexive right/.style={->,loop,looseness=7,in=30,out=330}
}
\definecolor{rgreen}{RGB}{0,150,0}
\definecolor{rblue}{RGB}{0,0,150}
\definecolor{rred}{RGB}{180,0,0}


% tm:


\usetikzlibrary{automata, positioning, arrows}
\usepackage{mathtools} % coloneq


% ========== Tree proofs ===========

\usepackage{xyling}
\usepackage{xfp}
\usepackage{ifthen}
\definecolor{annotcol}{rgb}{0.3, 0.4, 0.5}
\definecolor{red}{rgb}{1,0,0}
\def\checkmark{\color{annotcol}\tikz\fill[scale=0.4](0,.35) -- (.25,0) -- (1,.7) -- (.25,.15) -- cycle;}
\newcommand{\xmark}{\ding{55}}%
\newcommand{\tree}[2][0]{\Treek[#1]{0.7}{#2}}
%\newcommand{\dotline}{\GB{d}{.}}
\newcommand{\wlabel}[2]{\Kk[#1]{0}{\ifthenelse { \equal {#2} {} } {} {\ensuremath{(#2)}}}}
\newcommand{\ticklabel}[1]{\Kk[#1]{0}{\ensuremath{\checkmark}}}
\newcommand{\annotlabel}[2]{\Kk[#1]{0}{{\color{annotcol}#2}}}
\newcommand{\llabel}[2]{\Kk[-#1]{0}{{\color{annotcol}#2}}}
\newcommand{\branchbelow}{\B{ddl}\B{ddr}}
\newcommand{\tribranchbelow}{\B{ddl}\B{dd}\B{ddr}}
\newcommand{\closed}{\Below{\sffamily x}}
\newcommand{\treenode}[5]{\llabel{\fpeval{(#1)-1}}{#2} #3 \wlabel{#1}{#4} \annotlabel{\fpeval{(#1)+10}}{#5}}
\newcommand{\treenodeticked}[5]{\llabel{\fpeval{(#1)-1}}{#2} #3 \wlabel{#1}{#4} \annotlabel{\fpeval{(#1)+10}}{#5}  \ticklabel{\fpeval{(#1)+18}}  }
\newcommand{\nnode}[5]{\treenode{#1}{#2}{\K{#3}}{#4}{#5}}
\newcommand{\nnodeticked}[5]{\treenodeticked{#1}{#2}{\K{#3}}{#4}{#5}}
\newcommand{\nnodeclosed}[5]{\treenode{#1}{#2}{\K{#3}\closed}{#4}{#5}}
\newcommand{\dotbelowbnode}[5]{\treenode{#1}{#2}{\K{#3}\GB{dd}{.}\B[-8]{dddl}\B[-8]{dddr}}{#4}{#5}}
\newcommand{\dotbelownode}[5]{\treenode{#1}{#2}{\K{#3}\GB{dd}{.}}{#4}{#5}}
\newcommand{\bnode}[5]{\treenode{#1}{#2}{\K{#3}\branchbelow}{#4}{#5}}
\newcommand{\bnodeticked}[5]{\treenodeticked{#1}{#2}{\K{#3}\branchbelow}{#4}{#5}}
\newcommand{\tribnode}[5]{\treenode{#1}{#2}{\K{#3}\tribranchbelow}{#4}{#5}}
\newcommand{\barenode}[1]{\K{#1}}
\newcommand{\dotbelowbarenode}[1]{\K{#1}\GB{dd}{.}}
\newcommand{\dotbelowbarebnode}[1]{\K{#1}\GB{dd}{.}\B[-8]{dddl}\B[-8]{dddr}}
\newcommand{\dotbelowbaretribnode}[1]{\K{#1}\GB{dd}{.}\B[-8]{dddl}\B[-8]{ddd}\B[-8]{dddr}}

% Syntax:
%
% \tree[1]{ ... } => optional 1 adds width to branching
%
% Trees are defined like tabular tables:
%
% \tree{ & node1 & \\ node2 & & node3 }
%
% A tree node is defined by
%
% \nnode{10}{1.}{$A \land B$}{w}{Ass.}
%
% The first argument (10) controls the distance between the formula
% and the line number/world/annotation.
%
% Nodes under which the tree branches are defined by \bnode instead of
% \nnode. A bnode must be followed by an empty row:
%
%\tree[2]{
%    & \bnode{13}{1.}{$A \lor B$}{w}{Ass.} & \\
%    && \\
%    \nnode{8}{2.}{$A$}{w}{(1)} && \nnode{8}{3.}{$B$}{w}{(1)}
%}


% ========== shortcuts for displaying named axiom schemas ========
% 
\newcommand{\principle}[2]{\begin{equation}\tag{#1}#2\end{equation}}
\newenvironment{principles}{\gather}{\endgather}
\newcommand{\pri}[2]{#2 \tag{#1}}
\newcommand{\pr}[1]{(#1)}

% ========== CC license logo ===========
                                             
\usepackage[type={CC}, modifier={by-nc-sa}, version={4.0}, imageposition=left, imagewidth=20mm, imagedistance=3mm]{doclicense}

