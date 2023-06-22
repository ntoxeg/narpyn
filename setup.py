from setuptools import Extension, setup

c_extension = Extension("my_c_module", sources=["my_c_module.c"])

setup(
    ext_modules=[c_extension],
)
