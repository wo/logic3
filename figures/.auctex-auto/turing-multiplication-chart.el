;; -*- lexical-binding: t; -*-

(TeX-add-style-hook
 "turing-multiplication-chart"
 (lambda ()
   (LaTeX-add-environments
    '("cenumerate" LaTeX-env-args ["argument"] 0)))
 :latex)

