;; -*- lexical-binding: t; -*-

(TeX-add-style-hook
 "turing-loop-chart"
 (lambda ()
   (LaTeX-add-environments
    '("cenumerate" LaTeX-env-args ["argument"] 0)))
 :latex)

