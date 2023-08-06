# -*- coding: utf-8 -*-
"""
Created on Fri May 20 15:53:01 2022

@author: Bill Kuo
"""
from pipeline.steps.step import StepException

class Pipeline():
    def __init__(self, steps):
        self.steps = steps
        
    def run(self, inputs, utils):
        data = None

        for step in self.steps:
            try:
                data = step.process(data, inputs, utils)
                print(f'\nPipeline -> Step_Class: {step.__class__.__name__}\ntype: {type(data)}')
                
                try: print(f'Pipeline -> Data: {data.head(5)}\n')
                except: pass

            except StepException as e:
                print('pipeline_CF: Exception:', e)
                break
            