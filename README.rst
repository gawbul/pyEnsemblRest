=============
pyEnsemblRest
=============

``pyEnsemblRest`` is a simple Python wrapper around the EnsEMBL REST API

.. image:: https://travis-ci.org/gawbul/pyEnsemblRest.svg?branch=master :target: https://travis-ci.org/gawbul/pyEnsemblRest
.. image:: https://coveralls.io/repos/gawbul/pyEnsemblRest/badge.png :target: https://coveralls.io/r/gawbul/pyEnsemblRest
.. image:: https://badges.gitter.im/Join%20Chat.svg :target: https://gitter.im/gawbul/pyEnsemblRest?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge

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

To use a custom EnsEMBL REST server you should setup the EnsemblRest object as follows:
::

	from ensemblrest import EnsemblRest
	ensemblrest = EnsemblRest(server='localhost') # setup rest object to point to localhost server

You may also provide proxy server settings in the form of a dict, as follows:
::

	from ensemblrest import EnsemblRest
	ensemblrest = EnsemblRest(proxies={'http':'proxy.addres.com:3128', 'https':'proxy.address.com:3128'}) # setup rest object to point to localhost server

You should also sleep for a second between every 3 requests (with bursts of 6 requests allowed periodically) using the following syntax:
::

	from time import sleep
	sleep(1) # sleep for a second so we don't get rate-limited

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

	print ensemblrest.getFeatureById(id='ENSG00000157764', feature='gene')
	print ensemblrest.getFeatureByRegion(species='human', region='7:140424943..140624564', feature='gene')

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

	print ensemblrest.getLookupById(id='ENSG00000157764')

To access the *Mapping* endpoints you can use the following methods:
::

	print ensemblrest.getMapAssemblyOneToTwo(species='human', asm_one='NCBI36', region='X:1000000..1000100:1', asm_two='GRCh37')
	print ensemblrest.getMapCdnaToRegion(id='ENST00000288602', region='100..300')
	print ensemblrest.getMapCdsToRegion(id='ENST00000288602', region='1..1000')
	print ensemblrest.getMapTranslationToRegion(id='ENSP00000288602', region='100..300')

To access the *Ontologies and Taxonomy* endpoints you can use the following methods:
::

	print ensemblrest.getAncestorsById(id='GO:0005667')
	print ensemblrest.getAncestorsChartById(id='GO:0005667')
	print ensemblrest.getDescendentsById(id='GO:0005667')
	print ensemblrest.getOntologyById(id='GO:0005667')
	print ensemblrest.getOntologyByName(name='transcription factor complex')
	print ensemblrest.getTaxonomyClassificationById(id='9606')
	print ensemblrest.getTaxonomyById(id='9606')

To access the *Sequences* endpoints you can use the following methods:
::

	print ensemblrest.getSequenceById(id='ENSG00000157764')
	print ensemblrest.getSequenceByRegion(species='human', region='X:1000000..1000100')

To access the *Variation* endpoints you can use the following methods:
::

	print ensemblrest.getVariantConsequencesByRegion(species='human', region='9:22125503-22125502:1', allele='C')
	print ensemblrest.getVariantConsequencesById(species='human', id='COSM476')
