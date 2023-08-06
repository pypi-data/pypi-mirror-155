# Собираем модули

from setuptools import setup, Extension, find_packages
import pathlib
import os

module = [
    Extension('rsrfile', [f'src/{f}' for f in os.listdir('src') if f.endswith('.c')])]


here = pathlib.Path(__file__).parent.resolve()
long_description = (here / "README.md").read_text(encoding="utf-8")

setup(
    name='rsdb',
    description='Object–relational mapping for RiskSpectrum PSA model database',
    long_description=long_description,
    long_description_content_type='text/markdown',
    version='0.9.0',
    author='Kravchenko Vladimir S',
    author_email='kvover@gmail.com',
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "License :: OSI Approved :: GNU Lesser General Public License v2 or later (LGPLv2+)",
        "Natural Language :: English",
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.8, <4",
    url='https://github.com/HexQuant/rsdb',
    project_urls={
        "Bug Reports": "https://github.com/HexQuant/rsdb/issues",
        "Source": "https://github.com/HexQuant/rsdb",
    })