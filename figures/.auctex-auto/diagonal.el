;; -*- lexical-binding: t; -*-

(TeX-add-style-hook
 "diagonal"
 (lambda ()
   (TeX-add-symbols
    "N")
   (LaTeX-add-environments
    '("cenumerate" LaTeX-env-args ["argument"] 0)))
 :latex)

