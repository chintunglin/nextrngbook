# -*- coding: utf-8 -*-

import os
from setuptools import setup, Extension
from Cython.Build import cythonize
import numpy as np


extensions = [
    Extension(
        "nextrandom.dx_generator._dx_generator32",
        sources=[
            os.path.join("nextrandom", "dx_generator", "_dx_generator32.pyx"), 
            os.path.join("nextrandom", "dx_generator", "src", "dx_k_s_32.c")
        ],
        include_dirs=[
            np.get_include(),
            os.path.join(os.path.dirname(__file__), "nextrandom", "dx_generator", "src")
        ],
        define_macros=[("NPY_NO_DEPRECATED_API", "NPY_1_7_API_VERSION")]
    )
]

setup(
    name="nextrandom",
    ext_modules=cythonize(extensions, language_level="3str")
)


