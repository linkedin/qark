from setuptools import setup, find_packages
import os

# Get relative path to template files so they can be included as a `data_file`
TEMPLATE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "qark", "templates")
template_files = [os.path.join("qark", "templates", template)
                  for template in os.listdir(TEMPLATE_DIR) if os.path.splitext(template)[1] == ".jinja"]


QARK_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "qark")
LIB_DIR = os.path.join(QARK_DIR, "lib")
DECOMPILERS_DIR = os.path.join(LIB_DIR, "decompilers")
jar_files = [os.path.join(DECOMPILERS_DIR, jar_file)
             for jar_file in os.listdir(DECOMPILERS_DIR) if os.path.splitext(jar_file)[1] == ".jar"]


exploit_apk_files = [os.path.join(dir_path, filename)
                     for dir_path, _, files in os.walk(os.path.join(QARK_DIR, "exploit_apk"))
                     for filename in files]

with open('requirements.txt') as f:
    all_lines = f.read().splitlines()
    required = [requirement.split(' ')[0] for requirement in all_lines if not requirement.startswith(' ')]

setup(
    name="qark",
    version="2.0",
    packages=find_packages(),
    package_data={"qark": jar_files + exploit_apk_files},  # include the jd_core.jar file
    include_package_data=True,  # includes template files in qark/templates
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
