#!/usr/bin/env python3
"""Create HTML version of textbook."""

import os
import re
import shutil
import subprocess
import argparse
import datetime
from bs4 import BeautifulSoup
from html5lib import HTMLParser, constants

tmp_path = "tmp"
html_path = "html"

tex4ht_config = r"""
\Preamble{xhtml}
\Configure{tableofcontents*}{chapter,section,subsection}
\begin{document}
\EndPreamble
"""


MATHJAX_VERSION = "4.1.1"
MATHJAX_SCRIPT = f"html/mathjax/tex-chtml-nofont.js"
STIX2_CHTML = f"html/mathjax-fonts/mathjax-stix2-font/chtml.js"


def ensure_mathjax():
    """Download MathJax and STIX2 font files if not already present."""
    if os.path.exists(MATHJAX_SCRIPT) and os.path.exists(STIX2_CHTML):
        return
    import tempfile
    print("Installing MathJax and STIX2 font...")
    os.makedirs("html/mathjax", exist_ok=True)
    os.makedirs("html/mathjax-fonts/mathjax-stix2-font", exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        v = MATHJAX_VERSION
        # MathJax — full package (extensions loaded dynamically need to be present)
        subprocess.run(["npm", "pack", f"mathjax@{v}"], cwd=tmp, check=True,
                       capture_output=True)
        subprocess.run(["tar", "-xzf", f"mathjax-{v}.tgz", "--strip-components=1",
                        "-C", os.path.abspath("html/mathjax")], cwd=tmp, check=True,
                       capture_output=True)
        # STIX2 font package (chtml files only)
        subprocess.run(["npm", "pack", f"@mathjax/mathjax-stix2-font@{v}"],
                       cwd=tmp, check=True, capture_output=True)
        subprocess.run(["tar", "-xzf", f"mathjax-mathjax-stix2-font-{v}.tgz",
                        "--strip-components=1",
                        "-C", os.path.abspath("html/mathjax-fonts/mathjax-stix2-font"),
                        "--wildcards", "package/chtml*"],
                       cwd=tmp, check=True, capture_output=True)
    print("✓ MathJax installed.")


def main():
    """Create HTML version of textbook."""
    argparser = argparse.ArgumentParser(description="Create HTML version")
    argparser.add_argument('-f', '--fake', action='store_true', help="Use previous make4ht output")
    argparser.add_argument('-v', '--verbose', action='store_true', help="Verbose output")
    args = argparser.parse_args()

    ensure_mathjax()

    if not args.fake:
        prepare_paths()
        prepare_tex()
        make4ht(verbose=args.verbose)
        restore_css()
    save_or_restore_make4ht_output(restore=args.fake)

    rename_html_files()
    fix_toc_links()
    fix_html()
    create_index()
    check_links()


def prepare_paths():
    """Ensure tmp and html directories exist and tmp is empty."""
    try:
        shutil.rmtree(tmp_path)
    except FileNotFoundError:
        pass
    os.mkdir(tmp_path)
    if not os.path.exists(html_path):
        os.mkdir(html_path)
    # delete all html and svg files in html_path:
    # for f in os.listdir(html_path):
    #     if f.endswith('.html') or f.endswith('.svg'):
            # os.remove(html_path + '/' + f)
    # rename logic3.css in html_path so that we can restore it later:
    if os.path.exists(html_path + '/logic3.css'):
        print("Renaming logic3.css to _logic3.css")
        shutil.copyfile(html_path + '/logic3.css', html_path + '/_logic3.css')
    # create tex4ht configuration file:
    write_file(tmp_path + "/mytex4ht.cfg", tex4ht_config.strip())


def restore_css():
    """Restore customized logic3.css file that's overwritten by make4ht."""
    if os.path.exists(html_path + '/_logic3.css'):
        shutil.move(html_path + '/_logic3.css', html_path + '/logic3.css')


def prepare_tex():
    """Prepare the LaTeX files for processing."""
    shutil.copy('logic3.tex', tmp_path + '/logic3.tex')
    for chapter in tex_files():
        prep_chapter(chapter)
    prep_header_boxes()
    prep_logic3_cls()
    shutil.copy('doclicense-CC-by-nc-sa.pdf', tmp_path)
    shutil.copy('doclicense-CC-by-nc-sa.svg', tmp_path + '/doclicense-CC-by-nc-sa-88x31.svg')
    shutil.copy('logic3book.css', tmp_path)
    # Copy figures directory if it exists:
    if os.path.exists('figures'):
        shutil.copytree('figures', tmp_path + '/figures', dirs_exist_ok=True)


def tex_files():
    """Return list of chapter files."""
    pattern = re.compile(r'^\d\d-[^.]+\.tex$')
    chapters = [f for f in os.listdir('.') if pattern.match(f)]
    chapters.append('title.tex')
    return chapters


def html_files():
    """Return list of HTML files."""
    return [f for f in os.listdir(html_path) if f.endswith('.html')]


def prep_header_boxes():
    """Edit header-boxes.tex for conversion to HTML."""
    tex = read_file('header-boxes.tex')
    tex = re.sub('enforce breakable,', '%enforce breakable,', tex)
    tex = re.sub('breakable,', '%breakable,', tex)
    write_file(tmp_path + "/header-boxes.tex", tex)


def prep_logic3_cls():
    """Prepare logic3.cls for conversion to HTML."""
    cls = read_file("logic3.cls")
    # The custom column type C causes issues with tex4ht - disable it:
    cls = re.sub(r'\\newcolumntype\{C\}\{>\{\$\}c<\{\$\}\}',
                 r'\\newcolumntype{C}{c}', cls)
    write_file(tmp_path + "/logic3.cls", cls)


def prep_chapter(texfile):
    """Edit LaTeX chapter for conversion to HTML."""
    tex = read_file(texfile)
    tex = remove_noindent(tex)
    tex = fix_turingtape(tex)
    tex = fix_smallcaps_in_math(tex)
    tex = fix_custom_commands(tex)
    tex = fix_gather(tex)
    tex = fix_math_line_spacing(tex)
    tex = fix_math_columns(tex)
    tex = escape_labeled_items(tex)
    tex = escape_intext_links(tex)
    write_file(tmp_path + "/" + texfile, tex)


def fix_turingtape(tex):
    r"""Replace \turingtape / \inlineturingtape with placeholder markers.

    The \turingtape macro is a TikZ-based renderer that tex4ht/MathJax can't
    handle, so we strip it out and emit a TTAPESTART…TTAPEEND marker that
    fix_turingtape_html turns into HTML cells. The mode encodes whether the
    surrounding source had \ldots on the left/right (so we know whether to
    render leading/trailing ellipses).
    """
    def make_marker(mode, content, pos):
        return f'TTAPESTART|{mode}|{content}|{pos}|TTAPEEND'

    def display_mode(left_ldots, right_ldots):
        if left_ldots and right_ldots:
            return 'D'
        if left_ldots:
            return 'Dl'
        if right_ldots:
            return 'Dr'
        return 'D-'

    # \[ [\ldots] \turingtape{{cells}}{pos} [\ldots] \]
    display_pattern = re.compile(
        r'\\\[\s*(\\ldots\s+)?'
        r'\\turingtape\{\{([^{}]+)\}\}\{(\d+)\}'
        r'(\s+\\ldots)?\s*\\\]'
    )
    def display_repl(m):
        marker = make_marker(display_mode(m.group(1), m.group(4)), m.group(2), m.group(3))
        return f'\n\n{marker}\n\n'
    tex = display_pattern.sub(display_repl, tex)

    # gather* containing one or more [\ldots] \turingtape{{X}}{Y} [\ldots] lines
    line_pattern = re.compile(
        r'\s*(\\ldots\s+)?'
        r'\\turingtape\{\{([^{}]+)\}\}\{(\d+)\}'
        r'(\s+\\ldots)?\s*$'
    )
    def gather_repl(m):
        body = m.group(1)
        if r'\turingtape' not in body:
            return m.group(0)
        out = []
        for line in re.split(r'\\\\', body):
            line_m = line_pattern.match(line)
            if line_m:
                out.append(make_marker(
                    display_mode(line_m.group(1), line_m.group(4)),
                    line_m.group(2), line_m.group(3),
                ))
        if out:
            return '\n\n' + '\n\n'.join(out) + '\n\n'
        return m.group(0)
    tex = re.sub(
        r'\\begin\{gather\*\}(.*?)\\end\{gather\*\}',
        gather_repl, tex, flags=re.DOTALL,
    )

    # \inlineturingtape{{cells}}{pos}
    tex = re.sub(
        r'\\inlineturingtape\{\{([^{}]+)\}\}\{(\d+)\}',
        lambda m: make_marker('I', m.group(1), m.group(2)),
        tex,
    )
    return tex


def remove_noindent(tex):
    r"""Remove \noindent commands that prevent rendering text as p."""
    # Replace with a space to avoid joining adjacent words (e.g., \medskip\noindent\nNode)
    return re.sub(r'\\noindent\s*%?', ' ', tex)


_MATH_REGION = re.compile(
    r'\\\(.*?\\\)|\\\[.*?\\\]|\$\$.*?\$\$|\$.*?\$|'
    r'\\begin\{(equation\*?|align\*?|flalign\*?|gather\*?|multline\*?|eqnarray\*?)\}'
    r'.*?\\end\{\1\}',
    re.DOTALL,
)

# Same but for HTML output where tex4ht may add spaces in \begin {align*}
_HTML_MATH_REGION = re.compile(
    r'\\\(.*?\\\)|\\\[.*?\\\]|'
    r'\\begin\s*\{(equation\*?|align\*?|flalign\*?|gather\*?|multline\*?|eqnarray\*?)\}'
    r'.*?\\end\s*\{\1\}',
    re.DOTALL,
)


def sub_outside_math(pattern, replacement, tex):
    """Apply re.sub only to non-math segments of tex."""
    out = []
    last = 0
    for m in _MATH_REGION.finditer(tex):
        out.append(re.sub(pattern, replacement, tex[last:m.start()]))
        out.append(m.group(0))
        last = m.end()
    out.append(re.sub(pattern, replacement, tex[last:]))
    return ''.join(out)


def fix_custom_commands(tex):
    """Fix custom commands that make4ht doesn't understand."""
    # Fraktur letters - use word boundary or followed by non-letter
    tex = re.sub(r'\\L(?![a-zA-Z])', r'\\mathfrak{L}', tex)
    tex = re.sub(r'\\Cfr\b', r'\\mathfrak{C}', tex)
    tex = re.sub(r'\\Mfr\b', r'\\mathfrak{M}', tex)
    tex = re.sub(r'\\Mod\{([^}]+)\}', r'\\mathfrak{\1}', tex)
    # Handle \t{} tuples; allow up to two levels of nested braces, e.g.
    # \t{\llbracket t_1\rrbracket^{\mathfrak{M}},\ldots} where ^{...} contains {M}
    tex = re.sub(r'\\t\{((?:[^{}]|\{(?:[^{}]|\{[^{}]*\})*\})*)\}', r'\\langle \1 \\rangle', tex)
    # Turnstiles and semantic relations:
    tex = re.sub(r'\\notsatisfies(?![a-zA-Z])', r'\\not\\Vdash', tex)
    tex = re.sub(r'\\satisfies(?![a-zA-Z])', r'\\Vdash', tex)
    tex = re.sub(r'\\notentails(?![a-zA-Z])', r'\\not\\vDash', tex)
    tex = re.sub(r'\\entails(?![a-zA-Z])', r'\\vDash', tex)
    tex = re.sub(r'\\notproves(?![a-zA-Z])', r'\\not\\vdash', tex)
    tex = re.sub(r'\\proves(?![a-zA-Z])', r'\\vdash', tex)
    tex = re.sub(r'\\notmodels', r'\\not\\vDash', tex)
    # tex4ht loses the custom labels in enumitem's enumerate*; cenumerate renders fine:
    tex = re.sub(r'\\begin\{enumerate\*\}', r'\\begin{cenumerate}', tex)
    tex = re.sub(r'\\end\{enumerate\*\}', r'\\end{cenumerate}', tex)
    # Principle environments:
    tex = re.sub(r'\\principle\{([^}]+)\}\{([^}]+)\}', r'\\begin{equation}\\tag{\1}\2\\end{equation}', tex)
    tex = re.sub(r'\\begin{principles}', r'\\begin{enumerate}', tex)
    tex = re.sub(r'\\end{principles}', r'\\end{enumerate}', tex)
    tex = re.sub(r'\\pri\{([^}]+)\}\{(.+)\}', r'\\item[(\1)] $\2$', tex)
    tex = re.sub(r'\\pr\{([^}]+)\}', r'(\1)', tex)
    # Logic3-specific commands:
    # Allow up to two levels of nested braces in the argument, e.g.
    # \gn{\smallcaps{Prov}_T(\gn{A})} or \num{\gln{A}}.
    nested = r'(?:[^{}]|\{(?:[^{}]|\{[^{}]*\})*\})*'
    tex = re.sub(r'\\num\{(' + nested + r')\}', r'\\overline{\1}', tex)
    tex = re.sub(r'\\gn\{(' + nested + r')\}', r'\\ulcorner \1 \\urcorner', tex)
    tex = re.sub(r'\\dn\{(' + nested + r')\}', r'[\\![ \1 ]\\!]', tex)
    # Brackets:
    tex = re.sub(r'\\llbracket\b', r'⟦', tex)
    tex = re.sub(r'\\rrbracket\b', r'⟧', tex)
    # Substitutions that must NOT touch math regions
    # (\qed and \quad/\qquad are native to MathJax). Applied only outside math envs:
    tex = sub_outside_math(r'\\qed\b', r'QEDSYMBOL', tex)
    tex = sub_outside_math(r'\\q?quad\b', r'QUADSPACE', tex)
    return tex


def fix_math_columns(tex):
    """Fix tables using the custom C column type (math-mode columns).

    tex4ht doesn't handle the custom C column definition properly, so we
    replace C with c and wrap cell contents in $...$ where needed.
    """
    # Replace the specific table column spec that uses C
    tex = re.sub(r'\\begin\{tabular\}\{c \*\{4\}\{C\} C\}',
                 r'\\begin{tabular}{c *{4}{c} c}', tex)
    # Wrap bare math content in the table cells (like x_{1,0})
    tex = re.sub(r'& (x_\{[^}]+\}) &', r'& $\1$ &', tex)
    tex = re.sub(r'& (x_\{[^}]+\}) &', r'& $\1$ &', tex)  # run twice to catch adjacent
    tex = re.sub(r'& (\d) &', r'& $\1$ &', tex)
    tex = re.sub(r'& (\\cdots) ', r'& $\1$ ', tex)
    tex = re.sub(r'& (\\vdots) &', r'& $\1$ &', tex)
    return tex


def fix_smallcaps_in_math(tex):
    r"""Replace \smallcaps{} inside math with scriptstyle uppercase text.

    MathJax has correct metrics for \scriptstyle, so layout is accurate.
    """
    def repl_in_math(m):
        return re.sub(
            r'\\smallcaps\{([^}]*)\}',
            lambda s: '{\\scriptstyle \\class{smallcaps}{\\text{' + s.group(1).upper() + '}}}',
            m.group(0)
        )
    return _MATH_REGION.sub(repl_in_math, tex)


def fix_math_line_spacing(tex):
    """Add extra row spacing in display math environments for HTML rendering.

    Replaces \\\\ (row break) with \\\\[0.5em] so MathJax row spacing better
    matches the surrounding text line height. Skips \\\\ that already carry
    explicit spacing (\\\\[...]) or a star (\\\\*).
    """
    def add_spacing(m):
        return re.sub(r'\\\\(?![\[*])', r'\\\\[0.5em]', m.group(0))
    # Only display math; inline math doesn't use \\\\ for row breaks
    display = re.compile(
        r'\\\[.*?\\\]|\$\$.*?\$\$|'
        r'\\begin\{(equation\*?|align\*?|flalign\*?|gather\*?|multline\*?|eqnarray\*?)\}'
        r'.*?\\end\{\1\}',
        re.DOTALL,
    )
    return display.sub(add_spacing, tex)


def fix_gather(tex):
    """Replace gather environments with flalign to enforce left alignment."""
    pattern = re.compile(r'\\begin{gather(\*?)}(.*?)\\end{gather\*?}', re.DOTALL)

    def repl(match):
        environ = 'flalign*' if match.group(1) else 'flalign'
        body = match.group(2).strip()
        body = re.sub(r'^(.*?)(\\\\|$)', r'\\quad & \1 &\2', body, flags=re.MULTILINE)
        return f'\\begin{{{environ}}}\n{body}\n\\end{{{environ}}}'

    return pattern.sub(repl, tex)


def escape_labeled_items(tex):
    r"""
    Escape labeled \item to preserve the label.

    I sometimes use '\item[(*)] Principle' to label a Principle. make4ht turns
    this into a list item with a bullet point. We want to preserve the label.

    \item[(*)] Principle => \item[(*)] ITEMLABEL(*)ENDITEMLABEL Principle
    """
    tex = re.sub(r'\\item\[(.+?)\]', r'\\item[\1] ITEMLABEL\1ENDITEMLABEL', tex)
    return tex


def escape_intext_links(tex):
    r"""Insert content to restore links to definitions and observations etc.

    make4ht doesn't find links to tcolorbox definitions. So we do this:
    \begin{definition}{Basic Model}{basicmodel} =>  \begin{definition}{Basic Model ANCHORdef:basicmodelENDANCHOR}{basicmodel}
    \ref{def:basicmodel} => REFdef:basicmodelENDREF
    \begin{observation}{replacement-theorem} => \begin{observation}{replacement-theorem} ANCHORobs:replacement-theoremENDANCHOR
    \ref{obs:replacement-theorem} => REFobs:replacement-theoremENDREF

    We also replace references to page numbers:
    blahblah.\label{claim:replacement} blah => blahblah.ANCHORclaim:replacementENDANCHOR blah
    'on p.\ \pageref{table:systems}' => 'PAGEREFtable:systemsENDPAGEREF' => <a...>here</a>
    'on page \pageref{table:systems}' => 'PAGEREFtable:systemsENDPAGEREF' => <a...>here</a>
    'from page \pageref{table:systems}' => 'PAGEREFtable:systemsENDPAGEREF' => <a...>here</a>
    """
    tex = re.sub(r'\\begin{definition}\{(.*)\}\{([^}]+)\}', r'\\begin{definition}{\1 ANCHORdef:\2ENDANCHOR}{\2}', tex)
    tex = re.sub(r'\\ref\{def:([^}]+)\}', r'REFdef:\1ENDREF', tex)
    tex = re.sub(r'\\begin{observation}\{([^}]+)\}', r'\\begin{observation}{\1} ANCHORobs:\1ENDANCHOR', tex)
    tex = re.sub(r'\\ref\{obs:([^}]+)\}', r'REFobs:\1ENDREF', tex)
    # Theorem-like envs from header-boxes.tex (\newtcbtheorem-defined):
    for env, prefix in [('lemma', 'lem'), ('theorem', 'thm'),
                        ('proposition', 'prop'), ('corollary', 'cor')]:
        tex = re.sub(
            r'\\begin{' + env + r'}\{(.*)\}\{([^}]+)\}',
            r'\\begin{' + env + r'}{\1 ANCHOR' + prefix + r':\2ENDANCHOR}{\2}',
            tex
        )
        tex = re.sub(
            r'\\ref\{' + prefix + r':([^}]+)\}',
            r'REF' + prefix + r':\1ENDREF',
            tex
        )
    # page number references:
    tex = re.sub(r'\\label\{([^}]+)\}', r'\\label{\1}ANCHOR\1ENDANCHOR', tex)
    tex = re.sub(r'(?:on|from|at)\s+(?:p\.|page)\\?\s+\\pageref\{([^}]+)\}', r'PAGEREF\1ENDPAGEREF', tex)
    return tex


def restore_intext_links():
    """Restore links to definitions and observations etc.

    <p> Definition 1.2: Basic Model ANCHORdef:basicmodelENDANCHOR</p>
    <p>See REFdef:basicmodelENDREF</p>
    <p> Observation 1.1:</p></div><div class="tcolorbox-content"><p>ANCHORobs:semantic-deduction-theoremENDANCHOR

    Also links to pages:
    <p>blahblah.ANCHORclaim:replacementENDANCHOR blah</p>
    <p>'we saw this PAGEREFclaim:replacementENDPAGEREF'</p>
    """
    from pprint import pprint
    anchors = {}  # 'def:basicmodel' => ('02-models.html', '2.2')
                  # 'claim:replacement' => ('02-models.html', '')
    # First build the anchors dictionary
    for htmlfile in html_files():
        html = read_file(html_path + '/' + htmlfile)

        def extract_anchor(match):
            anchors[match.group(2)] = (htmlfile, match.group(1))
            definition_text = match.group(0).split('ANCHOR')[0].strip().rstrip(':')
            return definition_text + '<a id="' + match.group(2) + '"></a>'

        pattern = r"""
        (?:Definition|Observation|Lemma|Theorem|Proposition|Corollary)
        \s*([\d\.]+)              # chapter and section number
        [^<]*?                    # optional text like ': Basic Model '
        (?:<\s*\/?[^>]+>\s*)*     # optional tags, but no text in between
        ANCHOR(.+?)ENDANCHOR
        """
        html = re.sub(pattern, extract_anchor, html, flags=re.DOTALL|re.VERBOSE)
        # simple pageref anchors:
        html = re.sub(r'()ANCHOR(.+?)ENDANCHOR', extract_anchor, html)
        write_file(html_path + '/' + htmlfile, html)

    pprint(anchors)

    # Now replace the link placeholders
    for htmlfile in html_files():
        html = read_file(html_path + '/' + htmlfile)

        def replace_ref(match, pageref=False, link=True):
            if match.group(1) not in anchors:
                print('Missing anchor:', match.group(1))
                return '??'
            filename, num = anchors[match.group(1)]
            if pageref:
                num = 'here'
            if not link:
                return num
            return f'<a class="locallink" href="{filename}#{match.group(1)}">{num}</a>'

        def sub_refs_html_aware(html):
            """Replace REF placeholders, emitting bare numbers inside math blocks."""
            out = []
            last = 0
            for m in _HTML_MATH_REGION.finditer(html):
                out.append(re.sub(r'REF(.+?)ENDREF', replace_ref, html[last:m.start()]))
                math = re.sub(r'REF(.+?)ENDREF',
                               lambda r: replace_ref(r, link=False), m.group(0))
                out.append(math)
                last = m.end()
            out.append(re.sub(r'REF(.+?)ENDREF', replace_ref, html[last:]))
            return ''.join(out)

        html = sub_refs_html_aware(html)
        html = re.sub(r'PAGEREF(.+?)ENDPAGEREF', lambda m: replace_ref(m, True), html)
        write_file(html_path + '/' + htmlfile, html)


def make4ht(verbose=False):
    """Run make4ht to create HTML."""
    # with open(tmp_path+ "/href_db", mode="wt") as f:
    #     json.dump(hrefdb, f)

    tex4ht_options = [
        '2',   # split at chapter level
        # 'nominitoc',  # don't include tables of contents in each chapter
        # 'sec-filename',  # use filenames based on chapter titles
        # 'mathml',  # use MathML for math -- throws errors
        'mathjax',  # use MathJax as fallback
        'tikz',  # convert TikZ diagrams to SVG
        'enumerate+',  # enumerated list elements that keep the list couter value
        'fn-in',  # footnotes on each html page
    ]
    command = (
        f'cd {tmp_path} && '  # Change directory to the temporary path
        'make4ht '  # Call make4ht
        f'{"-a debug " if verbose else ""}'
        '-c mytex4ht.cfg '  # configuration file
        '--xetex '  # Use XeLaTeX engine for processing
        '--utf8 '  # Ensure UTF-8 encoding is used
        '-f html5 '  # Use HTML5 output format
        'logic3.tex '  # Main input file
        f'"{",".join(tex4ht_options)}" '  # tex4ht options
        f'-d ../{html_path} '  # Output directory
        '&& cd -'  # Return to the original directory
    )
    print(command)
    result = subprocess.run(command, shell=True, check=False, text=True)
    if result.stdout:
        print(result.stdout)
    if result.returncode != 0:
        print("Command failed with exit status", result.returncode)
        if result.stderr:
            print(result.stderr)
        # exit(1)


def save_or_restore_make4ht_output(restore=False):
    """
    Save output of make4ht to allow fake runs for debugging.

    We copy the html output of make4ht to a subdirectory of tmp_path. If fake is
    True, we instead copy the saved output back to html_path.
    """
    if not restore:
        shutil.copytree(html_path, tmp_path + '/html')
    else:
        # keep logic3.css!
        shutil.copyfile(html_path + '/logic3.css', tmp_path + '/html/logic3.css')
        shutil.rmtree(html_path)
        shutil.copytree(tmp_path + '/html', html_path)


def rename_html_files():
    """Rename HTML files to match chapter filenames."""
    mapping = {}
    mapping['logic3li1.html'] = 'toc.html'
    # Rename 'logic3ch1.html' to '01-propcal.html', etc.:
    tex_chapters = tex_files()
    for f in os.listdir(html_path):
        m = re.search(r'logic3ch(\d+).*\.html', f)
        if m:
            chapter_num = m.group(1)
            if len(chapter_num) == 1:
                chapter_num = '0' + chapter_num
            try:
                chapter_file = next(ch for ch in tex_chapters if ch.startswith(chapter_num))
                new_name = chapter_file.replace('.tex', '.html')
                mapping[f] = new_name
            except StopIteration:
                print("No chapter file found for", f)
    for old, new in mapping.items():
        print("Renaming", old, "to", new)
        shutil.move(html_path + '/' + old, html_path + '/' + new)
    adjust_links(mapping)


def adjust_links(mapping):
    """Adjust links in HTML files."""
    for htmlfile in os.listdir(html_path):
        if not htmlfile.endswith('.html'):
            continue
        html = read_file(html_path + '/' + htmlfile)
        # Sort by key length descending to avoid partial replacements
        for old, new in sorted(mapping.items(), key=lambda x: len(x[0]), reverse=True):
            html = html.replace(old, new)
        write_file(html_path + '/' + htmlfile, html)


def fix_toc_links():
    """Fix broken TOC links to chapter sections."""
    # We also make the local link names nicer. So we first extract all section headings from all chapters:
    mapping = {}
    for htmlfile in html_files():
        html = read_file(html_path + '/' + htmlfile)
        # <h3 class="sectionHead"><span class="titlemark">2.1</span><a id="x5-100002.1"></a>
        # <h3 class="sectionHead"><span class="titlemark">2.1</span><a id="x5-100002.1"></a>The possible-worlds analysis of possibility and necessity</h3>
        m = re.findall(r'<h3 class="sectionHead"><span[^>]*>([^<]+)</span>\s*<a\s+id="([^"]+)">', html)
        for num, old_id in m:
            new_id = 'sec-' + num.strip().replace('.', '-')
            print("Replacing", old_id, "with", new_id)
            mapping[old_id] = new_id
        # fix toc links:
        # <span class='sectionToc'><span class='ec-lmr-10x-x-109'>1.4  </span><a href='logic2ch1.html#duality' id='QQ2-4-8'><span class='ec-lmr-10x-x-109'>Duality</span></a></span>
        m = re.findall(r"class='sectionToc'><span.+?>(.+?) +</span><a href='(.+?)#(.+?)'", html)
        for num, filename, old_hash in m:
            old_name = filename + '#' + old_hash
            new_name = filename + '#sec-' + num.replace('.', '-')
            print("Replacing", old_name, "with", new_name)
            mapping[old_name] = new_name
        # <span class='chapterToc'><span class='ec-lmr-10x-x-109'>1 </span><a href='01-operators.html#modal-operators' id='QQ2-4-4'><span class='ec-lmr-10x-x-109'>Modal Operators</span></a></span>
        m = re.findall(r"class='chapterToc'>.+<a href='(.+?)#(.+?)'", html)
        for filename, old_hash in m:
            old_name = filename + '#' + old_hash
            print("Replacing", old_name, "with", filename)
            mapping[old_name] = filename
    adjust_links(mapping)


def fix_html():
    """Fix HTML files after conversion."""
    restore_intext_links()
    for htmlfile in html_files():
        html = read_file(html_path + '/' + htmlfile)
        html = remove_comments(html)
        html = embed_in_template(html, htmlfile)
        html = fix_tcolorboxes(html, htmlfile)
        html = fix_exercise_titles(html)
        html = fix_item_labels(html)
        html = fix_turingtape_html(html)
        html = fix_layout(html)
        validate_html(html, htmlfile)
        write_file(html_path + '/' + htmlfile, html)


def fix_turingtape_html(html):
    """Replace TTAPESTART…TTAPEEND markers with HTML tape cells."""
    def render(mode, content, pos):
        cells = [c.strip() for c in content.split(',')]
        try:
            highlight = int(pos)
        except ValueError:
            highlight = -1
        spans = []
        for i, c in enumerate(cells):
            cls = 'turingtape-cell'
            if i == highlight:
                cls += ' turingtape-highlight'
            inner = c if c else '&nbsp;'
            spans.append(f'<span class="{cls}">{inner}</span>')
        cells_html = ''.join(spans)
        if mode == 'I':
            return f'<span class="turingtape-inline">{cells_html}</span>'
        left = '…' if mode in ('D', 'Dl') else ''
        right = '…' if mode in ('D', 'Dr') else ''
        return (f'<span class="turingtape-display">{left}'
                f'<span class="turingtape">{cells_html}</span>{right}</span>')

    return re.sub(
        r'TTAPESTART\|(D[lr-]?|I)\|([^|]+)\|(\d+)\|TTAPEEND',
        lambda m: render(m.group(1), m.group(2), m.group(3)),
        html,
    )


def remove_comments(html):
    """Remove comments from HTML."""
    return re.sub(r'<!--.+?-->', '', html, flags=re.DOTALL)


def embed_in_template(html, filename):
    """Embed HTML files in template."""
    template = read_file('html_template.html')
    template = template.replace('{{year}}', str(datetime.datetime.now().year))
    toc = read_toc()
    template = template.replace('{{toc}}', '\n'.join(toc))
    body = re.split(r'<body\s*>', html, maxsplit=1)[1].rsplit('</body')[0]
    body = re.sub(r'<div class=.crosslinks.>.+?</div>', '', body, flags=re.DOTALL)
    # insert link to next chapter:
    chapter_toc = (t for t in toc if 'chapterToc' in t)
    try:
        next(t for t in chapter_toc if filename in t)
        next_link = next(chapter_toc)
        body += f'<div class="nextchapter">Next chapter: {next_link}</div>'
    except StopIteration:
        pass
    template = template.replace("{{content}}", body)
    title = 'Logic, Computability, and Incompleteness'
    m = re.search(r'<h2 class=.chapterHead[^>?]+>(.+)</h2>', body, flags=re.DOTALL)
    if m:
        title += ' | ' + re.sub(r'<[^>]+>', '', m.group(1))
    template = template.replace("{{title}}", title)
    return template


def read_toc():
    """Return TOC as list of <a>s."""
    toc_html = read_file(html_path + '/toc.html')
    toc_links = re.findall(r'<span class=.(chapterToc|sectionToc).><span[^>]*>([\d.]*)\s*</span><a href=.([^"\']+).><span[^>]*>([^<]+)</span></a></span>', toc_html)
    toc = [f'<a class="{level}" href="{href}">{num} {name}</a>' for level, num, href, name in toc_links]
    if len(toc) == 0:
        print("TOC not found in toc.html")
    return toc


def fix_item_labels(html):
    r"""Fix item labels that were escaped in LaTeX.

    <li> ITEMLABEL(*)ENDITEMLABEL => <li class="nobullet"><span class="itemlabel">(*)</span>
    """
    html = re.sub(r'<li[^>]*>\s*(?:<p[^>]*>)?\s*ITEMLABEL(.+?)ENDITEMLABEL',
                  r'<li class="nobullet"><span class="itemlabel">\1</span>',
                  html, flags=re.DOTALL)
    # remove ITEMLABEL(*)ENDITEMLABEL accidentally inserted into other kinds of items:
    html = re.sub(r'ITEMLABEL.+?ENDITEMLABEL', '', html)
    # remove orphaned </p> tags before </li> (left behind when opening <p> was removed above)
    html = re.sub(r'\s*</p>\s*(</li>)', r'\1', html)
    return html


def fix_layout(html):
    """Fix layout issues in HTML."""
    html = fix_mathjax_linebreaks(html)
    # Convert QUADSPACE placeholder to em space:
    html = re.sub(r'QUADSPACE', r'&emsp;', html)
    # remove anchors in lists that add a linebreak:
    html = re.sub(r'(<li class=.enumerate.[^>]*>)\s*<a\s+id=.[^\'"]+[\'"]></a>', r'\1', html)
    # strip trailing whitespace before </p> so justify does not stretch the last line:
    html = re.sub(r'\s+</p>', '</p>', html)
    # remove whitespace before section titles:
    html = re.sub(r'(<span class=.titlemark.>.+?</span>) *', r'\1', html)
    # widen too narrow tex, e.g. in $\Kn\!\neg\!\Kn\!\neg p$
    html = re.sub(r'\\!\s*\\', r'\\', html)
    # remove \hspace{-xxx} from math elements:
    html = re.sub(r'\\hspace\s*\{[^}]+\}', '', html)
    # remove empty table rows:
    html = re.sub(r'<tr>\s*<td[^>]*>\s*</td>\s*</tr>', '', html)
    # QED symbol, right-aligned:
    html = re.sub(r'QEDSYMBOL', r'<span class="qed">□</span>', html)
    return html


def fix_mathjax_linebreaks(html):
    r"""
    Fix linebreaks after mathjax elements.

    mathjax turns '... \( x \);' into '...</mjx-container>;' and nothing
    prevents a line break just before the semicolon. We don't want a line break
    there, so we wrap '\( x \);' in a no-wrap span.
    """
    html = re.sub(r'(\\\((?:[^\\)]|\\[^)])+\\\)[;.,?!\)])', r'<span class="nowrap">\1</span>', html)
    # Also keep an opening curly quote glued to the math it introduces
    # (and the closing quote, if present): ‘\(...\)’
    html = re.sub(r'(‘\\\((?:[^\\)]|\\[^)])+\\\)’?)', r'<span class="nowrap">\1</span>', html)
    # Glue a standalone opening bracket math element to the next token,
    # and a standalone closing bracket math element to the preceding token,
    # so a line break can't fall right next to ‘{’, ‘[’, ‘}’ or ‘]’.
    html = re.sub(r'(\\\(\\(?:\{|\[)\\\))(\s+[^\s<>]+)',
                  r'<span class="nowrap">\1\2</span>', html)
    html = re.sub(r'([^\s<>]+\s+)(\\\(\\(?:\}|\])\\\)[;.,?!\)]?)',
                  r'<span class="nowrap">\1\2</span>', html)
    return html


def validate_html(html, filename):
    """Validate HTML5 structure using html5lib and report issues."""
    parser = HTMLParser(namespaceHTMLElements=False)
    parser.parse(html)

    if parser.errors:
        print(f"WARNING: Validation issues in {filename}:")
        for (line, col), errorcode, datavars in parser.errors:
            message = constants.E.get(errorcode, errorcode)
            if isinstance(message, str) and datavars:
                try:
                    message = message % datavars
                except (TypeError, KeyError):
                    pass
            print(f"  Line {line}, Col {col}: {message}")


def fix_tcolorboxes(html, htmlfile):
    """
    Fix missing or excessive </div> closings in tcolorboxes.

    There are two problems.

    First, "tcolorbox document" divs in the answers chapter aren't properly
    closed: there's neither a closing tag for the <div class="tcolorbox
    document"> nor for the embedded <div class="tcolorbox-content"> or
    even divs inside that!

    Second, "tcolorbox proof" divs have an extra closing </div> at the end.

    Another minor issue, while we're here: the tcolorboxes for lemmas and
    theorems have class "tcolorbox tcolorbox", which makes them impossible to
    specifically style in the CSS. We change their class to "tcolorbox obs".
    """
    # Remove extra </div> after tcolorbox proof:
    html = re.sub(r'(class="tcolorbox proof".*?</div>\s*</div>)\s*</div>', r'\1', html, flags=re.DOTALL)

    # Close unclosed tcolorbox document divs in answers.html:
    if 'answers' in htmlfile:
        # Add </div></div> before each tcolorbox document to close the previous one:
        html = html.replace(
            '<div class="tcolorbox document"',
            '</div></div><div class="tcolorbox document"'
        )
        # Remove the first spurious </div></div> (the first tcolorbox has no previous to close):
        html = html.replace('</div></div><div class="tcolorbox document"', '<div class="tcolorbox document"', 1)
        # Close the last tcolorbox document before the footer:
        html = html.replace('<footer>', '</div></div><footer>')

    soup = BeautifulSoup(html, 'html.parser')  # auto-closes elements

    # Fix duplicate class "tcolorbox tcolorbox" -> "tcolorbox obs":
    for tbox in soup.find_all('div', class_='tcolorbox'):
        classes = tbox.get('class', [])
        if classes.count('tcolorbox') > 1:
            tbox['class'] = ['tcolorbox', 'obs']

    return str(soup)


def fix_exercise_titles(html):
    """Move exercise headings from content to title div."""
    html = re.sub(
        r'(class="tcolorbox exercise"[^>]*>)\s*<div class="tcolorbox-title">\s*</div>(\s*<div class="tcolorbox-content">.*?)<strong>([^<]+)</strong>\s*',
        r'\1<div class="tcolorbox-title">\3</div>\2',
        html,
        flags=re.DOTALL
    )
    return html


def create_index():
    """Create index.html."""
    html = read_file(html_path + '/toc.html')
    html = re.sub(r'<h2.+?</h2>', '', html)
    shutil.copyfile('doclicense.png', html_path + '/doclicense.png')
    write_file(html_path + '/index.html', html)


def check_links():
    """Check for missing link targets ('??')."""
    for htmlfile in html_files():
        html = read_file(html_path + '/' + htmlfile)
        if '??' in html:
            print("Missing link targets in", htmlfile)


def read_file(filename):
    """Read file and return contents."""
    with open(filename) as f:
        return f.read()


def write_file(filename, data):
    """Write data to file."""
    with open(filename, mode="wt") as f:
        f.write(data)


if __name__ == "__main__":
    main()
