from setuptools import setup, find_packages
setup(
    name = "qark",
    version = "1.2.19",
    packages = ['qark/modules','qark/lib', 'qark'],
    include_package_data = True,
#     scripts = ['qark.py'],
    install_requires = ['AxmlParserPY>=0.01',
                        'blessed>=1.9.5',
                        'blessings>=1.6',
                        'beautifulsoup4>=4.4.0',
                        'colorama>=0.3.3',
                        'html5lib>=0.999999',
                        'progressbar>=2.3',
                        'pyfiglet>=0.7.4',
                        'argparse>=1.3.0',
                        'coloredlogs>=1.0.1'],
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
