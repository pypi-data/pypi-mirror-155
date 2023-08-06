# Author: luckgakidz <luckgakidz@luckgakidz.com>
# Copyright (c) 2022- luckgakidz
# Licence: MIT

from setuptools import setup

DESCRIPTION = 'Assorted tools of S parameter.'
NAME = 'as2s-sparameter'
AUTHOR = 'luckgakidz'
AUTHOR_EMAIL = 'luckgakidz@luckgakidz.com'
URL = 'https://github.com/luckgakidz/as2s_sparameter'
LICENSE = 'MIT'
DOWNLOAD_URL = URL
VERSION = '0.0.5'
PYTHON_REQUIRES = '>=3.10'
INSTALL_REQUIRES = ['scikit-rf>=0.22.1']
PACKAGES = ['as2s_sparameter']
KEYWORDS = 'sparameter touchstone'
CLASSIFIERS = [
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.10',
]
with open('README.md', 'r', encoding='utf-8') as fp:
    readme = fp.read()
LONG_DESCRIPTION = readme
LONG_DESCRIPTION_CONTENT_TYPE = 'text/markdown'

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type=LONG_DESCRIPTION_CONTENT_TYPE,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    maintainer=AUTHOR,
    maintainer_email=AUTHOR_EMAIL,
    url=URL,
    download_url=URL,
    packages=PACKAGES,
    classifiers=CLASSIFIERS,
    license=LICENSE,
    keywords=KEYWORDS,
    install_requires=INSTALL_REQUIRES,
)
