# -*- coding: utf-8 -*-
"""
Created on Fri Jun 17 10:19:01 2022

@author: Jinhai
"""

import numpy as np
import sys
from DigiNet.activations import Activations_hdw as Activations


class Dense_hdw(Activations):
    
    def __init__(
            self,
            input_len,
            output_len,
            Quantization = [16,4],
            fract_width = 8,
            W = 'W_fc_Quant.txt',
            Bias = 'Bias_fc_Quant.txt',
            activations = None,
            **kwargs,
            ):
        
        try:
            self.W  = np.loadtxt(W, dtype='str')
            self.Bias  = np.loadtxt(Bias, dtype='str')
        except:
            print('Weight path is not correct!')
            
        super().__init__(Quant = Quantization)
        
        self.input_len  = input_len
        self.output_len = output_len
        self.fract_width = fract_width
        self.act = self.get(activations)
        
        
    def forward(self, X):
        
        dim_in = np.shape(X)[0]
        if dim_in != np.shape(self.W)[1]:
            print("I/W dimension do not match")
            sys.exit()
            
        out = np.zeros(self.output_len, dtype='int32')
        p1 = out.copy()
        dtype = self.Quant[0]
        
        for i in range(self.output_len):
            for j in range(self.input_len):
                p1[i] += int(self.W[i, j], dtype) * int(X[j], dtype) >> self.fract_width
            out[i] = p1[i] + int(self.Bias[i], dtype)
            
        fc_out = self.act(out)
        
        self.fc_out = fc_out
        
        return self, self.fc_out