from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.0.1'
DESCRIPTION = 'init version of python client'
LONG_DESCRIPTION = 'description of python client usage.'

# Setting up
setup(
    name="nikki.python",
    version=VERSION,
    author="dev nikki",
    url ="https://github.com/nikki-build/nikki.python",
    author_email="dev.nikki.build@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=[ 'websocket', 'websocket-client'],
    keywords=['python', 'nikki'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
       
    ]
)