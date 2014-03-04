# Setup to generate .exe
from distutils.core import setup
import py2exe

setup(windows=["superconductor.py"])