import sys
import os

# Make sure that the application source directory (this directory's parent) is
# on sys.path.

srcfolder = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+'/src'
sys.path.insert(0, srcfolder)
