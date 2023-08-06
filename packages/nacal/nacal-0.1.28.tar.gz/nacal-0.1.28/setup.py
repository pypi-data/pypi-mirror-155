import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


import codecs
import os.path

def read(rel_path):
    here = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(here, rel_path), 'r') as fp:
        return fp.read()

def get_version(rel_path):
    for line in read(rel_path).splitlines():
        if line.startswith('__version__'):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    else:
        raise RuntimeError("Unable to find version string.")

nombre = "nacal"

setuptools.setup(
    name = nombre,
    version=get_version(nombre + "/__init__.py"),
    author="Marcos Bujosa",
    license="GPLv3",
    author_email="mbujosab@ucm.es",
    description="Notacion Asociativa para un curso de Algebra Lineal (NAcAL)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mbujosab/nacallib",
    packages=setuptools.find_packages(),
    #pakages=["nacal"],
    install_requires=["sympy>=1.1.0"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Intended Audience :: Education",
        "Framework :: Jupyter",
        "Environment :: Console",
        "Natural Language :: Spanish",
        "Topic :: Scientific/Engineering :: Mathematics",
        "Development Status :: 3 - Alpha",
    ],
    python_requires='>=3.6',
    keywords="nacal"
)
