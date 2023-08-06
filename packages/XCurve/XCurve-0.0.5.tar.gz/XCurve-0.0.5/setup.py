import setuptools
import os
if os.path.exists('README.md'):
    with open('README.md', encoding='utf-8') as fp:
        long_description = fp.read()
else:
    long_description = ' '
if os.path.exists('requirements.txt'):
    with open('requirements.txt', encoding='utf-8') as fp:
        install_requires = fp.read()
        install_requires = install_requires.split('\n')
else:
    install_requires = []

setuptools.setup(
    name="XCurve",                     # This is the name of the package
    version="0.0.5",                      # The initial release version
    author="qqgroup",                     # Full name of the author
    author_email='  ',
    description="machine learning package",
    url='https://gitee.com/Statusrank/xcurve-opt',
    long_description=long_description,      # Long description read from the the readme file
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),    # List of all python modules to be installed
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],                                      # Information to filter the project on PyPi website
    python_requires='>=3.8',                # Minimum version requirement of the package
    py_modules=["XCurve"],             # Name of the python package
    package_dir={'XCurve':'XCurve'},
    install_requires=install_requires       # Install other dependencies if any
)
