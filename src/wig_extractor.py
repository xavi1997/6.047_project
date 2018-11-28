# -*- coding: utf-8 -*-
"""
Created on Tue Nov 27 17:58:53 2018

@author: luisxavierramostormo
"""

import numpy as np

def extract_wig(filename):
    """
    WORKING
    Outputs np 2D array with data all in one row
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
            
    return np.array([out])
    

def load_training_data():
    """
    Extract data from many files and put it all together. Split it in "bites" that
    fit as input of CNN. Should be numpy array of 2D arrays, each of which is an input
    
    
    """
    pass


print(extract_wig("../data/example_data/chr21_E001-H3K4me1.pval.signal.bedGraph.wig"))