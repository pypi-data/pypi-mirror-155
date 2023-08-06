from setuptools import find_packages, setup

PKG_NAME = "zeitgeber"

version = "0.0.1"

setup(
    name=PKG_NAME,
    version=version,
    description=(
        "A library with utils to work with circadian time timeseries and plot them"
    ),
    zip_safe=False,

)
