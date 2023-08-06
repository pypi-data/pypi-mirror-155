import numpy as np

"""
Dictionary writing code, relies on base list zip procedure. 
Ensure that this is launched and run before anything that may interfere with this base python function. 
"""

def norm_dict(scale):
    """
    Generates dictionary of value and label for use within mapper2
    Used for non-transformed variables
    :param scale: input raw values that you wish to use as labels
    :return: returns dictionary associating value and a label
    """
    i = scale.copy()
    labels = [str(i) for i in i]
    values = list(i)
    return dict(zip(labels, values))

def log1p_dict(scale):
    """
    Generates dictionary of value and label for use within mapper 2
    Used for dependent variables that have been log1 transformed
    :param scale: input raw values that you wish to use as labels
    :return: returns dictionary associating value and a label, value is log1p transformation of input
    """
    i = scale.copy()
    labels = [str(i) for i in i]
    values = list(np.log1p(i))
    return dict(zip(labels, values))

def log2p_dict(scale):
    """
    Generates dictionary of value and label for use within mapper 2
    Used for dependent variables that have been log1 transformed twice
    :param scale: input raw values that you wish to use as labels
    :return: returns dictionary associating value and a label, value is log1p transformation twice of input
       """
    i = scale.copy()
    labels = [str(i) for i in i]
    values = list(np.log1p(np.log1p(i)))
    return dict(zip(labels, values))

"""
Standard dictionary stored for ease of access
"""
standard_scale_1p_2p= [0, 1, 3, 10, 30, 100, 300, 1000, 3000]
standard_scale = [0,100,300,1000,3000]
dictionary_stand = norm_dict(standard_scale)
dictionary_stand_1p = log1p_dict(standard_scale_1p_2p)
dictionary_stand_2p = log2p_dict(standard_scale_1p_2p)