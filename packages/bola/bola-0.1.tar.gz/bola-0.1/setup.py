import setuptools
from glob import glob
import site
from setuptools import Extension
import os
import sys
from pathlib import Path
from pybind11.setup_helpers import Pybind11Extension, build_ext

# https://github.com/googlefonts/fontmake/commit/164b24fd57c062297bf68b21c8ae88bc676f090b
site.ENABLE_USER_SITE = "--user" in sys.argv[1:]

__version__ = "0.1"


EIGEN_INCLUDE_DIR = os.environ.get("BOLA_EIGEN_DIR", "/usr/include/eigen3")

source_dir = Path(__file__).parent / "bola" / "src"

ext_modules = [
    Pybind11Extension(
        "bola._cpp",
        sources=sorted(glob("bola/src/*.cpp")),
        # Example: passing in the version to the compiled code
        # define_macros=[("VERSION_INFO", __version__)],
        extra_compile_args=["-O3"],
        language="c++",
        # extra_link_args=["-lgomp"],
        include_dirs=[EIGEN_INCLUDE_DIR],
    ),
]


with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="bola",
    version=__version__,
    author="Thomas Titscher",
    author_email="thomas.titscher@gmail.com",
    description="Sphere stuff",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    ext_modules=ext_modules,
    cmdclass={"build_ext": build_ext},
    zip_safe=False,
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=["tabulate", "numpy", "loguru", "vtk", "tqdm", "gmsh"],
    extras_require={  # Optional
        "dev": ["black"],
        "test": ["pytest", "pytest-cov", "flake8", "h5py", "meshio"],
    },
)
