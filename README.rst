=============
pyEnsemblRest
=============

``pyEnsemblRest`` is a simple Python wrapper around the EnsEMBL REST API

.. image:: https://travis-ci.org/pyOpenSci/pyEnsemblRest.svg?branch=master :target: https://travis-ci.org/pyOpenSci/pyEnsemblRest :alt: Build Status

.. image:: https://img.shields.io/coveralls/pyOpenSci/pyEnsemblRest.svg?maxAge=2592000   :target: https://img.shields.io/pypi/v/pyensemblrest.svg :alt: Code Coverage

.. image:: https://img.shields.io/gitter/room/pyOpenSci/pyEnsemblRest.js.svg?maxAge=2592000   :target: https://gitter.im/pyOpenSci/pyEnsemblRest :alt: Gitter Chat

.. image:: https://img.shields.io/pypi/v/pyensemblrest.svg?maxAge=2592000   :target: https://pypi.python.org/pypi/pyensemblrest

.. image:: https://img.shields.io/github/downloads/pyOpenSci/pyEnsemblRest/total.svg?maxAge=2592000   :target: https://github.com/pyOpenSci/pyEnsemblRest

Installation
============
::

    git clone https://github.com/pyOpenSci/pyEnsemblRest.git
    cd pyEnsemblRest
    sudo python setup.py install

Usage
=====

To import an setup a new EnsemblRest object you should do the following:
::

	from ensemblrest import EnsemblRest
	ensRest = EnsemblRest()

EnsemblRest() istance points to http://rest.ensembl.org/ . In order to use EnsemblGenome, you can import a different object:
::

	from ensemblrest import EnsemblGenomeRest
	ensGenomeRest = EnsemblGenomeRest()

Or, as an alternative, you can give a different base url during EnsemblRest class instantiation:
::

	from ensemblrest import EnsemblRest
	ensGenomeRest = EnsemblRest(base_url='http://rest.ensemblgenomes.org')

To use a custom EnsEMBL REST server you should setup the EnsemblRest as the precedent way:
::

	from ensemblrest import EnsemblRest
	ensRest = EnsemblRest(base_url='http://localhost:3000') # setup rest object to point to localhost server. The 3000 stands for REST default port

You may also provide proxy server settings in the form of a dict, as follows:
::

	from ensemblrest import EnsemblRest
	ensRest = EnsemblRest(proxies={'http':'proxy.addres.com:3128', 'https':'proxy.address.com:3128'}) # setup rest object to point to localhost server

EnsEMBL has a rate-limit policy to deal with requests. You can do up to 15 requests per second. You could wait a little during your requests:
::

	from time import sleep
	sleep(1) # sleep for a second so we don't get rate-limited

Alternatively this library verifies and limits your requests to 15 requests per second. Avoid to run different python processes to get your data, otherwise you will be blacklisted by ensembl team. If you have to do a lot or requests, consider to use POST supported endpoints, or contact ensembl team to add POST support to endpoints of your interest.

GET endpoints
-------------

EnsemblRest and EnsemblGenomeRest class methods are not defined in libraries, so you cannot see docstring using help() method on python or ipython terminal. However you can see all methods available for ensembl_ and ensemblgenomes_ rest server once class is instantiate. To get help on a particoular method, please refer to ensembl help documentation on different endpoints in the ensembl_ and ensemblgenomes_ rest service. Please note that endpoints on ensembl_ may be different from ensemblgenomes_ endpoints.
If you look, for example, at sequence_ endpoint documentation, you will find optional and required parameters. Required parameters must be specified in order to work properly, otherwise you will get an exception. Optional parameters may be specified or not, depending on your request. In all cases parameter name are the same used in documentation. For example to get data using sequence_ endpoint, you must specify at least required parameters:
::

	seq = ensRest.getSequenceById(id='ENSG00000157764')

In order to mask sequence and to expand the 5' UTR you may set optional parameters using the same name described in documentation:
::

	seq = ensRest.getSequenceById(id='ENSG00000157764', mask="soft", expand_5prime=1000)

POST endpoints
--------------

