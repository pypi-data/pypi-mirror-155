from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.0.32'
DESCRIPTION = 'Get financial data synchronously. This package is a wrapper around the IB API.'
LONG_DESCRIPTION = 'A package that allows to get financial data from ib, in sync(event driven) and async way'

# Setting up
setup(
    name="ib_syncevent",
    version=VERSION,
    author="Zohar",
    author_email="<mail@test.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=['ibapi'],
    python_requires='>=3.8',
    keywords=['python', 'ib', 'financial', 'financial data', 'stcoks'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
