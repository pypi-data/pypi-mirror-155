from distutils.core import setup
from Cython.Build import cythonize
import numpy
import os


print('Getting into utils/setup.py')
c_path = os.path.abspath(os.path.dirname(__file__)) # string

print("Current Working Directory:" , os.getcwd())
print(c_path)

upper_path = os.path.dirname(c_path)
root_path = os.path.abspath(os.path.dirname(upper_path)) # string
print(root_path)
os.chdir(root_path)

print("Current Working Directory After Change:" , os.getcwd()) 

# ext_modules=cythonize('opencood/utils/box_overlaps.pyx'),

setup(
    name='box overlaps',
    ext_modules=cythonize(c_path + '/box_overlaps.pyx'),
    include_dirs=[numpy.get_include()]
)
