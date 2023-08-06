# -*- coding: utf-8 -*-
"""
Created on Thu May 26 09:33:40 2022

@author: user
"""

from .step import Step

class Preflight(Step):
    def process(self, data, inputs, utils):
        utils.create_dirs() # build log file
        
        return data


