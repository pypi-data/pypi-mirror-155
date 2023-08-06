from setuptools import setup, find_packages

VERSION = '3.0.0' 
DESCRIPTION = 'Software to run the 3D-PAWS weather stations.'

with open(file="README.md", mode="r") as readme:
    LONG_DESCRIPTION = readme.read()

setup(
        name="3d-paws", 
        version=VERSION,
        author="Joey Rener",
        author_email="jrener@ucar.edu",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=[], 
        
        keywords=['python', '3d', 'paws'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)