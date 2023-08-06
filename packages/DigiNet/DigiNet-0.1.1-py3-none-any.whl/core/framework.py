# -*- coding: utf-8 -*-
"""
Created on Sun Jun 19 11:25:55 2022

@author: Jinhai
"""

import numpy as np
from DigiNet.layers import LSTM_hdw, LSTM_sfw, Dense_hdw, Dense_sfw


class Framework():
    
    def __init__(self):
        
        self.Layers = []
        self.layer_base = tuple([LSTM_hdw, LSTM_sfw, Dense_hdw, Dense_sfw])
        
    def add(self, layer):
        
        if isinstance(layer, self.layer_base):
            self.Layers.append(layer)
        else:
            raise TypeError (
                "The added layer must be an instance of class Layer. "
                 f"Received: layer={layer} of type {type(layer)}."
                 )
            
    def evaluate(self, X):
        
        dim = np.size(self.Layers)
        out = []
        out.append(X)
        
        for i in range(dim):
            self.Layers[i], result = self.Layers[i].forward(out[i])
            out.append(result)
        
        self.out = out
        