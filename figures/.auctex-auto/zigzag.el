;; -*- lexical-binding: t; -*-

(TeX-add-style-hook
 "zigzag"
 (lambda ()
   (TeX-add-symbols
    "N"
    "NN")
   (LaTeX-add-environments
    '("cenumerate" LaTeX-env-args ["argument"] 0)))
 :latex)

