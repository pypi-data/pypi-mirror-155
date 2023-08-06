# -*- coding: utf-8 -*-
"""
Created on Tue Jun 14 13:54:33 2022

@author: Jinhai
"""

import numpy as np
from DigiNet.preprocessing import Quantize

sigmoid_dic = {
    16:{
        4: [0x0200, 0x0000, 0x0100, 2],
        }
    }

tanh_dic = {
    16:{
        4: [0x009F, 0x01BA, -0x0100, 0x0058, 0x0068, 0x0100, 8],
        }
    }

class Activations_hdw(Quantize):
    
    def __init__(self, Quant):
        
        super().__init__(Quant = Quant)
        
        self.sigmoid_para = sigmoid_dic.get(Quant[0]).get(Quant[1])
        self.tanh_para = tanh_dic.get(Quant[0]).get(Quant[1])
        
        
    def sigmoid(self, num):
        
        [base, low, high, shift] = self.sigmoid_para
        
        out = num.copy()
        dim = np.size(num)
        
        for i in range (dim):
            out[i] = np.piecewise(num[i], 
                                  
                                  [num[i] < -base, num[i] > base, 
                                   -base <= num[i] <= base],
                                  
                                  [low, high, ((num[i] + base) >> shift)])
            
        return self.toQuant(out)
    
    
    def tanh(self, num):
        
        [margin_l, margin_h, low, slope, bias, high, shift] = self.tanh_para
        
        out = num.copy()
        dim = np.size(num)
        
        for i in range (dim):
            out[i] = np.piecewise(num[i], 
                                  
                                  [num[i] <= -margin_h, 
                                   -margin_h < num[i] <= -margin_l,
                                   -margin_l < num[i] < margin_l,
                                   margin_l <= num[i] < margin_h,
                                   num[i] >= margin_h],
                                  
                                  [low, 
                                   (slope * num[i] >> shift) - bias, 
                                   num[i], 
                                   (slope * num[i] >> shift) + bias, 
                                   high])
            
        return self.toQuant(out)
    
    
    def linear(self, num):
        
        return self.toQuant(num)
    
    
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