from setuptools import setup, find_packages
import os
import io

QARK_DIR = "qark"
LIB_DIR = os.path.join(QARK_DIR, "lib")


exploit_apk_files = [os.path.join(dir_path, filename).replace(os.path.join(QARK_DIR, ""), "")
                     for dir_path, _, files in os.walk(os.path.join(QARK_DIR, "exploit_apk"))
                     for filename in files]


with io.open('README.rst', 'rt', encoding='utf8') as f:
    long_description = f.read()

setup(
    name="qark",
    version="4.0.0",
    packages=find_packages(exclude=["tests*"]),
    package_dir={QARK_DIR: QARK_DIR},
    package_data={
        QARK_DIR: [
            os.path.join("lib", "decompilers", "*.jar"),  # include any decompiler jar files
            os.path.join("lib", "apktool", "*.jar"),  # include apktool
            os.path.join("lib", "dex2jar-2.0", "*"),  # include dex2jar
            os.path.join("lib", "dex2jar-2.0", "lib", "*"),  # include dex2jar
            os.path.join("templates", "*.jinja"),  # include the reporting template files
        ] + exploit_apk_files,  # include all the java files required for creating an exploit APK
    },
    install_requires=[
        "requests[security]",
        "pluginbase",
        "jinja2",
        "enum34; python_version < '3.4'",
        "javalang",
        "click",
        "six",
    ],
    # metadata for upload to PyPI
    author="Tushar Dalvi & Tony Trummer",
    author_email="tushardalvi@gmail.com, tonytrummer@hotmail.com",
    description="Android static code analyzer",
    long_description=long_description,
    license="Apache 2.0",
    keywords="android security qark exploit",
    url="https://www.github.com/linkedin/qark",
    entry_points="""
        [console_scripts]
        qark=qark.qark:cli""",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: MacOS",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: Unix",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.6",
    ]
)
