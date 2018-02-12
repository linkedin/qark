from setuptools import setup, find_packages

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name="qark",
    version="2.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=required,
    # metadata for upload to PyPI
    # author="Tushar Dalvi & Tony Trummer",
    # author_email="tushardalvi@gmail.com, tonytrummer@hotmail.com",
    description="Android static code analyzer",
    license="Apache 2.0",
    keywords="android security qark exploit",
    url="https://www.github.com/linkedin/qark",
    entry_points="""
        [console_scripts]
        qark=qark.qark:cli""",
)
