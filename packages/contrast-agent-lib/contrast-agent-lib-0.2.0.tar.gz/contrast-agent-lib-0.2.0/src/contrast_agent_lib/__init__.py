import ctypes

from sys import platform
from os import path

# TODO: PYT-2369 Wheel distributions will remove the need for this logic entirely
lib_name = "libcontrast_c"
if path.exists("/etc/alpine-release"):
    lib_name += "_musl"
lib_ext = ".dylib" if platform.startswith("darwin") else ".so"
lib_path = "".join([path.dirname(__file__), "/libs/", lib_name, lib_ext])

lib_contrast = ctypes.cdll.LoadLibrary(lib_path)
