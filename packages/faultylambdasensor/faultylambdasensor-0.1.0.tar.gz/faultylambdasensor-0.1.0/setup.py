from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.1.0'
DESCRIPTION = 'Get Air:Fuel Ratio, Lambda Value and Spark Angle for Any Engine'
LONG_DESCRIPTION = 'Python Package for determining the Air: Fuel Ratio from the Fuel Maps and Spark Angle from the Ignition Map'
PROJECT_URLS = {
    'Source Code': 'https://github.com/SHESHANKSK/faultylambdasensor',
    'BUG Tracker': 'https://github.com/SHESHANKSK/faultylambdasensor/issues'
}

# Setting up
setup(
    version=VERSION,
    author="Sheshank Kindalkar",
    author_email="sheshankkindalkar@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    project_urls=PROJECT_URLS,
    packages=find_packages(),
    install_requires=['numpy', 'scipy'],
    keywords=['python', 'lambdasensor', 'air:fule',
              'sparkangle', 'automotive', 'fulemap', 'ignitionmap', 'faultysensor'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Education",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
