import os
import re
import setuptools

scriptFolder = os.path.dirname(os.path.realpath(__file__))
os.chdir(scriptFolder)

# Find version info from module (without importing the module):
with open("src/tongyi/__init__.py", "r") as fileObj:
    version = re.search(
        r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', fileObj.read(), re.MULTILINE
    ).group(1)

setuptools.setup(
    name="tongyi",
    version=version,
    author="dicey",
    author_email="dicey.dai@clickcorp.com",
    description="test for mutiple platforms",
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(where='src'),
    package_dir={'': 'src'},
    test_suite='tests',
    include_package_data = True,
    classifiers=[
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