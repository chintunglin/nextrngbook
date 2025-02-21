# -*- coding: utf-8 -*-


# setup.py
from setuptools import setup, Extension
from Cython.Build import cythonize
import numpy as np


extensions = [
    Extension(
        "_dx_generator32",
        sources=["_dx_generator32.pyx", "src/dx_k_s_32.c"],
        include_dirs=[np.get_include()],
        define_macros=[("NPY_NO_DEPRECATED_API", "NPY_1_7_API_VERSION")]
    )
]

setup(
    name="_dx_generator32",
    ext_modules=cythonize(extensions, language_level="3str")
)


