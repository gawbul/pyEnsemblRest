from setuptools import setup
from setuptools import find_packages

__author__ = 'Steve Moss'
__email__ = 'gawbul@gmail.com'
__version__ = '0.2.0b'

setup(
    # Basic package information.
    name='pyensemblrest',
    version=__version__,
    packages=find_packages(),

    # Packaging options.
    include_package_data=True,

    # Package dependencies.
    install_requires=['requests>=1.0.0, <2.0.0'],

    # Metadata for PyPI.
    author='Steve Moss',
    author_email='gawbul@gmail.com',
    license='GPLv3',
    url='http://github.com/pyopensci/pyensemblrest/tree/master',
    keywords='ensembl python rest api',
    description='An easy way to access EnsEMBL data with Python.',
    long_description=open('README.rst').read(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
        'Topic :: Internet',
    ]
)
