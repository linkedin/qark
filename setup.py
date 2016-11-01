from setuptools import setup, find_packages
from pip.req import parse_requirements

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name = "qark",
    version = "1.2.19",
    packages = ['qark/modules','qark/lib', 'qark'],
    include_package_data = True,
#     scripts = ['qark.py'],
    install_requires = required,
    package_data = {
        # If any package contains *.txt or *.rst files, include them:
        './': ['*.py'],
        # And include any *.msg files found in the 'hello' package, too:
        #'hello': ['*.msg'],
    },
    # metadata for upload to PyPI
    author = "Tushar Dalvi & Tony Trummer",
    author_email = "tushardalvi@gmail.com, tonytrummer@hotmail.com",
    description = "Android static code analyzer",
    license = "Apache 2.0",
    keywords = "android security qark exploit",
    url = "https://www.github.com/linkedin/qark",

)
