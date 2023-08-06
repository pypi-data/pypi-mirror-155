# -*- coding: utf-8 -*-
"""
Created on Wed Jun 15 09:22:33 2022

@author: Jinhai
"""

import numpy as np
import sys
from DigiNet.activations import Activations_sfw as Activations


class LSTM_sfw(Activations):
    
    def __init__(
            self,
            input_len,
            output_len,
            W_in = 'W_in.txt',
            W_rec = 'W_rec.txt',
            Bias = 'Bias.txt',
            activations = ['sigmoid', 'tanh'],
            **kwargs,
            ):
        
        try:
            self.W_in  = np.loadtxt(W_in)
            self.W_rec = np.loadtxt(W_rec)
            self.Bias  = np.loadtxt(Bias)
        except:
            print('Weight path is not correct!')
        
        super().__init__()
        
        self.input_len  = input_len
        self.output_len = output_len
        self.act_gate = self.get(activations[0])
        self.act_cell = self.get(activations[1])
        
        [self.W_f, self.W_g, self.W_i, self.W_o] = np.array([self.W_in]).reshape(4, self.output_len, self.input_len)
        [self.R_f, self.R_g, self.R_i, self.R_o] = np.array([self.W_rec]).reshape(4, self.output_len, self.output_len)
        [self.B_f, self.B_g, self.B_i, self.B_o] = np.array([self.Bias]).reshape(4, self.output_len)
    
        
    def forward(self, X):

        [t, dim] = np.shape(X)
        for i in range (t):
            if i == 0:
                h_ini = np.full(self.output_len, 0)
                c_ini = np.full(self.output_len, 0)
                self = self.SFE(c_ini, h_ini, X[i])
            else:
                self = self.SFE(self.c_out, self.h_out, X[i])
                
        return self, self.h_out
        
    
    def SFE(self, c_in, h_in, X_in):
        # time step one
        z_f = self.VMM(X_in, self.W_f, h_in, self.R_f, self.B_f)
        z_i = self.VMM(X_in, self.W_i, h_in, self.R_i, self.B_i)
        z_g = self.VMM(X_in, self.W_g, h_in, self.R_g, self.B_g)
        z_o = self.VMM(X_in, self.W_o, h_in, self.R_o, self.B_o)
        
        # time step two
        T_f = self.act_gate(z_f)
        T_i = self.act_gate(z_i)
        T_g = self.act_cell(z_g)
        T_o = self.act_gate(z_o)
        
        # time step three --> Hadamard Product
        P_f = self.Hadamard(c_in, T_f)
        P_ig = self.Hadamard(T_i, T_g)
        
        # time step four
        c_out = P_f + P_ig
        
        # time step five
        T_c = self.act_cell(c_out)
        
        # time step six
        h_out = self.Hadamard(T_c, T_o)
        
        # save parameters
        self.z_f, self.z_i, self.z_g, self.z_o = z_f, z_i, z_g, z_o
        self.T_f, self.T_i, self.T_g, self.T_o = T_f, T_i, T_g, T_o
        self.P_f, self.P_ig = P_f, P_ig
        self.c_out = c_out
        self.T_c = T_c
        self.h_out = h_out
        
        return self
    
    def VMM(self, X, W_in, h_in, W_rec, Bias):
        dim_in = np.shape(X)[0]
        dim_rec = np.shape(h_in)[0]
        if dim_in != np.shape(W_in)[1] or dim_rec != np.shape(W_rec)[1]:
            print("I/W dimension do not match")
            sys.exit()
        p1 = np.matmul(W_in, X)
        p2 = np.matmul(W_rec, h_in)
             
        return p1 + p2 + Bias
    
    
    def Hadamard(self, arr1, arr2):
        if np.size(arr1) != np.size(arr2):
            print("Dimension do not match")
            sys.exit()
        
        return arr1 * arr2
        