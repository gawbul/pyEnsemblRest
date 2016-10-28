=============
pyEnsemblRest
=============

``pyEnsemblRest`` is a simple Python wrapper around the EnsEMBL REST API

.. image:: https://travis-ci.org/pyOpenSci/pyEnsemblRest.svg?branch=master
    :target: https://travis-ci.org/pyOpenSci/pyEnsemblRest
    :alt: Build Status

.. image:: https://coveralls.io/repos/github/pyOpenSci/pyEnsemblRest/badge.svg?branch=master
    :target: https://coveralls.io/github/pyOpenSci/pyEnsemblRest?branch=master
    :alt: Code Coverage

.. image:: https://img.shields.io/scrutinizer/g/pyOpenSci/pyEnsemblRest.svg?maxAge=2592000
    :target: https://img.shields.io/scrutinizer/g/pyOpenSci/pyEnsemblRest.svg?maxAge=2592000
    :alt: Code Quality

.. image:: https://img.shields.io/gitter/room/pyOpenSci/pyEnsemblRest.js.svg?maxAge=2592000
    :target: https://gitter.im/pyOpenSci/pyEnsemblRest
    :alt: Gitter Chat

.. image:: https://img.shields.io/pypi/v/pyensemblrest.svg?maxAge=2592000
    :target: https://pypi.python.org/pypi/pyensemblrest
    :alt: PyPi Package

.. image:: https://img.shields.io/github/downloads/pyOpenSci/pyEnsemblRest/total.svg?maxAge=2592000
    :target: https://github.com/pyOpenSci/pyEnsemblRest
    :alt: GitHub Downloads

.. image:: https://img.shields.io/pypi/dd/pyensemblrest.svg?maxAge=2592000
    :target: https://img.shields.io/pypi/dd/pyensemblrest.svg?maxAge=2592000
    :alt: PyPi Downloads
    
License
=======

pyEnsemblRest - A wrapper for the EnsEMBL REST API

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


Installation
============

Using pip
---------

Simply type:

.. code:: bash

  pip install pyensemblrest


From source
-----------

Clone the pyEnsemblRest then install package from source:

.. code:: bash

  git clone https://github.com/pyOpenSci/pyEnsemblRest.git
  cd pyEnsemblRest
  sudo python setup.py install

Usage
=====

To import an setup a new EnsemblRest object you should do the following:

.. code:: python

  from ensemblrest import EnsemblRest
  ensRest = EnsemblRest()

EnsemblRest() istance points to http://rest.ensembl.org/ . In order to use EnsemblGenome, you can import a different object:

.. code:: python

  from ensemblrest import EnsemblGenomeRest
  ensGenomeRest = EnsemblGenomeRest()

Or, as an alternative, you can give a different base url during EnsemblRest class instantiation:

.. code:: python

  from ensemblrest import EnsemblRest
  ensGenomeRest = EnsemblRest(base_url='http://rest.ensemblgenomes.org')

To use a custom EnsEMBL REST server you should setup the EnsemblRest as the precedent way:

.. code:: python

  from ensemblrest import EnsemblRest
  # setup rest object to point to localhost server. The 3000 stands for REST default port
  ensRest = EnsemblRest(base_url='http://localhost:3000')

You may also provide proxy server settings in the form of a dict, as follows:

.. code:: python

  from ensemblrest import EnsemblRest
  # setup rest object to point to a proxy server
  ensRest = EnsemblRest(proxies={'http':'proxy.address.com:3128', 'https':'proxy.address.com:3128'})

EnsEMBL has a rate-limit policy to deal with requests. You can do up to 15 requests per second. You could wait a little during your requests:

.. code:: python

  from time import sleep
  # sleep for a second so we don't get rate-limited
  sleep(1)

Alternatively this library verifies and limits your requests to 15 requests per second. Avoid to run different python processes to get your data, otherwise you will be blacklisted by ensembl team. If you have to do a lot or requests, consider to use POST supported endpoints, or contact ensembl team to add POST support to endpoints of your interest.

GET endpoints
-------------