POST endpoints can be used as the GET endpoints, the only difference is that they support parameters in python list in order to perform multiple queries on the same ensembl endpoint. The parameters name are the same used in documentation, for example we can use the `POST sequence`_ endpoint in such way:
::

	seqs = ensRest.getSequenceByMultipleIds(ids=["ENSG00000157764", "ENSG00000248378" ])

where the example value { "ids" : ["ENSG00000157764", "ENSG00000248378" ] } is converted in the non-positional argument ids=["ENSG00000157764", "ENSG00000248378" ]. As the previous example, we can add optional parameters:
::

	seqs = ensRest.getSequenceByMultipleIds(ids=["ENSG00000157764", "ENSG00000248378"], mask="soft")

Change the default Output format
--------------------------------

You can change the default output format by passing a supported ``Content-type`` using
the ``content_type`` parameter, for example:
::

  plain_xml = ensRest.getArchiveById(id='ENSG00000157764', content_type="text/xml")

For a complete list of supported ``Content-type`` see `Supported MIME Types`_ from
ensembl REST documentation. You need also to check if the same ``Content-type`` is
supported in EnsEMBL endpoint description.

.. _Supported MIME Types: https://github.com/Ensembl/ensembl-rest/wiki/Output-formats#supported-mime-types

Methods list
------------

Here is a list of all methods defined. Methods called by ensRest object are specific to ensembl_ rest server, while methods called via ensGenomeRest are specific of ensemblgenomes_ rest server.

To access the *Archive* endpoints you can use the following methods:
::

	print ensRest.getArchiveById(id="ENSG00000157764")
	print ensRest.getArchiveByMultipleIds(id=["ENSG00000157764", "ENSG00000248378"])


To access the *Comparative Genomics* endpoints you can use the following methods:
::

	print ensGenomeRest.getGeneFamilyById(id="MF_01687", compara="bacteria")
	print ensGenomeRest.getGeneFamilyMemberById(id="b0344", compara="bacteria")
	print ensGenomeRest.getGeneFamilyMemberBySymbol(symbol="lacZ", species="escherichia_coli_str_k_12_substr_mg1655", compara="bacteria")
	print ensRest.getGeneTreeById(id='ENSGT00390000003602')
	print ensRest.getGeneTreeMemberById(id='ENSG00000157764')
	print ensRest.getGeneTreeMemberBySymbol(species='human', symbol='BRCA2')
	print ensRest.getAlignmentByRegion(species="taeniopygia_guttata", region="2:106040000-106040050:1", species_set_group="sauropsids")
	print ensRest.getHomologyById(id='ENSG00000157764')
	print ensRest.getHomologyBySymbol(species='human', symbol='BRCA2')

To access the *Cross References* endpoints you can use the following methods:
::

	print ensRest.getXrefsById(id='ENSG00000157764')
	print ensRest.getXrefsByName(species='human', name='BRCA2')
	print ensRest.getXrefsBySymbol(species='human', symbol='BRCA2')


To access the *Information* endpoints you can use the following methods:
::

	print ensRest.getInfoAnalysis(species="homo_sapiens")
	print ensRest.getInfoAssembly(species="homo_sapiens", bands=1) #bands is an optional parameter
	print ensRest.getInfoAssemblyRegion(species="homo_sapiens", region_name="X")
	print ensRest.getInfoBiotypes(species="homo_sapiens")
	print ensRest.getInfoComparaMethods()
	print ensRest.getInfoComparaSpeciesSets(methods="EPO")
	print ensRest.getInfoComparas()
	print ensRest.getInfoData()
	print ensGenomeRest.getInfoEgVersion()
	print ensRest.getInfoExternalDbs(species="homo_sapiens")
	print ensGenomeRest.getInfoDivisions()
	print ensGenomeRest.getInfoGenomesByName(name="campylobacter_jejuni_subsp_jejuni_bh_01_0142")

	#This response is very heavy
	#print ensGenomeRest.getInfoGenomes()

	print ensGenomeRest.getInfoGenomesByAccession(division="U00096")
	print ensGenomeRest.getInfoGenomesByAssembly(division="GCA_000005845")
	print ensGenomeRest.getInfoGenomesByDivision(division="EnsemblPlants")
	print ensGenomeRest.getInfoGenomesByTaxonomy(division="Arabidopsis")
	print ensRest.getInfoPing()
	print ensRest.getInfoRest()
	print ensRest.getInfoSoftware()
	print ensRest.getInfoSpecies()

