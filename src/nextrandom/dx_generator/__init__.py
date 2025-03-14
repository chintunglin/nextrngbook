# -*- coding: utf-8 -*-


from ._dx_generator32 import _DXGenerator32
import csv
import os

current_dir = os.path.dirname(os.path.abspath(__file__))

__all__ = ["create_dx32"]


# read parameters
with open(os.path.join(current_dir, "data", "dx32_parameters.csv"), 
          "r", newline="") as dx32_csv:
    
    dx32_parameter_reader = csv.DictReader(dx32_csv, delimiter=",")
    
    dx32_parameter_table = \
        {int(parameter.pop("dx32_id")): parameter for parameter in dx32_parameter_reader}


def create_dx32(dx32_id=270, seed=None):
    
    dx32_id = int(dx32_id) # to ensure data type
    
    target_dx32_parameters = dx32_parameter_table[dx32_id]
    
    target_dx32_parameters = {key: float(value) \
                                  for key, value in target_dx32_parameters.items()}
        
    dx32_parameter_table[dx32_id] = target_dx32_parameters
    
    return _DXGenerator32(target_dx32_parameters["bb"], 
                          target_dx32_parameters["pp"], 
                          target_dx32_parameters["kk"], 
                          target_dx32_parameters["ss"], 
                          target_dx32_parameters["log10(period)"],
                          seed)