import sys
from setuptools import find_packages, setup
import re

CURRENT_PYTHON = sys.version_info[:2]
REQUIRED_PYTHON = (3, 7)
if CURRENT_PYTHON < REQUIRED_PYTHON:
    sys.stderr.write(
        """
==========================
Unsupported Python version
==========================
This version of idtrackerai requires Python {}.{}, but you're trying to
install it on Python {}.{}.
""".format(
            *(REQUIRED_PYTHON + CURRENT_PYTHON)
        )
    )
    sys.exit(1)

requirements = [
]


EXCLUDE_FROM_PACKAGES = []
PKG_NAME = "zeitgeber"

version = ""
with open(f"{PKG_NAME}/__init__.py", "r") as fd:
    try:
        version = re.search(
            r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', fd.read(), re.MULTILINE
        ).group(1)
    except AttributeError as error:
        print("Initializing version")
        version = "0.0.0"

with open("README.md", "r") as fd:
    long_description = fd.read()

setup(
    name=PKG_NAME,
    version=version,
    python_requires=">={}.{}".format(*REQUIRED_PYTHON),
    # url="https://idtrackerai.readthedocs.io/en/latest/",
    # author="Francisco Romero Ferrero, Mattia G. Bergomi, Francisco J.H. Heras, Ricardo Ribeiro",
    # author_email="idtracker@gmail.com",
    description=(
        "A multi-animal tracking algorithm based on convolutional neural networks"
    ),
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="GPLv3+",
    packages=find_packages(exclude=EXCLUDE_FROM_PACKAGES),
    include_package_data=True,
    package_data={
    #     "idtrackerai": [
    #         "data/example_video_compressed/*.avi",
    #         "utils/test.json",
    #     ]
    },
    install_requires=requirements,
    extras_require={
        # "cli": ["idtrackerai-app == 1.0.0a0"],
        # "gui": [
        #     "idtrackerai-app == 1.0.0a0",
        #     "pyforms-gui==4.904.152",
        #     "python-video-annotator==3.306",
        #     "python-video-annotator-module-idtrackerai == 1.0.1a0",
        # ],
        # "gpu": ["pytorch", "torchvision"],
        # "dev": ["pytest", "black", "sphinx", "numpydoc"],
    },
    zip_safe=False,
    classifiers=[
        # "Development Status :: 3 - Alpha",
        # "Environment :: Console",
        # "Intended Audience :: Science/Research",
        # "Intended Audience :: Developers",
        # "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        # "Operating System :: OS Independent",
        # "Programming Language :: Python",
        # "Programming Language :: Python :: 3",
        # "Programming Language :: Python :: 3.7",
        # "Topic :: Scientific/Engineering",
        # "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    entry_points={
        "console_scripts": [
        ],
    },
)
