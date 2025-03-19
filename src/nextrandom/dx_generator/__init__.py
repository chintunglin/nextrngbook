# -*- coding: utf-8 -*-


from ._dx_generator32 import _DXGenerator32
import csv
import os
import warnings
import random

__all__ = ["create_dx32", "get_dx32_id_table", "get_dx32_max_id"]


# read parameters
current_dir = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(current_dir, "data", "dx32_parameters.csv"), 
          "r", newline="") as dx32_csv:
    
    dx32_parameter_reader = csv.DictReader(dx32_csv, delimiter=",")
    
    _dx32_parameter_table = \
        {int(parameter.pop("dx32_id")): parameter for parameter in dx32_parameter_reader}

    _dx32_id_max = max(_dx32_parameter_table.keys())

del current_dir
del dx32_csv
del dx32_parameter_reader


def create_dx32(dx32_id=270, seed=None):
    """Return a _DXGenerator32 object.
    
    Args:
        dx32_id
        seed
        
    Returns:
        A _DXGenerator32 object.
    
    
    
    """
    
    if int(dx32_id) != dx32_id:
        raise ValueError(
            f"Invalid id: {dx32_id}. Must be an integer with int or float type "
            "(e.g., 270 or 270.0)."
        )
        
    if dx32_id < 0:
        raise ValueError(f"Invalid id: {dx32_id}. Must be non-negative.")
        
    if dx32_id > _dx32_id_max:
        
        random.seed(dx32_id)
        
        rand_id = random.randint(0, _dx32_id_max)
        
        warnings.warn(
            f"dx32_id {dx32_id} exceeds the maximum value {_dx32_id_max}. "
            f"For consistency, the id has been mapped to a fixed value within range: {rand_id}. "
            f"This value may be the same for different out-of-range ids. "
        )
        
        dx32_id = rand_id
    
    
    target_dx32_parameters = _dx32_parameter_table[dx32_id]
    
    target_dx32_parameters = \
        {key: float(value) for key, value in target_dx32_parameters.items()}
    
    return _DXGenerator32(target_dx32_parameters["bb"], 
                          target_dx32_parameters["pp"], 
                          target_dx32_parameters["kk"], 
                          target_dx32_parameters["ss"], 
                          target_dx32_parameters["log10(period)"],
                          seed)


def get_dx32_id_table():
    
    return _dx32_parameter_table


def get_dx32_max_id():
    
    return _dx32_id_max