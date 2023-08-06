from setuptools import find_packages, setup
import os

def read(fname):
    """
    Utility function to read the README file. Used for the long_description.
    :param fname:
    :return:
    """
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

_REQUIRED = ['datasets']
_EXTRAS = []

setup(
    name='petdatasetreader',
    version='0.0.1a1',
    packages=find_packages(), #exclude=("tests", "results_frameworks")),
    install_requires=_REQUIRED,
    # extras_require=_EXTRAS,
    include_package_data=False,
    platforms="Any",

    python_requires='!=2.7, >=3.5.*',
    classifiers=[
            "Development Status :: 3 - Alpha",
            "License :: OSI Approved :: MIT License",
            "Natural Language :: English",

            "Intended Audience :: Science/Research",
            "Intended Audience :: Developers",
            "Intended Audience :: Education",
            "Intended Audience :: End Users/Desktop",
            "Intended Audience :: Information Technology",

            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3.5",
            "Programming Language :: Python :: 3.6",
            "Programming Language :: Python :: 3.7",
            "Programming Language :: Python :: 3.8",
            "Programming Language :: Python :: 3.9",
            "Programming Language :: Python :: 3.10",
            "Programming Language :: Python :: 3.11",
            "Programming Language :: Python :: 3.12",

            "Topic :: Scientific/Engineering",
            "Topic :: Utilities",
        ],

    author='Patrizio Bellan',
    author_email='patrizio.bellan@gmail.com',
    maintainer="Patrizio Bellan",
    maintainer_email="patrizio.bellan@gmail.com",

    url='https://pdi.fbk.eu/pet-dataset',

    license='MIT',
    keywords=["huggingface", "PET", "dataset", "benchmark", "process extraction from text",
              "natural language processing", "nlp", "business process management", "bpm"],
    description='Convenient interface that provides structured representations of the PET dataset hosted on Huggingface',
    long_description=read("README.rst"),
    long_description_content_type='text/x-rst',
)
