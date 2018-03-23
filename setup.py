from setuptools import setup, find_packages
import os

# Get relative path to template files so they can be included as a `data_file`
TEMPLATE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "qark", "templates")
template_files = [os.path.join("qark", "templates", template)
                  for template in os.listdir(TEMPLATE_DIR) if os.path.splitext(template)[1] == ".jinja"]

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name="qark",
    version="2.0",
    packages=find_packages(),
    data_files=[("templates", template_files)],
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
