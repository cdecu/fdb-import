import os

from fdbimport import __version__, __author__, __email__
from setuptools import setup, find_packages

base = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(base, 'README.md'), encoding='utf-8') as file:
    long_description = file.read()

setup(
    name='fdb-import',
    version=__version__,
    description='test fdb import',
    long_description=long_description,
    url='https://github.com/cdecu/fdbimport.git',
    download_url='',
    author=__author__,
    author_email=__email__,
    maintainer='carlos',
    maintainer_email='carlos@xpertbilling.com',
    license='Freeware',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'License :: Freeware',
        'Natural Language :: English',
        'Natural Language :: French',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Multimedia :: Graphics',
        'Topic :: Utilities'
    ],
    keywords='test fdb import',
    platforms=['Any'],
    packages=find_packages(),
    install_requires=['fdb', 'openpyxl', 'humanize'],
    entry_points={
        'console_scripts': ['fdbimport=fdbimport.fdbimport:main']
    }
)
