import setuptools
import re
import os.path

longDescription = None
if os.path.isfile("readme.md") :
    with open("readme.md", "r") as fh:
        longDescription = fh.read()
        longDescription = re.sub(r'\]\(doc\/', '](https://github.com/wqking/obfupy/tree/master/doc/', longDescription)

description = "obfupy is a Python 3 library that can obfuscate whole Python 3 projects, transform the source code to obfuscated and hard to understand code. obfupy aims to produce correct and functional code."
if longDescription is None :
    longDescription = description

setuptools.setup(
    name = "obfupy",
    version = "0.1.1",
    author = "wqking",
    author_email = "wqking@NOSPAMoutlook.com",
    description = description,
    long_description = longDescription,
    long_description_content_type = "text/markdown",
    url = "https://github.com/wqking/obfupy",
    packages = setuptools.find_packages(),
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires = '>=3.9',
    platforms = ['any'],
)
