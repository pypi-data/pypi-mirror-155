# -*- coding: utf-8 -*-
"""
Created on Fri Jun 17 10:36:26 2022

@author: Jinhai
"""

import numpy as np


class Quantize(object):
    
    def __init__(self, Quant):
        
        self.Quant = Quant
        
    
    def toQuant(self, array):
        
        if self.Quant[0] == 16:
            return tuple([hex(m) for m in array])
        
        elif self.Quant[0] == 8:
            return tuple([oct(m) for m in array])
        
        elif self.Quant[0] == 2:
            return tuple([bin(m) for m in array])
        
        else:
            print('Quantization not valid')