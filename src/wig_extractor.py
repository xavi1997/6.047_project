# -*- coding: utf-8 -*-
"""
Created on Tue Nov 27 17:58:53 2018

@author: luisxavierramostormo
"""

def extract_wig(filename):
    """
    WORKING
    """
    out = []
    i = 2 # trim first two rows that contain all the same info
    with open(filename) as f:
        for line in f:
            if i > 0:
                i -= 1
                continue
            out.append(float(line.strip())) # trim whitespace. Add datapoints as floats
        f.close()
            
    return out


# print(extract_wig("chr21_E001-H3K4me1.pval.signal.bedGraph.wig"))