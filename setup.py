#! /usr/bin/env python
from distutils.core import setup, Extension

m = Extension("baseutils",
        sources=["baseutils.c"],
        extra_compile_args=["-O3"])

setup(name = "baseutils", description = "baseutils for python27",
        ext_modules = [m])