EnsemblRest and EnsemblGenomeRest class methods are not defined in libraries, so you cannot see docstring using help() method on python or ipython terminal. However you can see all methods available for ensembl_ and ensemblgenomes_ rest server once class is instantiate. To get help on a particular method, please refer to ensembl help documentation on different endpoints in the ensembl_ and ensemblgenomes_ rest service. Please note that endpoints on ensembl_ may be different from ensemblgenomes_ endpoints.
If you look, for example, at sequence_ endpoint documentation, you will find optional and required parameters. Required parameters must be specified in order to work properly, otherwise you will get an exception. Optional parameters may be specified or not, depending on your request. In all cases parameter name are the same used in documentation. For example to get data using sequence_ endpoint, you must specify at least required parameters:

.. code:: python

  seq = ensRest.getSequenceById(id='ENSG00000157764')

In order to mask sequence and to expand the 5' UTR you may set optional parameters using the same name described in documentation:

.. code:: python

  seq = ensRest.getSequenceById(id='ENSG00000157764', mask="soft", expand_5prime=1000)

Multiple values for a certain parameters (for GET methods) can be submitted in a list. For example, to get the same results of

.. code:: bash

  curl 'http://rest.ensembl.org/overlap/region/human/7:140424943-140624564?feature=gene;feature=transcript;feature=cds;feature=exon' -H 'Content-type:application/json'

as described in `overlap region`_ GET endpoint, you can use the following function:

.. code:: python

  data = ensRest.getOverlapByRegion(species="human", region="7:140424943-140624564", feature=["gene", "transcript", "cds", "exon"])

.. _overlap region: http://rest.ensembl.org/documentation/info/overlap_region

POST endpoints
--------------

POST endpoints can be used as the GET endpoints, the only difference is that they support parameters in python list in order to perform multiple queries on the same ensembl endpoint. The parameters name are the same used in documentation, for example we can use the `POST sequence`_ endpoint in such way:

.. code:: python

  seqs = ensRest.getSequenceByMultipleIds(ids=["ENSG00000157764", "ENSG00000248378" ])

where the example value ``{ "ids" : ["ENSG00000157764", "ENSG00000248378" ] }`` is converted in the non-positional argument ``ids=["ENSG00000157764", "ENSG00000248378" ]``. As the previous example, we can add optional parameters:

.. code:: python

  seqs = ensRest.getSequenceByMultipleIds(ids=["ENSG00000157764", "ENSG00000248378"], mask="soft")

Change the default Output format
--------------------------------

You can change the default output format by passing a supported ``Content-type`` using
the ``content_type`` parameter, for example:

.. code:: python

  plain_xml = ensRest.getArchiveById(id='ENSG00000157764', content_type="text/xml")

For a complete list of supported ``Content-type`` see `Supported MIME Types`_ from
ensembl REST documentation. You need also to check if the same ``Content-type``
is supported in the EnsEMBL endpoint description.

.. _Supported MIME Types: https://github.com/Ensembl/ensembl-rest/wiki/Output-formats#supported-mime-types

Rate limiting
-------------

Sometime you can be rate limited if you are querying EnsEMBL REST services with more than one concurrent processes, or by `sharing ip addresses`_. In such case, you can have a message like this:

.. _sharing ip addresses: https://github.com/Ensembl/ensembl-rest/wiki#example-clients

.. code:: bash

  ensemblrest.exceptions.EnsemblRestRateLimitError: EnsEMBL REST API returned a 429 (Too Many Requests): You have been rate-limited; wait and retry. The headers X-RateLimit-Reset, X-RateLimit-Limit and X-RateLimit-Remaining will inform you of how long you have until your limit is reset and what that limit was. If you get this response and have not exceeded your limit then check if you have made too many requests per second. (Rate limit hit:  Retry after 2 seconds)

Even if this library tries to do 15 request per seconds, you should avoid to run multiple
EnsEMBL REST clients. To deal which such problem without interrupting your code, try
to deal with the exception; For example:

