# -*- coding: utf-8 -*-
# MIT License
# Copyright (c) 2025 chintunglin

"""Provides an interface for generating `_DXGenerator` objects from `dx_id` values.

Provides an end-user interface for generating `_DXGenerator` objects 
based on `dx_id` values. It also allows users to access the internal table of `dx_id` 
values and their parameters, as well as retrieve the maximum allowed `dx_id`.
 
The `dx_id_table` is organized such that each `dx_id` corresponds to a 
unique set of parameters. The `dx_id` values are assigned in ascending 
order based on the `log10(period)` value of the parameters.

Examples:
    >>> from nextrngbook.dx_generator import create_dx
    >>> create_dx()
    _DXGenerator(
        bb=1016882, pp=2146123787, kk=50873, ss=2, log10_period=474729.3125
    )
    >>> from nextrngbook import dx_generator
    >>> dx_id_table = dx_generator.get_dx_id_table()
    >>> print(dx_id_table)
    {0: {'kk': '2', 'ss': '1', 'bb': '32693', 'pp': '2147483249', 'log10(period)': '18.7'}, 
     1: {'kk': '2', 'ss': '1', 'bb': '32710', 'pp': '2147483249', 'log10(period)': '18.7'},
     ...}
    >>> max_dx_id = dx_generator.get_dx_max_id()
    >>> print(max_dx_id)
    4194

**Functions:**

- `create_dx(dx_id, seed=None)` - Returns a `_DXGenerator` object 
    generated from the internal parameters.
- `get_dx_id_table()` - Returns the internal table of `dx_id` values 
    and their associated parameters.
- `get_dx_max_id()` - Returns the maximum allowed `dx_id` value.

**Type Aliases:**
    
- `SeedType` - Type alias for valid seed input types. Can be `None`, `int`, 
`NDArray[np.integer]`, `SeedSequence`, or a sequence of integers.
"""

from ._dx_generator32 import _DXGenerator
import csv
import os
import warnings
import random
import numpy as np
from numpy.typing import NDArray
from numpy.random import SeedSequence
from typing import Union, Sequence

__all__ = ["create_dx", "get_dx_id_table", "get_dx_max_id"]

SeedType = Union[None, int, NDArray[np.integer], SeedSequence, Sequence[int]]

# read parameters
current_dir = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(current_dir, "data", "dx32_parameters.csv"), 
          "r", newline="") as dx32_csv:
    
    dx32_parameter_reader = csv.DictReader(dx32_csv, delimiter=",")
    
    _dx32_parameter_table = \
        {int(parameter.pop("dx_id")): parameter for parameter in dx32_parameter_reader}

    _dx32_id_max = max(_dx32_parameter_table.keys())

del current_dir
del dx32_csv
del dx32_parameter_reader


def create_dx(dx_id: Union[float, int] = 4194, 
              seed: SeedType = None) -> _DXGenerator:
    """Returns a `_DXGenerator` object generated from the internal parameters.
    
    Retrieves the corresponding parameters from the internal table based on 
    the given `dx_id`, and then returns the corresponding `_DXGenerator` object
    based on these parameters.
    
    If `dx_id` exceeds the maximum allowed value, it is mapped to a fixed value 
    within the valid range, with the specific mapping depending on the given 
    `dx_id`. Regardless of whether `dx_id` is within the valid range or has
    been mapped, the function will always return the generated object with the 
    same parameter settings for the same `dx_id` on every call.
    
    The maximum allowed `dx_id` value can be retrieved using the function 
    `get_dx_max_id`. To inspect the full table of `dx_id` values and their 
    corresponding parameters, use the function `get_dx_id_table`.

    
    Args:
        dx_id: A non-negative integer representing the identifier used to 
            retrieve the corresponding parameters from the internal table.
        seed: A value used to initialize the random number generator. If None, 
            fresh and unpredictable entropy will be retrieved from the OS. 
            If an int or array-like of integers is provided, it will be passed 
            to `SeedSequence` to set the initial state of the BitGenerator. 
            Alternatively, a `SeedSequence` instance can also be used directly. 
            This function uses the same seeding mechanism as NumPy's random system.
        
    Examples:
        >>> create_dx()
        _DXGenerator(
            bb=1016882, pp=2146123787, kk=50873, ss=2, log10_period=474729.3125
        )
        >>> create_dx(dx_id=4000)
        _DXGenerator(
            bb=1046381, pp=2147472413, kk=1301, ss=2, log10_period=12140.7998046875
        )
    """
    
    if int(dx_id) != dx_id:
        raise ValueError(
            f"Invalid id: {dx_id}. Must be an integer with int or float type "
            "(e.g., 270 or 270.0)."
        )
        
    if dx_id < 0:
        raise ValueError(f"Invalid id: {dx_id}. Must be non-negative.")
        
    if dx_id > _dx32_id_max:
        
        random.seed(dx_id)
        
        rand_id = random.randint(0, _dx32_id_max)
        
        warnings.warn(
            f"dx_id {dx_id} exceeds the maximum value {_dx32_id_max}. "
            f"For consistency, the id has been mapped to a fixed value within range: {rand_id}. "
            f"This value may be the same for different out-of-range ids. "
        )
        
        dx_id = rand_id
    
    
    target_dx32_parameters = _dx32_parameter_table[dx_id]
    
    target_dx32_parameters = \
        {key: float(value) for key, value in target_dx32_parameters.items()}
    
    return _DXGenerator(target_dx32_parameters["bb"], 
                        target_dx32_parameters["pp"], 
                        target_dx32_parameters["kk"], 
                        target_dx32_parameters["ss"], 
                        target_dx32_parameters["log10(period)"], 
                        seed)


def get_dx_id_table() -> dict:
    """Returns the internal table of `dx_id` values and their associated parameters."""
    return _dx32_parameter_table


def get_dx_max_id() -> int:
    """Returns the maximum allowed `dx_id` value."""
    return _dx32_id_max