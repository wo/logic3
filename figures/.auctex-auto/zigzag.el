;; -*- lexical-binding: t; -*-

(TeX-add-style-hook
 "zigzag"
 (lambda ()
   (TeX-add-to-alist 'LaTeX-provided-class-options
                     '(("standalone" "tikz" "border=5pt")))
   (TeX-add-to-alist 'LaTeX-provided-package-options
                     '(("tikz" "")))
   (TeX-run-style-hooks
    "latex2e"
    "standalone"
    "standalone10"
    "tikz")
   (TeX-add-symbols
    "N"
    "NN")
   (LaTeX-add-environments
    '("cenumerate" LaTeX-env-args ["argument"] 0)))
 :latex)

