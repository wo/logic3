;; -*- lexical-binding: t; -*-

(TeX-add-style-hook
 "partition"
 (lambda ()
   (LaTeX-add-environments
    '("cenumerate" LaTeX-env-args ["argument"] 0)))
 :latex)

