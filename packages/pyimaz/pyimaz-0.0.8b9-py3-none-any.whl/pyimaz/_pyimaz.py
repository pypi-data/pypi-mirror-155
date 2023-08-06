import os as _os
import numpy as np

def _get_imaz_chapman():
    _path = _os.path.join(_os.path.dirname(_os.path.abspath(__file__))
                          , "_ext", "_data", "chapman.txt")
    return np.loadtxt(_path, dtype=np.float32, unpack=True)

def _get_imaz_data_biases():
    _path = _os.path.join(_os.path.dirname(_os.path.abspath(__file__))
                          , "_ext", "_data", "data biases.txt")
    return np.loadtxt(_path, dtype=np.float32, unpack=True)
def _get_imaz_data_weights():
    _path = _os.path.join(_os.path.dirname(_os.path.abspath(__file__))
                          , "_ext", "_data", "data weights.txt")
    return np.loadtxt(_path, dtype=np.float32, unpack=True)
def _get_imaz_pressure():
    _path = _os.path.join(_os.path.dirname(_os.path.abspath(__file__))
                          , "_ext", "_data", "Imaz pressure.txt")
    return np.loadtxt(_path, dtype=np.float32)
def _get_imaz_nighttruequiet():
    _path = _os.path.join(_os.path.dirname(_os.path.abspath(__file__))
                          , "_ext", "_data", "nighttruequiet.txt")
    return np.loadtxt(_path, dtype=np.float32, unpack=True)
def _get_imaz_press_60deg():
    _path = _os.path.join(_os.path.dirname(_os.path.abspath(__file__))
                          , "_ext", "_data", "press_60deg.txt")
    return np.loadtxt(_path, dtype=np.float32)
def _get_imaz_press_70deg():
    _path = _os.path.join(_os.path.dirname(_os.path.abspath(__file__))
                          , "_ext", "_data", "press_70deg.txt")
    return np.loadtxt(_path, dtype=np.float32)


