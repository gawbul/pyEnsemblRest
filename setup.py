
"""

    This file is part of pyEnsemblRest.
    Copyright (C) 2013-2016, Steve Moss

    pyEnsemblRest is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    pyEnsemblRest is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with pyEnsemblRest.  If not, see <http://www.gnu.org/licenses/>.

"""



from setuptools import setup
from setuptools import find_packages

__author__ = 'Steve Moss'
__email__ = 'gawbul@gmail.com'
__version__ = '0.2.3'

setup(
    # Basic package information.
    name='pyensemblrest',
    version=__version__,
    packages=find_packages(exclude=['test']),

    # Packaging options.
    include_package_data=True,

    # Package dependencies.
    install_requires=['requests>=1.0.0'],

    # testing modules
    test_suite = "test",

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
