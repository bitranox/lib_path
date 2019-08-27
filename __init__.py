try:
    from .lib_path import *
# this we need for pip install --install-option test
except ImportError:
    import lib_path
