# -*- coding: utf-8 -*-
"""
Created on Wed May 18 10:45:26 2022

@author: Bill Kuo
"""
from abc import ABC
from abc import abstractmethod

class Step(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def process(self, data, inputs, utils):
        pass

class StepException(Exception):
    pass