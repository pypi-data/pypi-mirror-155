# -*- coding: utf-8 -*-
"""
Created on Fri Jun 17 15:21:30 2022

@author: Jinhai
"""

import numpy as np
import sys
from DigiNet.activations import Activations_sfw as Activations


class Dense_sfw(Activations):
    
    def __init__(
            self,
            input_len,
            output_len,
            W = 'W_fc.txt',
            Bias = 'Bias_fc.txt',
            activations = None,
            **kwargs,
            ):
        
        try:
            self.W  = np.loadtxt(W)
            self.Bias  = np.loadtxt(Bias)
        except:
            print('Weight path is not correct!')
            
        super().__init__()
        
        self.input_len  = input_len
        self.output_len = output_len
        self.act = self.get(activations)
        
        
    def forward(self, X):
        
        dim_in = np.shape(X)[0]
        if dim_in != np.shape(self.W)[1]:
            print("I/W dimension do not match")
            sys.exit()
            
        out = np.matmul(self.W, X) + self.Bias
        
        fc_out = self.act(out)
        
        self.fc_out = fc_out
        
        return self, self.fc_out