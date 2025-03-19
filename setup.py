# -*- coding: utf-8 -*-


import os
from setuptools import setup, Extension, find_packages
from Cython.Build import cythonize
import numpy as np


extensions = [
    Extension(
        "nextrandom.dx_generator._dx_generator32",
        sources=[
            os.path.join("src", "nextrandom", "dx_generator", "_dx_generator32.pyx"), 
            os.path.join("src", "nextrandom", "dx_generator", "src", "dx_k_s_32.c")
        ],
        include_dirs=[
            np.get_include(),
            os.path.join(os.path.dirname(__file__), "src", "nextrandom", "dx_generator", "src")
        ],
        define_macros=[("NPY_NO_DEPRECATED_API", "NPY_1_7_API_VERSION")]
    )
]

setup(
    name="nextrandom",
    packages=find_packages(where="src", 
                           exclude=["nextrandom.dx_generator.data", 
                                    "nextrandom.dx_generator.src"]),
    package_dir={'': 'src'},
    include_package_data=True,
    package_data={"nextrandom.dx_generator": ["data/*"]},
    ext_modules=cythonize(extensions, language_level="3str")
)