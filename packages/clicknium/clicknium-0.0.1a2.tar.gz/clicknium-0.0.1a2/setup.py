import os
import re
import setuptools

scriptFolder = os.path.dirname(os.path.realpath(__file__))
os.chdir(scriptFolder)

# Find version info from module (without importing the module):
with open("src/clicknium/__init__.py", "r") as fileObj:
    version = re.search(
        r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', fileObj.read(), re.MULTILINE
    ).group(1)

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="clicknium",
    version=version,
    author="ClickCorp",
    author_email="clicknium@clickcorp.com",
    description="Python sdk which enables GUI automation for all type of applications.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(where='src'),
    package_dir={'': 'src'},
    test_suite='tests',
    install_requires=['pythonnet','typing_extensions'],
    include_package_data = True,
    classifiers=[
        'Environment :: Win32 (MS Windows)',
        'Environment :: X11 Applications',
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    package_data={
        '':['*.dll','*.config','*.xml']
    }
)