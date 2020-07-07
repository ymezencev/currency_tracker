

import os
import inspect
from inspect import getsourcefile
from os.path import abspath

print(os.getcwd())

print(os.path.dirname(os.path.abspath(__file__)))

print(abspath(getsourcefile(lambda: 0)))
print(abspath(inspect.getsourcefile(inspect.currentframe())))

from pathlib import Path
print(Path.home())
print(os.path.expanduser("~"))
print(os.environ['WINDIR'])
print(os.environ['HOMEDRIVE'])
