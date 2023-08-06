from distutils.core import setup
from Cython.Build import cythonize
import numpy
import os

"""
print('Getting into utils/setup.py')
c_path = os.path.abspath(os.path.dirname(__file__)) # string
print("Current Working Directory:" , os.getcwd())
print(c_path)
os.chdir(c_path)
print("Current Working Directory After Change:" , os.getcwd()) 
"""
setup(
    name='box overlaps',
    ext_modules=cythonize('opencood/utils/box_overlaps.pyx'),
    include_dirs=[numpy.get_include()]
)
