# -*- coding: utf-8 -*-
import unicodedata

def unicode_line_folding(long_line, width, line_prifix=''): 
    lines = []
    if (width < 2):
        return lines 

    prifix_width = 0
    chr_width = lambda x: 2 if (unicodedata.east_asian_width(x) in ('F','W','A')) else 1

    if (line_prifix):
        for lp in line_prifix:
            prifix_width += chr_width(lp)

    start = end = 0 
    step = 0
    for uni_chr in long_line:
        end += 1
        cur_width = chr_width(uni_chr)
        step += cur_width
        if step > width - prifix_width:
            step = cur_width
            lines.append( line_prifix + long_line[start:end - 1])
            start = end - 1

    lines.append(line_prifix + long_line[start:end])
    return lines

