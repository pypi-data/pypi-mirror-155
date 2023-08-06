from setuptools import setup, find_packages

VERSION = '1.1.0' 
DESCRIPTION = 'TriCCo'
LONG_DESCRIPTION = 'TriCCo: a python package for connected component labeling on triangular grids'

setup(
        name="tricco", 
        version=VERSION,
        author="Aiko Voigt",
        author_email="<aiko.voigt@univie.ac.at>",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        url = "https://gitlab.phaidra.org/climate/tricco",
        install_requires=['numpy', 'xarray', 'connected-components-3d', 'networkx'],
        keywords=['python', 'connected components', 'triangular grids'],
        classifiers= [
            "Intended Audience :: Science/Research",
            "Programming Language :: Python :: 3",
            "Operating System :: OS Independent",
        ],
        packages=find_packages(exclude=["benchmarks","examples"]),
        python_requires=">=3.8",
)
