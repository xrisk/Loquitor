import imp
import os
import sys
from warnings import warn

scriptdir = os.path.dirname(__file__)

__all__ = []
for filename in os.listdir(scriptdir):
    if filename.startswith(".") or filename.startswith("_") or not filename.endswith(".py"):
        continue

    __all__.append(filename[:-3])

try:
    os.makedirs(os.path.join(os.path.expanduser("~"), ".loquitor"))
except OSError:
    warn("Could not create configuration folder.")

del imp, os, sys, scriptdir, filename
from . import *
