# -*- coding: utf-8 -*-
"""
Created on Wed Jun 15 17:22:47 2022

@author: Jinhai
"""

import numpy as np

class Activations_sfw(object):
    
    def __init__(self, **kwargs):
        
        for key, value in kwargs.items():
            setattr(self, key, value)
            
            
    def sigmoid(self, num):
        
        return 1 / (1 + np.exp(-num))
    
    
    def tanh(self, num):
        
        return np.tanh(num)
    
    
    def linear(self, num):
        
        return num
    
    
    def get(self, identifier):
        
        if identifier is None:
            return self.linear
        
        if isinstance(identifier, (str, dict)):
            return eval('self.' + identifier)
        elif callable(identifier):
            return identifier
        else:
            raise TypeError(
                f"Could not interpret activation function identifier: {identifier}"
                )