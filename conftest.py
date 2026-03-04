import os
import sys
print(__file__)
print(os.path.dirname(__file__))
project_root = os.path.join(os.path.dirname(__file__), '...')
print("**PROJECT ROOT: ", project_root)
sys.path.insert(0, project_root)
print(sys.path)