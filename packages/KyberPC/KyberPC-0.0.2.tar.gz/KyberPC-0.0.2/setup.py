from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.0.2'
DESCRIPTION = 'Kyber with Polar Codes'
LONG_DESCRIPTION = 'A library of a Secure Post Quantum Scheme with Polar Codes for Error Correction.'

# Setting up
setup(
    name="KyberPC",
    version=VERSION,
    author="Jason-Papa",
    author_email="iasonvas@gmail.com",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=['numpy', 'matplotlib'],
    keywords=['python', 'Kyber', 'Error Correction', 'Polar Codes', 'Kyber with Polar Codes'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Microsoft :: Windows",
    ]
)