# -*- coding: utf-8 -*-


# setup.py
from setuptools import setup, Extension
from Cython.Build import cythonize
import numpy as np


extensions = [
    Extension(
        "_pcg64tmwc",
        sources=["_pcg64tmwc.pyx", "src/pcg64tmwc.c"],
        include_dirs=[np.get_include()],
        define_macros=[("NPY_NO_DEPRECATED_API", "NPY_1_7_API_VERSION")]
    )
]

setup(
    name="_pcg64tmwc",
    ext_modules=cythonize(extensions, language_level="3str")
)


