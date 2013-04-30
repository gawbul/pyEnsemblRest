=============
pyEnsemblRest
=============

``pyEnsemblRest`` is a simple Python wrapper around the EnsEMBL REST API

Installation
============
::

    git clone git://github.com/gawbul/pyensemblrest.git
    cd pyensemblrest
    sudo python setup.py install

Usage
=====

To import an setup a new EnsemblRest object you should do the following:
::

	from ensemblrest import EnsemblRest
	ensemblrest = EnsemblRest()

To access the *Comparative Genomics* endpoints you can use the following methods:
::

	print ensemblrest.getGeneTreeById(id='ENSGT00390000003602')
	print ensemblrest.getGeneTreeByMemberId(id='ENSG00000157764')
	print ensemblrest.getGeneTreeByMemberSymbol(species='human', symbol='BRCA2')
	
	print ensemblrest.getHomologyById(id='ENSG00000157764')
	print ensemblrest.getHomologyBySymbol(species='human', symbol='BRCA2')

To access the *Cross References* endpoints you can use the following methods:
::

	print ensemblrest.getXrefsById(id='ENSG00000157764')
	print ensemblrest.getXrefsByName(species='human', name='BRCA2')
	print ensemblrest.getXrefsBySymbol(species='human', symbol='BRCA2')

To access the *Features* endpoints you can use the following methods:
::

	print ensemblrest.getFeatureById(id='ENSG00000157764')
	print ensemblrest.getFeatureByRegion(species='human', region='7:140424943-140624564')

To access the *Information* endpoints you can use the following methods:
::

	print ensemblrest.getAssemblyInfo(species='human')
	print ensemblrest.getAssemblyInfoRegion(species='human', region_name='X')

	print ensemblrest.getInfoComparas()
	print ensemblrest.getInfoData()
	print ensemblrest.getInfoPing()
	print ensemblrest.getInfoRest()
	print ensemblrest.getInfoSoftware()
	print ensemblrest.getInfoSpecies()

To access the *Lookup* endpoints you can use the following methods:
::

	print ensemblrest.getLookupyId(id='ENSG00000157764')

To access the *Mapping* endpoints you can use the following methods:
::

To access the *Ontologies and Taxonomy* endpoints you can use the following methods:
::

To access the *Sequences* endpoints you can use the following methods:
::

	print ensemblrest.getSequenceById(id='ENSG00000157764')
	print ensemblrest.getSequenceByRegion(species='human', region='X:1000000..1000100')

To access the *Variation* endpoints you can use the following methods:
::