.. code:: python

  # import required modules
  import os
  import sys
  import time
  import logging

  # get ensembl REST modules and exception
  from ensemblrest import EnsemblRest
  from ensemblrest import EnsemblRestRateLimitError

  # An useful way to defined a logger lever, handler, and formatter
  logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
  logger = logging.getLogger(os.path.basename(sys.argv[0]))

  # setup a new EnsemblRest object
  ensRest = EnsemblRest()

  # Get a request and deal with retry_after. Set a maximum number of retries (don't
  # try to do the same request forever or you will be banned from ensembl!)
  attempt = 0
  max_attempts = 3

  while attempt < max_attempts:
      # update attempt count
      attempt += 1

      try:
          result = ensRest.getLookupById(id='ENSG00000157764')
          # exit while on success
          break

      # log exception and sleep a certain amount of time (sleeping time increases at each step)
      except EnsemblRestRateLimitError, message:
          logger.warn(message)
          time.sleep(ensRest.retry_after*attempt)

      finally:
          if attempt >= max_attempts:
              raise Exception("max attempts exceeded (%s)" %(max_attempts))

  sys.stdout.write("%s\n" %(result))
  sys.stdout.flush()

Methods list
------------

Here is a list of all methods defined. Methods called by ``ensRest`` instance are specific to ensembl_ rest server, while methods called via ``ensGenomeRest`` instance are specific of ensemblgenomes_ rest server.

To access the *Archive* endpoints you can use the following methods:

.. code:: python

  print ensRest.getArchiveById(id="ENSG00000157764")
  print ensRest.getArchiveByMultipleIds(id=["ENSG00000157764", "ENSG00000248378"])

To access the *Comparative Genomics* endpoints you can use the following methods:

.. code:: python

  print ensGenomeRest.getGeneFamilyById(id="MF_01687", compara="bacteria")
  print ensGenomeRest.getGeneFamilyMemberById(id="b0344", compara="bacteria")
  print ensGenomeRest.getGeneFamilyMemberBySymbol(symbol="lacZ", species="escherichia_coli_str_k_12_substr_mg1655", compara="bacteria")
  # Change the returned content type to "Newick" format
  print ensRest.getGeneTreeById(id='ENSGT00390000003602', nh_format="simple", content_type="text/x-nh")
  print ensRest.getGeneTreeMemberById(id='ENSG00000157764')
  print ensRest.getGeneTreeMemberBySymbol(species='human', symbol='BRCA2')
  print ensRest.getAlignmentByRegion(species="taeniopygia_guttata", region="2:106040000-106040050:1", species_set_group="sauropsids")
  print ensRest.getHomologyById(id='ENSG00000157764')
  print ensRest.getHomologyBySymbol(species='human', symbol='BRCA2')

To access the *Cross References* endpoints you can use the following methods:

.. code:: python

  print ensRest.getXrefsById(id='ENSG00000157764')
  print ensRest.getXrefsByName(species='human', name='BRCA2')
  print ensRest.getXrefsBySymbol(species='human', symbol='BRCA2')

To access the *Information* endpoints you can use the following methods:

.. code:: python

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
  print ensRest.getInfoSpecies(division="ensembl")
  print ensRest.getInfoVariation(species="homo_sapiens")
  # Restrict populations returned to e.g. only populations with LD data. It is highly recommended
  # to set a filter and to avoid loading the complete list of populations.
  print ensRest.getInfoVariationPopulations(species="homo_sapiens", filter="LD")

To access the *Linkage Disequilibrium* endpoints you can use the following methods:

.. code:: python

  print ensRest.getLdId(species="human", id="rs1042779", population_name="1000GENOMES:phase_3:KHV", window_size=500, d_prime=1.0)
  print ensRest.getLdPairwise(species="human", id1="rs6792369", id2="rs1042779")
  print ensRest.getLdRegion(species="human", region="6:25837556..25843455", population_name="1000GENOMES:phase_3:KHV")

To access the *Lookup* endpoints you can use the following methods:

.. code:: python

  print ensRest.getLookupById(id='ENSG00000157764')
  print ensRest.getLookupByMultipleIds(ids=["ENSG00000157764", "ENSG00000248378" ])
  print ensRest.getLookupBySymbol(species="homo_sapiens", symbol="BRCA2", expand=1)
  print ensRest.getLookupByMultipleSymbols(species="homo_sapiens", symbols=["BRCA2", "BRAF"])

To access the *Mapping* endpoints you can use the following methods:

.. code:: python

  print ensRest.getMapCdnaToRegion(id='ENST00000288602', region='100..300')
  print ensRest.getMapCdsToRegion(id='ENST00000288602', region='1..1000')
  print ensRest.getMapAssemblyOneToTwo(species='human', asm_one='NCBI36', region='X:1000000..1000100:1', asm_two='GRCh37')
  print ensRest.getMapTranslationToRegion(id='ENSP00000288602', region='100..300')

