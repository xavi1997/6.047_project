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

DATA_DIR = "../data/all_data/EXAMPLE/CONVERTEDDATADIR/chr21_" # just add celltype, marker, and extension

def extract_cell_type_marks_avail():
    """
    returns mapping of {cell_type_num : {set of modifications available}}
    WORKING
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

def extract_wig_gz(filename, size = None):
    """
    WORKING
    filename must be .gz
    Outputs np 2D array with data all in one row
    """
    out = []
    i = 2 # trim first two rows that contain all the same info
    length = 0
    with gzip.open(filename) as f:
        for line in f:
            if i > 0:
                i -= 1
                continue
            out.append(float(line.strip())) # trim whitespace. Add datapoints as floats
            length += 1
            if size == length: # never happens if size is None
                break
        f.close()
    if size != None and length < size:
        raise RuntimeError("something weird happened. size input could be too big")
    return np.array([out])
    

def load_training_data(mod1, mod2, size = 100000):
    """
    Extract data from many files and put it all together. Split it in "bites" that
    fit as input of CNN. Should be numpy array of 2D arrays, each of which is an input
    
    inputs are 1xN, all of the same marker
    
    inputs for cnn are markers of mod1
    outputs are markers of mod2
    
    function returns: (inputs, outputs), for all cell_types that have both markers
    """
    inputs = []
    outputs = []
    cell_types = []
    cell_type_mods = extract_cell_type_marks_avail()
    for cell_type in cell_type_mods:
        if mod1 in cell_type_mods[cell_type] and mod2 in cell_type_mods[cell_type]:
            cell_types.append(cell_type)
    
    for cell_type in cell_types:
        input_filename = DATA_DIR + cell_type + "-" + mod1 + DATA_EXTENSION
        inputs.append(extract_wig_gz(input_filename, size = size))
        output_filename = DATA_DIR + cell_type + "-" + mod2 + DATA_EXTENSION
        outputs.append(extract_wig_gz(output_filename, size = size))
    
    return np.array(inputs), np.array(outputs)

#==============================================================================
# mod1 = "H3K27me3"
# mod2 = "H3K36me3"
# a = load_training_data(mod1, mod2)
# x = a[0][0][0]
# for num in x:
#     if num != .12:
#         print(num)
# print(a)
#==============================================================================