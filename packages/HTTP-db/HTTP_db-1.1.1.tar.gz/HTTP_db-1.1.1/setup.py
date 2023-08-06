from setuptools import setup
import HTTP_db

DESCRIPTION = "Simple and easy database system using HTTP"
NAME = 'HTTP_db'
AUTHOR = 'nattyan-tv'
AUTHOR_EMAIL = 'nananatsu2020@outlook.com'
URL = 'https://github.com/nattyan-tv/HTTP_db'
LICENSE = 'MIT License'
DOWNLOAD_URL = 'https://github.com/nattyan-tv/HTTP_db'
VERSION = HTTP_db.__version__
PYTHON_REQUIRES = ">=3.7"

INSTALL_REQUIRES = [
    'aiohttp>=3.8.1'
]

PACKAGES = [
    'HTTP_db'
]

CLASSIFIERS = [
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3 :: Only',
]
with open('README.md', encoding='utf-8') as f:
    long_description = f.read()


setup(name=NAME,
      author=AUTHOR,
      author_email=AUTHOR_EMAIL,
      maintainer=AUTHOR,
      maintainer_email=AUTHOR_EMAIL,
      description=DESCRIPTION,
      long_description=long_description,
      long_description_content_type='text/markdown',
      license=LICENSE,
      url=URL,
      version=VERSION,
      download_url=DOWNLOAD_URL,
      python_requires=PYTHON_REQUIRES,
      install_requires=INSTALL_REQUIRES,
      packages=PACKAGES,
      classifiers=CLASSIFIERS,
      keywords=['HTTP', 'database', 'simple', 'easy', 'nirabot'],
      )