To access the *Ontologies and Taxonomy* endpoints you can use the following methods:

.. code:: python

  print ensRest.getAncestorsById(id='GO:0005667')
  print ensRest.getAncestorsChartById(id='GO:0005667')
  print ensRest.getDescendantsById(id='GO:0005667')
  print ensRest.getOntologyById(id='GO:0005667')
  print ensRest.getOntologyByName(name='transcription factor complex')
  print ensRest.getTaxonomyClassificationById(id='9606')
  print ensRest.getTaxonomyById(id='9606')
  print ensRest.getTaxonomyByName(name="Homo%25")

To access the *Overlap* endpoints you can use the following methods:

.. code:: python

  print ensRest.getOverlapById(id="ENSG00000157764", feature="gene")
  print ensRest.getOverlapByRegion(species="human", region="7:140424943-140624564", feature="gene")
  print ensRest.getOverlapByTranslation(id="ENSP00000288602")

To access the *Regulation* endpoints you can use the following method:

.. code:: python

  print ensRest.getRegulatoryFeatureById(species="homo_sapiens", id="ENSR00001348195")

To access the *Sequences* endpoints you can use the following methods:

.. code:: python

  print ensRest.getSequenceById(id='ENSG00000157764')
  print ensRest.getSequenceByMultipleIds(ids=["ENSG00000157764", "ENSG00000248378" ])
  print ensRest.getSequenceByRegion(species='human', region='X:1000000..1000100')
  print ensRest.getSequenceByMultipleRegions(species="homo_sapiens", regions=["X:1000000..1000100:1", "ABBA01004489.1:1..100"])

To access the *Transcript Haplotypes* endpoints you can use the following methods:

.. code:: python

  print ensRest.getTranscripsHaplotypes(species="homo_sapiens", id="ENST00000288602")

To access the *VEP* endpoints you can use the following methods:

.. code:: python

  print ensRest.getVariantConsequencesByHGVSnotation(species="human", hgvs_notation="AGT:c.803T>C")
  print ensRest.getVariantConsequencesById(species='human', id='COSM476')
  print ensRest.getVariantConsequencesByMultipleIds(species="human", ids=[ "rs116035550", "COSM476" ])
  print ensRest.getVariantConsequencesByRegion(species='human', region='9:22125503-22125502:1', allele='C')
  print ensRest.getVariantConsequencesByMultipleRegions(species="human", variants=["21 26960070 rs116645811 G A . . .", "21 26965148 rs1135638 G A . . ." ] )

To access the *Variation* endpoints you can use the following methods:

.. code:: python

  print ensRest.getVariationById(id="rs56116432", species="homo_sapiens")
  print ensRest.getVariationByMultipleIds(ids=["rs56116432", "COSM476" ], species="homo_sapiens")

To access the *Variation GA4GH* endpoints you can use the following methods:

.. code:: python

  print ensRest.searchGA4GHCallSet(variantSetId=1, pageSize=2)
  print ensRest.getGA4GHCallSetById(id="1:NA19777")
  print ensRest.searchGA4GHDataset(pageSize=3)
  print ensRest.getGA4GHDatasetById(id="6e340c4d1e333c7a676b1710d2e3953c")
  print ensRest.getGA4GHVariantsById(id="1:rs1333049")
  print ensRest.searchGA4GHVariants(variantSetId=1, referenceName=22, start=17190024, end=17671934, pageToken="", pageSize=1)
  print ensRest.searchGA4GHVariantsets(datasetId="6e340c4d1e333c7a676b1710d2e3953c", pageToken="", pageSize=2)
  print ensRest.getGA4GHVariantsetsById(id=1)
  print ensRest.searchGA4GHReferences(referenceSetId="GRCh38", pageSize=10)
  print ensRest.getGA4GHReferencesById(id="9489ae7581e14efcad134f02afafe26c")
  print ensRest.searchGA4GHReferenceSets()
  print ensRest.getGA4GHReferenceSetsById(id="GRCh38")


.. _ensembl: http://rest.ensembl.org/
.. _ensemblgenomes: http://rest.ensemblgenomes.org/
.. _sequence: http://rest.ensembl.org/documentation/info/sequence_id
.. _POST sequence: http://rest.ensembl.org/documentation/info/sequence_id_post
