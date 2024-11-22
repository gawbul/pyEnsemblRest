# pyEnsemblRest

`pyEnsemblRest` is a simple Python client for the Ensembl REST API

[![GitHub Build Status](https://github.com/gawbul/pyEnsemblRest/actions/workflows/pull_request.yaml/badge.svg)](https://github.com/gawbul/pyEnsemblRest/actions/workflows/pull_request.yaml)

[![GitHub Build Status](https://github.com/gawbul/pyEnsemblRest/actions/workflows/push_tag.yaml/badge.svg)](https://github.com/gawbul/pyEnsemblRest/actions/workflows/push_tag.yaml)

[![Coveralls Code Coverage](https://coveralls.io/repos/github/gawbul/pyEnsemblRest/badge.svg?branch=main)](https://coveralls.io/github/gawbul/pyEnsemblRest?branch=main)

[![Scrutinizer Code Quality](https://scrutinizer-ci.com/g/gawbul/pyEnsemblRest/badges/quality-score.png?b=main)](https://scrutinizer-ci.com/g/gawbul/pyEnsemblRest/?branch=main)

[![Gitter Chat](https://img.shields.io/gitter/room/gawbul/pyEnsemblRest.js.svg?maxAge=2592000)](https://gitter.im/gawbul/pyEnsemblRest)

[![PyPi Package](https://img.shields.io/pypi/v/pyensemblrest.svg?maxAge=2592000)](https://pypi.python.org/pypi/pyensemblrest)

[![GitHub Downloads (all assets, all releases)](https://img.shields.io/github/downloads/gawbul/pyEnsemblRest/total)](https://github.com/gawbul/pyEnsemblRest/releases)

[![PyPi Downloads](https://img.shields.io/pypi/dd/pyensemblrest.svg?maxAge=2592000)](https://img.shields.io/pypi/dd/pyensemblrest.svg?maxAge=2592000)

## License

pyEnsemblRest - A client for the Ensembl REST API written in the Python
programming language

Copyright (C) 2013-2024, Steve Moss

pyEnsemblRest is free software: you can redistribute it and/or modify it
under the terms of the GNU General Public License as published by the
Free Software Foundation, either version 3 of the License, or (at your
option) any later version.

pyEnsemblRest is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General
Public License for more details.

You should have received a copy of the GNU General Public License along
with pyEnsemblRest. If not, see \<<http://www.gnu.org/licenses/>\>.

## Installation

### Using pip

Simply type:

``` bash
pip install pyensemblrest
```

### From source

Clone the pyEnsemblRest repository then install the package from source:

``` bash
git clone https://github.com/gawbul/pyEnsemblRest.git
cd pyEnsemblRest
make install
```

## Usage

To import and setup a new EnsemblRest object you should do the following:

``` python
from pyensemblrest import EnsemblRest
ensRest = EnsemblRest()
```

The `EnsemblRest()` instance points to <https://rest.ensembl.org/> by default.

To use a custom Ensembl REST server you should setup the `EnsemblRest()` as follows:

``` python
from pyensemblrest import EnsemblRest
# setup rest object to point to localhost server. The 3000 stands for REST default port
ensRest = EnsemblRest(base_url='http://localhost:3000')
```

You may also provide proxy server settings in the form of a dict, as follows:

``` python
from pyensemblrest import EnsemblRest
# setup rest object to point to a proxy server
ensRest = EnsemblRest(proxies={'http':'proxy.address.com:3128', 'https':'proxy.address.com:3128'})
```

EnsEMBL has a rate-limit policy to deal with requests. You can do up to
15 requests per second. You could wait a little during your requests:

``` python
from time import sleep
# sleep for a second so we don't get rate-limited
sleep(1)
```

Alternatively this library verifies and limits your requests to 15
requests per second. Avoid running different python processes to get your
data, otherwise you will be blacklisted by the Ensembl team. If you have to
do a lot or requests, consider using POST supported endpoints, or
contact the Ensembl team to add POST support to endpoints of your interest.

### GET endpoints

EnsemblRest class methods are not defined in the libraries so you
cannot see docstrings using the help() method on the python or
ipython terminal. However you can see all methods available for
the [ensembl](https://rest.ensembl.org/) REST server once the class
is instantiated. To get help on a particular method, please refer to
Ensembl help documentation for different endpoints in the
[Ensembl](https://rest.ensembl.org/) REST service. If you look at the
[sequence](https://rest.ensembl.org/documentation/info/sequence_id)
endpoint documentation, you will find optional and required parameters.
Required parameters must be specified in order to work properly,
otherwise you will get an exception. Optional parameters may be
specified or not, depending on your request. In all cases parameter names
are the same as those used in documentation. For example to get data using
the [sequence](http://rest.ensembl.org/documentation/info/sequence_id)
endpoint, you must specify at least the required parameters:

``` python
seq = ensRest.getSequenceById(id='ENSG00000157764')
```

In order to mask the sequence and to expand the 5\' UTR you may set
optional parameters using the same parameter described in the documentation:

``` python
seq = ensRest.getSequenceById(id='ENSG00000157764', mask="soft", expand_5prime=1000)
```

Multiple values for certain parameters (for GET methods) can be
submitted in a list. For example, to get the same result for

``` bash
curl 'http://rest.ensembl.org/overlap/region/human/7:140424943-140624564?feature=gene;feature=transcript;feature=cds;feature=exon' -H 'Content-type:application/json'
```

as described in [overlap region](https://rest.ensembl.org/documentation/info/overlap_region)
GET endpoint, you can use the following function and parameters:

``` python
data = ensRest.getOverlapByRegion(species="human", region="7:140424943-140624564", feature=["gene", "transcript", "cds", "exon"])
```

### POST endpoints

POST endpoints can be used as the GET endpoints, the only difference is
that they support parameters in a python list in order to perform multiple
queries on the same Ensembl endpoint. The parameter names are the same as
used in the documentation, for example we can use the [POST sequence](https://rest.ensembl.org/documentation/info/sequence_id_post)
endpoint in the following way:

``` python
seqs = ensRest.getSequenceByMultipleIds(ids=["ENSG00000157764", "ENSG00000248378"])
```

where the example values
`{ "ids": ["ENSG00000157764", "ENSG00000248378"] }` are converted to
the non-positional argument `ids=["ENSG00000157764", "ENSG00000248378"]`.
As with the previous example, we can add optional parameters:

``` python
seqs = ensRest.getSequenceByMultipleIds(ids=["ENSG00000157764", "ENSG00000248378"], mask="soft")
```

### Change the default output format

You can change the default output format by passing a supported
`Content-type` using the `content_type` parameter, for example:

``` python
plain_xml = ensRest.getArchiveById(id='ENSG00000157764', content_type="text/xml")
```

For a complete list of supported `Content-type` see [Supported MIME
Types](https://github.com/Ensembl/ensembl-rest/wiki/Output-formats#supported-mime-types)
from the Ensembl REST documentation. You also need to check if the same
`Content-type` is supported in the EnsEMBL endpoint description.

### Rate limiting

Sometime you can be rate limited if you are querying EnsEMBL REST
services with more than one concurrent process, or by [sharing ip
addresses](https://github.com/Ensembl/ensembl-rest/wiki#example-clients).
In such case, you can receive a message like this:

``` bash
ensemblrest.exceptions.EnsemblRestRateLimitError: EnsEMBL REST API returned a 429 (Too Many Requests): You have been rate-limited; wait and retry. The headers X-RateLimit-Reset, X-RateLimit-Limit and X-RateLimit-Remaining will inform you of how long you have until your limit is reset and what that limit was. If you get this response and have not exceeded your limit then check if you have made too many requests per second. (Rate limit hit:  Retry after 2 seconds)
```

Even though this library tries to do 15 request per seconds, you should
avoid running multiple EnsEMBL REST clients. To deal which such problems
without interrupting your code, try to deal with the exceptions; For
example:

``` python
# import required modules
import os
import sys
import time
import logging

# get ensembl REST modules and exception
from pyensemblrest import EnsemblRest
from pyensemblrest import EnsemblRestRateLimitError

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
```

### Methods list

Here is a list of all methods defined. Methods called by `ensRest`
instance are specific to the [Ensembl](https://rest.ensembl.org/)
REST server.

To access the *Archive* endpoints you can use the following methods:

``` python
print(ensRest.getArchiveById(id="ENSG00000157764"))
print(ensRest.getArchiveByMultipleIds(id=["ENSG00000157764", "ENSG00000248378"]))
```

To access the *Comparative Genomics* endpoints you can use the following
methods:

``` python
print(ensRest.getCafeGeneTreeById(id="ENSGT00390000003602"))
print(ensRest.getCafeGeneTreeMemberBySymbol(species="human", symbol="BRCA2"))
print(ensRest.getCafeGeneTreeMemberById(species="human", id="ENSG00000167664"))
print(ensRest.getGeneTreeById(id="ENSGT00390000003602"))
print(ensRest.getGeneTreeMemberBySymbol(species="human", symbol="BRCA2"))
print(ensRest.getGeneTreeMemberById(species="human", id="ENSG00000167664"))
print(
    ensRest.getAlignmentByRegion(
        species="human",
        region="X:1000000..1000100:1",
        species_set_group="mammals",
    )
)
print(ensRest.getHomologyById(species="human", id="ENSG00000157764"))
print(ensRest.getHomologyBySymbol(species="human", symbol="BRCA2"))
```

To access the *Cross References* endpoints you can use the following
methods:

``` python
print(ensRest.getXrefsBySymbol(species="human", symbol="BRCA2"))
print(ensRest.getXrefsById(id="ENSG00000157764"))
print(ensRest.getXrefsByName(species="human", name="BRCA2"))
```

To access the *Information* endpoints you can use the following methods:

``` python
print(ensRest.getInfoAnalysis(species="homo_sapiens"))
print(
    ensRest.getInfoAssembly(species="homo_sapiens", bands=1)
)  # bands is an optional parameter
print(ensRest.getInfoAssemblyRegion(species="homo_sapiens", region_name="X"))
ensRest.timeout = 300
print(ensRest.getInfoBiotypes(species="homo_sapiens"))  # this keeps timing out
ensRest.timeout = 60
print(ensRest.getInfoBiotypesByGroup(group="coding", object_type="gene"))
print(ensRest.getInfoBiotypesByName(name="protein_coding", object_type="gene"))
print(ensRest.getInfoComparaMethods())
print(ensRest.getInfoComparaSpeciesSets(methods="EPO"))
print(ensRest.getInfoComparas())
print(ensRest.getInfoData())
print(ensRest.getInfoEgVersion())
print(ensRest.getInfoExternalDbs(species="homo_sapiens"))
print(ensRest.getInfoDivisions())
print(ensRest.getInfoGenomesByName(name="arabidopsis_thaliana"))
print(ensRest.getInfoGenomesByAccession(accession="U00096"))
print(ensRest.getInfoGenomesByAssembly(assembly_id="GCA_902167145.1"))
print(ensRest.getInfoGenomesByDivision(division="EnsemblPlants"))
print(ensRest.getInfoGenomesByTaxonomy(taxon_name="Homo sapiens"))
print(ensRest.getInfoPing())
print(ensRest.getInfoRest())
print(ensRest.getInfoSoftware())
print(ensRest.getInfoSpecies())
print(ensRest.getInfoVariationBySpecies(species="homo_sapiens"))
print(ensRest.getInfoVariationConsequenceTypes())
print(
    ensRest.getInfoVariationPopulationIndividuals(
        species="human", population_name="1000GENOMES:phase_3:ASW"
    )
)
# Restrict populations returned to e.g. only populations with LD data. It is highly recommended
# to set a filter and to avoid loading the complete list of populations.
print(ensRest.getInfoVariationPopulations(species="homo_sapiens", filter="LD"))
```

To access the *Linkage Disequilibrium* endpoints you can use the
following methods:

``` python
print(
    ensRest.getLdId(
        species="homo_sapiens",
        id="rs56116432",
        population_name="1000GENOMES:phase_3:KHV",
        window_size=500,
        d_prime=1.0,
    )
)
print(ensRest.getLdPairwise(species="homo_sapiens", id1="rs6792369", id2="rs1042779"))
print(
    ensRest.getLdRegion(
        species="homo_sapiens",
        region="6:25837556..25843455",
        population_name="1000GENOMES:phase_3:KHV",
    )
)
```

To access the *Lookup* endpoints you can use the following methods:

``` python
print(ensRest.getLookupById(id="ENSG00000157764"))
print(ensRest.getLookupByMultipleIds(ids=["ENSG00000157764", "ENSG00000248378"]))
print(ensRest.getLookupBySymbol(species="homo_sapiens", symbol="BRCA2", expand=1))
print(
    ensRest.getLookupByMultipleSymbols(
        species="homo_sapiens", symbols=["BRCA2", "BRAF"]
    )
)
```

To access the *Mapping* endpoints you can use the following methods:

``` python
print(ensRest.getMapCdnaToRegion(id="ENST00000288602", region="100..300"))
print(ensRest.getMapCdsToRegion(id="ENST00000288602", region="1..1000"))
print(
    ensRest.getMapAssemblyOneToTwo(
        species="homo_sapiens",
        asm_one="GRCh37",
        region="X:1000000..1000100:1",
        asm_two="GRCh38",
    )
)
print(ensRest.getMapTranslationToRegion(id="ENSP00000288602", region="100..300"))
```

To access the *Ontologies and Taxonomy* endpoints you can use the
following methods:

``` python
print(ensRest.getAncestorsById(id="GO:0005667"))
print(ensRest.getAncestorsChartById(id="GO:0005667"))
print(ensRest.getDescendantsById(id="GO:0005667"))
print(ensRest.getOntologyById(id="GO:0005667"))
print(ensRest.getOntologyByName(name="transcription factor complex"))
print(ensRest.getTaxonomyClassificationById(id="9606"))
print(ensRest.getTaxonomyById(id="9606"))
print(ensRest.getTaxonomyByName(name="Homo%25"))
```

To access the *Overlap* endpoints you can use the following methods:

``` python
print(ensRest.getOverlapById(id="ENSG00000157764", feature="gene"))
print(
    ensRest.getOverlapByRegion(
        species="homo_sapiens", region="X:1..1000:1", feature="gene"
    )
)
print(ensRest.getOverlapByTranslation(id="ENSP00000288602"))
```

To access the *Phenotype annotations* endpoints you can use the following methods:

``` python
print(ensRest.getPhenotypeByAccession(species="homo_sapiens", accession="EFO:0003900"))
print(ensRest.getPhenotypeByGene(species="homo_sapiens", gene="ENSG00000157764"))
print(
    ensRest.getPhenotypeByRegion(species="homo_sapiens", region="9:22125500-22136000:1")
)
print(ensRest.getPhenotypeByTerm(species="homo_sapiens", term="coffee consumption"))
```

To access the *Regulation* endpoints you can use the following method:

``` python
print(
    ensRest.getRegulationBindingMatrix(
        species="homo_sapiens", binding_matrix="ENSPFM0001"
    )
)
```

To access the *Sequences* endpoints you can use the following methods:

``` python
print(ensRest.getSequenceById(id="ENSG00000157764"))
print(ensRest.getSequenceByMultipleIds(ids=["ENSG00000157764", "ENSG00000248378"]))
print(
    ensRest.getSequenceByRegion(species="homo_sapiens", region="X:1000000..1000100:1")
)
print(
    ensRest.getSequenceByMultipleRegions(
        species="homo_sapiens",
        regions=["X:1000000..1000100:1", "ABBA01004489.1:1..100"],
    )
)
```

To access the *Transcript Haplotypes* endpoints you can use the
following method:

``` python
print(ensRest.getTranscriptHaplotypes(species="homo_sapiens", id="ENST00000288602"))
```

To access the *VEP* endpoints you can use the following methods:

``` python
print(
    ensRest.getVariantConsequencesByHGVSNotation(
        species="homo_sapiens", hgvs_notation="ENST00000366667:c.803C>T"
    )
)
print(
    ensRest.getVariantConsequencesByMultipleHGVSNotations(
        species="homo_sapiens",
        hgvs_notations=["ENST00000366667:c.803C>T", "9:g.22125504G>C"],
    )
)
print(ensRest.getVariantConsequencesById(species="homo_sapiens", id="rs56116432"))
print(
    ensRest.getVariantConsequencesByMultipleIds(
        species="homo_sapiens", ids=["rs56116432", "COSM476", "__VAR(sv_id)__"]
    )
)
print(
    ensRest.getVariantConsequencesByRegion(
        species="homo_sapiens", region="9:22125503-22125502:1", allele="C"
    )
)
print(
    ensRest.getVariantConsequencesByMultipleRegions(
        species="homo_sapiens",
        variants=[
            "21 26960070 rs116645811 G A . . .",
            "21 26965148 rs1135638 G A . . .",
        ],
    )
)
```

To access the *Variation* endpoints you can use the following methods:

``` python
print(ensRest.getVariationRecoderById(species="homo_sapiens", id="rs56116432"))
print(
    ensRest.getVariationRecoderByMultipleIds(
        species="homo_sapiens", ids=["rs56116432", "rs1042779"]
    )
)
print(ensRest.getVariationById(species="homo_sapiens", id="rs56116432"))
print(ensRest.getVariationByPMCID(species="homo_sapiens", pmcid="PMC5002951"))
print(ensRest.getVariationByPMID(species="homo_sapiens", pmid="26318936"))
print(
    ensRest.getVariationByMultipleIds(
        species="homo_sapiens", ids=["rs56116432", "COSM476", "__VAR(sv_id)__"]
    )
)
```

To access the *Variation GA4GH* endpoints you can use the following
methods:

``` python
print(ensRest.getGA4GHBeacon())
print(
    ensRest.getGA4GHBeaconQuery(
        alternateBases="C",
        assemblyId="GRCh38",
        end="23125503",
        referenceBases="G",
        referenceName="9",
        start="22125503",
        variantType="DUP",
    )
)
print(
    ensRest.postGA4GHBeaconQuery(
        alternateBases="C",
        assemblyId="GRCh38",
        end="23125503",
        referenceBases="G",
        referenceName="9",
        start="22125503",
        variantType="DUP",
    )
)
print(ensRest.getGA4GHFeaturesById(id="ENST00000408937.7"))
ensRest.timeout = 180
print(
    ensRest.searchGA4GHFeatures(
        parentId="ENST00000408937.7",
        featureSetId="",
        featureTypes=["cds"],
        end=220023,
        referenceName="X",
        start=197859,
        pageSize=1,
    )
)  # this keeps timing out
ensRest.timeout = 60
print(ensRest.searchGA4GHCallset(variantSetId=1, pageSize=2))
print(ensRest.getGA4GHCallsetById(id="1"))
print(ensRest.searchGA4GHDatasets(pageSize=3))
print(ensRest.getGA4GHDatasetsById(id="6e340c4d1e333c7a676b1710d2e3953c"))
print(ensRest.searchGA4GHFeaturesets(datasetId="Ensembl"))
print(ensRest.getGA4GHFeaturesetsById(id="Ensembl"))
print(ensRest.getGA4GHVariantsById(id="1:rs1333049"))
print(
    ensRest.searchGA4GHVariantAnnotations(
        variantAnnotationSetId="Ensembl",
        referenceId="9489ae7581e14efcad134f02afafe26c",
        start=25221400,
        end=25221500,
        pageSize=1,
    )
)
print(
    ensRest.searchGA4GHVariants(
        variantSetId=1,
        referenceName=22,
        start=25455086,
        end=25455087,
        pageToken="",
        pageSize=1,
    )
)
print(
    ensRest.searchGA4GHVariantsets(
        datasetId="6e340c4d1e333c7a676b1710d2e3953c", pageToken="", pageSize=2
    )
)
print(ensRest.getGA4GHVariantsetsById(id=1))
print(ensRest.searchGA4GHReferences(referenceSetId="GRCh38", pageSize=10))
print(ensRest.getGA4GHReferencesById(id="9489ae7581e14efcad134f02afafe26c"))
print(ensRest.searchGA4GHReferencesets())
print(ensRest.getGA4GHReferencesetsById(id="GRCh38"))
print(ensRest.searchGA4GHVariantAnnotationsets(variantSetId="Ensembl"))
print(ensRest.getGA4GHVariantAnnotationsetsById(id="Ensembl"))
```
