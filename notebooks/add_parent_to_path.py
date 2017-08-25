import os
import sys

# Add parent directory so we can import ipy_table.
# Add it at the beginning of sys.path so that the local version is used rather than any installed version.
module_path = os.path.abspath(os.path.join('..'))
if module_path not in sys.path:
    sys.path.insert(0, module_path)