# -*- coding: utf-8 -*-
"""
Created on Mon Jun  6 17:34:14 2022

@author: Jinhai
"""


class Base_layer(object):
    
    def __init__(self, **kwargs):
        
        for key, value in kwargs.items():
            setattr(self, key, value)
        
        