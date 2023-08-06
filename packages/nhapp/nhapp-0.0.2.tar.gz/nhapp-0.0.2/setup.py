import os
import pandas
from setuptools import find_packages, setup
import setuptools
with open(os.path.join(os.path.dirname(__file__), "README.md")) as readme:
    README = readme.read()

setuptools.setup(
    name="nhapp",
    version="0.0.2",
    author="Nguyen Manh Dung ",
    author_email="123456zvn2@gmail.com",
    description="inspire your love ",
    long_description="Make you feel the strong of love",
    long_description_content_type="text/markdown",
    url="https://github.com/mwpnava/Python-Code/tree/master/My_own_Python_package",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    # requires=pandas
)