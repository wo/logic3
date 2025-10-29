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
\usepackage{amsmath}
\usepackage{stmaryrd} % for \llbracket and \rrbracket
\usepackage{fitch}
\def\worules{%
\def\ii{\by{$\to$I}}%
\def\ie{\by{$\to$E}}%
\def\Ai{\by{$\forall$I}}%
\def\Ae{\by{$\forall$E}}%
\def\Ei{\by{$\exists$I}}%
\def\Ee{\by{$\exists$E}}%
\def\ai{\by{$\wedge$I}}%
\def\ae{\by{$\wedge$E}}%
\def\ai{\by{$\wedge$I}}%
\def\ae{\by{$\wedge$E}}%
\def\oi{\by{$\vee$I}}%
\def\oe{\by{$\vee$E}}%
\def\ni{\by{$\neg$I}}%
\def\ne{\by{$\neg$E}}%
\def\be{\by{$\bot$E}}%
\def\nne{\by{$\neg\neg$E}}%
\def\r{\by{R}}}

\usepackage{amsfonts}
\usepackage{amssymb}

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
\newcommand{\Mfr}{\ensuremath{\mathfrak{M}}\xspace}

\newcommand{\Mod}[1]{\ensuremath{\mathfrak{#1}}\xspace}


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
\newcommand{\satisfies}{\Vdash}
\newcommand{\notsatisfies}{\not\Vdash}

\newcommand{\entails}{\vDash}
\newcommand{\notentails}{\not\vDash}

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

\newcommand{\dn}[1]{\llbracket #1 \rrbracket}



% better smallcaps:
\newcommand{\smallcaps}[1]{{\text{\footnotesize \MakeUppercase{#1}}}}

% compact enumerate environment for single-line items:
\newenvironment{cenumerate}[1][]
  {\begin{enumerate}[itemsep=2pt,parsep=0pt,topsep=6pt,partopsep=2pt,#1]}
  {\end{enumerate}}


\definecolor{rgreen}{RGB}{0,150,0}
\definecolor{rblue}{RGB}{0,0,150}
\definecolor{rred}{RGB}{180,0,0}


% Command to draw a Turing machine tape
% Usage: \turingtape{content}{highlighted position (0-indexed)}
% content is comma-separated
\newcommand{\turingtape}[2]{%
  \begin{tikzpicture}[baseline=-0.5ex]
    \foreach \symbol [count=\i from 0] in #1 {
      \ifnum\i=#2
        \node[draw=gray!50, minimum size=0.6cm, inner sep=1pt, fill=gray!10] at (\i*0.6,0) {\symbol};
      \else
        \node[draw=gray!50, minimum size=0.6cm, inner sep=1pt] at (\i*0.6,0) {\symbol};
      \fi
    }
  \end{tikzpicture}%
}

\newcommand{\inlineturingtape}[2]{%
  \begin{tikzpicture}[baseline=-0.7ex]
    \foreach \symbol [count=\i from 0] in #1 {
      \ifnum\i=#2
        \node[draw=gray!50, minimum size=0.4cm, inner sep=1pt, fill=gray!10] at (\i*0.4,0) {\symbol};
      \else
        \node[draw=gray!50, minimum size=0.4cm, inner sep=1pt] at (\i*0.4,0) {\symbol};
      \fi
    }
  \end{tikzpicture}%
}


% Turing machines

\usetikzlibrary{automata, arrows}
\usetikzlibrary{matrix, positioning, shapes.geometric, calc}
\usetikzlibrary{decorations.pathreplacing}
\usetikzlibrary{arrows.meta}

\tikzset{
  state/.style = {circle,draw,minimum size=25pt,inner sep=0pt},
  every edge/.style = {draw,->,>=Stealth,auto,font=\footnotesize},
}

\usepackage{wrapfig}

\newcommand{\num}[1]{\overline{#1}}
\newcommand{\gn}[1]{\ulcorner #1 \urcorner}

\newcommand{\pconcat}{\raisebox{0.3ex}{%
    \ensuremath{\stackrel{\scriptscriptstyle p}{\frown}}}}

\newcommand{\pconcatseventeen}{\raisebox{0.3ex}{%
    \ensuremath{\stackrel{\scriptscriptstyle 17}{\frown}}}}
\newcommand{\dotminus}{\mathrel{\dot-}}


\newenvironment{axioms}{%
    \smallskip
    \begin{flushleft}
    \begin{quote}
    \begin{tabular}{@{}ll}
}{%
    \end{tabular}
    \end{quote}
    \end{flushleft}
    \smallskip
}


\usepackage{booktabs}
\usepackage{array}
\newcolumntype{C}{>{$}c<{$}}   % math-mode centered column
\renewcommand{\arraystretch}{1.15} % a bit more row height

\usepackage{adjustbox}

\usepackage{mathtools} % coloneq

\usepackage{xcolor,pifont}

% plain green tick and red cross, exactly like the picture
\newcommand{\cmarkd}{\textcolor{green!50!black}{\ding{51}}} % ✓
\newcommand{\xmarkd}{\textcolor{red!70!black}{\ding{55}}}   % ✗

\newcommand{\cmark}{\ding{51}}
\newcommand{\xmark}{\ding{55}}

\usepackage{rotating}
\usepackage{multirow}

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

