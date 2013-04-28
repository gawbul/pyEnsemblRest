pyEnsemblRest
=============
``pyEnsemblRest`` is a simple Python wrapper around the EnsEMBL REST API

Installation
------------
::

    git clone git://github.com/gawbul/pyensemblrest.git
    cd pyensemblrest
    sudo python setup.py install

Usage
-----
::

	from ensemblrest import EnsemblRest
	erest = EnsemblRest()
	print erest.getRestVersion()
	print erest.getSpeciesInfo()