To access the *Lookup* endpoints you can use the following methods:
::

	print ensRest.getLookupById(id='ENSG00000157764')
	print ensRest.getLookupByMultipleIds(ids=["ENSG00000157764", "ENSG00000248378" ])
	print ensRest.getLookupBySpeciesSymbol(species="homo_sapiens", symbol="BRCA2", expand=1)
	print ensRest.getLookupByMultipleSpeciesSymbols(species="homo_sapiens", symbols=["BRCA2", "BRAF"])

To access the *Mapping* endpoints you can use the following methods:
::

	print ensRest.getMapCdnaToRegion(id='ENST00000288602', region='100..300')
	print ensRest.getMapCdsToRegion(id='ENST00000288602', region='1..1000')
	print ensRest.getMapAssemblyOneToTwo(species='human', asm_one='NCBI36', region='X:1000000..1000100:1', asm_two='GRCh37')
	print ensRest.getMapTranslationToRegion(id='ENSP00000288602', region='100..300')

To access the *Ontologies and Taxonomy* endpoints you can use the following methods:
::

	print ensRest.getAncestorsById(id='GO:0005667')
	print ensRest.getAncestorsChartById(id='GO:0005667')
	print ensRest.getDescendantsById(id='GO:0005667')
	print ensRest.getOntologyById(id='GO:0005667')
	print ensRest.getOntologyByName(name='transcription factor complex')
	print ensRest.getTaxonomyClassificationById(id='9606')
	print ensRest.getTaxonomyById(id='9606')
	print ensRest.getTaxonomyByName(name="Homo%25")

To access the *Overlap* endpoints you can use the following methods:
::

	print ensRest.getOverlapById(id="ENSG00000157764", feature="gene")
	print ensRest.getOverlapByRegion(species="human", region="7:140424943-140624564", feature="gene")
	print ensRest.getOverlapByTranslation(id="ENSP00000288602")

To access the *Regulation* endpoints you can use the following method:
::

	print ensRest.getRegulatoryFeatureById(species="homo_sapiens", id="ENSR00001348195")

To access the *Sequences* endpoints you can use the following methods:
::

	print ensRest.getSequenceById(id='ENSG00000157764')
	print ensRest.getSequenceByMultipleIds(ids=["ENSG00000157764", "ENSG00000248378" ])
	print ensRest.getSequenceByRegion(species='human', region='X:1000000..1000100')
	print ensRest.getSequenceByMultipleRegions(species="homo_sapiens", regions=["X:1000000..1000100:1", "ABBA01004489.1:1..100"])

To access the *VEP* endpoints you can use the following methods:
::

	print ensRest.getVariantConsequencesByHGVSnotation(species="human", hgvs_notation="AGT:c.803T>C")
	print ensRest.getVariantConsequencesById(species='human', id='COSM476')
	print ensRest.getVariantConsequencesByMultipleIds(species="human", ids=[ "rs116035550", "COSM476" ])
	print ensRest.getVariantConsequencesByRegion(species='human', region='9:22125503-22125502:1', allele='C')
	print ensRest.getVariantConsequencesByMultipleRegions(species="human", variants=["21 26960070 rs116645811 G A . . .", "21 26965148 rs1135638 G A . . ." ] )

To access the *Variation* endpoints you can use the following method:
::

	print ensRest.getVariationBySpeciesId(id="rs56116432", species="homo_sapiens")


.. _ensembl: http://rest.ensembl.org/
.. _ensemblgenomes: http://rest.ensemblgenomes.org/
.. _sequence: http://rest.ensembl.org/documentation/info/sequence_id
.. _POST sequence: http://rest.ensembl.org/documentation/info/sequence_id_post
