# -*- coding: utf-8 -*-
"""
Created on Tue Nov 27 17:58:53 2018

@author: luisxavierramostormo
"""

import numpy as np
import gzip

# tells you which samples have which chromatin modification data
DATA_INFO_DIR = "../data/all_data/EXAMPLE/tier1_samplemarktable.txt"

# data of celltype C with modification H is stored in 
DATA_EXTENSION = ".pval.signal.bedGraph.wig.gz"

def extract_cell_type_marks_avail():
    """
    returns mapping of {cell_type_num : {set of modifications available}}
    """
    out = {}
    with open(DATA_INFO_DIR) as f:
        for line in f:
            line = line.replace("\t", " ")
            cell_type, modification, filename = line.split(" ")
            filename = filename.strip()
            if cell_type not in out:
                out[cell_type] = set()
            out[cell_type].add(modification)
        f.close()
            
    return out

def extract_wig(filename):
    """
    WORKING
    filename must be .gz
    Outputs np 2D array with data all in one row
    """
    out = []
    i = 2 # trim first two rows that contain all the same info
    with gzip.open(filename) as f:
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
    
    inputs are 1xN, all of the same marker
    """
    pass


print(extract_cell_type_marks_avail())