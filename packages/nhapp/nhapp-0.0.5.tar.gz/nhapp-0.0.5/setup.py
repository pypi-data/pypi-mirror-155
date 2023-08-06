import os
from setuptools import find_packages, setup
import setuptools
import numpy
with open(os.path.join(os.path.dirname(__file__), "README.md")) as readme:
    README = readme.read()
setuptools.setup(
    name="nhapp",
    version="0.0.5",
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
    python_requires='>=3.8',
    install_requires=['numpy','pandas']

    # install_requires=[
        # 'numpy>=1.18.5'; platform_machine!='aarch64' and platform_machine!='arm64' and python_version<'3.10',
	    # numpy>=1.19.2; platform_machine=='aarch64' and python_version<'3.10',
	    # numpy>=1.20.0; platform_machine=='arm64' and python_version<'3.10',
	    # numpy>=1.21.0; python_version>='3.10',
	    # python-dateutil>=2.8.1,

	    # numpy>=1.18.5; platform_machine!='aarch64' and platform_machine!='arm64' and python_version<'3.10',
	    # numpy>=1.19.2; platform_machine=='aarch64' and python_version<'3.10',
	    # numpy>=1.20.0; platform_machine=='arm64' and python_version<'3.10',
	    # numpy>=1.21.0; python_version>='3.10',
	    # python-dateutil>=2.8.1,
	    # pytz>=2020.1,
        
    

    # include_package_data = True
    # zip_safe = False

)