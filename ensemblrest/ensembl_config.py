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

    Configuration information for the EnsEMBL REST API
    
"""

# import pyensemblrest version
import six
from . import __version__

# set urls
ensembl_default_url = 'http://rest.ensembl.org'
ensembl_genomes_url = 'http://rest.ensemblgenomes.org'

# ensembl api lookup table. Specify here function common to ensembl and ensemblgenomes
# REST server
ensembl_api_table = {
    # Archive
    'getArchiveById': {
        'doc': 'Uses the given identifier to return the archived sequence',
        'url': '/archive/id/{{id}}',
        'method': 'GET',
        'content_type': 'application/json'
    },
    'getArchiveByMultipleIds': {
        'doc': 'Retrieve the archived sequence for a set of identifiers',
        'url': '/archive/id',
        'method': 'POST',
        'content_type': 'application/json',
        'post_parameters': ['id']
    },
    

    # Comparative Genomics
    'getGeneTreeById': {
        'doc': 'Retrieves a gene tree dump for a gene tree stable identifier',
        'url': '/genetree/id/{{id}}',
        'method': 'GET',
        'content_type': 'text/x-phyloxml+xml'
    },
    'getGeneTreeMemberById': {
        'doc': 'Retrieves a gene tree that contains the stable identifier',
        'url': '/genetree/member/id/{{id}}',
        'method': 'GET',
        'content_type': 'text/x-phyloxml+xml'
    },
    'getGeneTreeMemberBySymbol': {
        'doc': 'Retrieves a gene tree containing the gene identified by a symbol',
        'url': '/genetree/member/symbol/{{species}}/{{symbol}}',
        'method': 'GET',
        'content_type': 'text/x-phyloxml+xml'
    },
    'getAlignmentByRegion': {
        'doc': 'Retrieves genomic alignments as separate blocks based on a region and species',
        'url': '/alignment/region/{{species}}/{{region}}',
        'method': 'GET',
        'content_type': 'application/json'
    },
    'getHomologyById': {
        'doc': 'Retrieves homology information (orthologs) by Ensembl gene id',
        'url': '/homology/id/{{id}}',
        'method': 'GET',
        'content_type': 'application/json'
    },
    'getHomologyBySymbol': {
        'doc': 'Retrieves homology information (orthologs) by symbol',
        'url': '/homology/symbol/{{species}}/{{symbol}}',
        'method': 'GET',
        'content_type': 'application/json'
    },
    

    # Cross References
    'getXrefsBySymbol': {
        'doc': """Looks up an external symbol and returns all Ensembl objects linked to it. """
               """This can be a display name for a gene/transcript/translation, """
               """a synonym or an externally linked reference. """
               """If a gene's transcript is linked to the supplied symbol """
               """the service will return both gene and transcript (it supports transient links).""",
        'url': '/xrefs/symbol/{{species}}/{{symbol}}',
        'method': 'GET',
        'content_type': 'application/json'
    },
    'getXrefsById': {
        'doc': "Perform lookups of Ensembl Identifiers and retrieve their external references in other databases",
        'url': '/xrefs/id/{{id}}',
        'method': 'GET',
        'content_type': 'application/json'
    },
    'getXrefsByName': {
        'doc': "Performs a lookup based upon the primary accession or display label of an external reference "
               "and returning the information we hold about the entry",
        'url': '/xrefs/name/{{species}}/{{name}}',
        'method': 'GET',
        'content_type': 'application/json'
    },
    

    # Information
    'getInfoAnalysis': {
        'doc': 'List the names of analyses involved in generating Ensembl data',
        'url': '/info/analysis/{{species}}',
        'method': 'GET',
        'content_type': 'application/json'
    },
    'getInfoAssembly': {
        'doc': 'List the currently available assemblies for a species',
        'url': '/info/assembly/{{species}}',
        'method': 'GET',
        'content_type': 'application/json'
    },
    'getInfoAssemblyRegion': {
        'doc': 'Returns information about the specified toplevel sequence region for the given species',
        'url': '/info/assembly/{{species}}/{{region_name}}',
        'method': 'GET',
        'content_type': 'application/json'
    },
    'getInfoBiotypes': {
        'doc': 'List the functional classifications of gene models that Ensembl associates with a particular species. '
               'Useful for restricting the type of genes/transcripts retrieved by other endpoints',
        'url': '/info/biotypes/{{species}}',
        'method': 'GET',
        'content_type': 'application/json',
    },
    'getInfoComparaMethods': {
        'doc': 'List all compara analyses available (an analysis defines the type of comparative data)',
        'url': '/info/compara/methods',
        'method': 'GET',
        'content_type': 'application/json',
    },
    'getInfoComparaSpeciesSets': {
        'doc': 'List all collections of species analysed with the specified compara method',
        'url': '/info/compara/species_sets/{{methods}}',
        'method': 'GET',
        'content_type': 'application/json',
    },
    'getInfoComparas': {
        'doc': 'Lists all available comparative genomics databases and their data release',
        'url': '/info/comparas',
        'method': 'GET',
        'content_type': 'application/json'
    },
    'getInfoData': {
        'doc': 'Shows the data releases available on this REST server. '
               'May return more than one release (unfrequent non-standard Ensembl configuration)',
        'url': '/info/data',
        'method': 'GET',
        'content_type': 'application/json'
    },
    'getInfoExternalDbs': {
        'doc': 'Lists all available external sources for a species',
        'url': '/info/external_dbs/{{species}}',
        'method': 'GET',
        'content_type': 'application/json',
    },    
    'getInfoPing': {
        'doc': 'Checks if the service is alive',
        'url': '/info/ping',
        'method': 'GET',
        'content_type': 'application/json'
    },
    'getInfoRest': {
        'doc': 'Shows the current version of the Ensembl REST API',
        'url': '/info/rest',
        'method': 'GET',
        'content_type': 'application/json'
    },
    'getInfoSoftware': {
        'doc': 'Shows the current version of the Ensembl API used by the REST server',
        'url': '/info/software',
        'method': 'GET',
        'content_type': 'application/json'
    },
    'getInfoSpecies': {
        'doc': 'Lists all available species, their aliases, available adaptor groups and data release',
        'url': '/info/species',
        'method': 'GET',
        'content_type': 'application/json'
    },
    'getInfoVariation': {
        'doc': 'List the variation sources used in Ensembl for a species',
        'url': '/info/variation/{{species}}',
        'method': 'GET',
        # Default ensembl content type
    },
    'getInfoVariationPopulations': {
        'doc': 'List all populations for a species',
        'url': '/info/variation/populations/{{species}}',
        'method': 'GET',
        # Default ensembl content type
    },
    
    
    # Linkage Disequilibrium
    'getLdId': {
        'doc': 'Computes and returns LD values between the given variant and all other variants '
               'in a window centered around the given variant. The window size is set to 500 kb',
        'url': '/ld/{{species}}/{{id}}/{{population_name}}',
        'method': 'GET',
        # Default ensembl content type
    },
    'getLdPairwise': {
        'doc': 'Computes and returns LD values between the given variants',
        'url': '/ld/{{species}}/pairwise/{{id1}}/{{id2}}',
        'method': 'GET',
        # Default ensembl content type
    },
    'getLdRegion': {
        'doc': 'Computes and returns LD values between all pairs of variants in the defined region',
        'url': '/ld/{{species}}/region/{{region}}/{{population_name}}',
        'method': 'GET',
        # Default ensembl content type
    },
    
    
    # Lookup
    'getLookupById': {
        'doc': 'Find the species and database for a single identifier',
        'url': '/lookup/id/{{id}}',
        'method': 'GET',
        'content_type': 'application/json'
    },
    'getLookupByMultipleIds': {
        'doc': 'Find the species and database for several identifiers. '
               'IDs that are not found are returned with no data',
        'url': '/lookup/id',
        'method': 'POST',
        'content_type': 'application/json',
        'post_parameters': ['ids']
    },
    'getLookupBySymbol': {
        'doc': 'Find the species and database for a symbol in a linked external database',
        'url': '/lookup/symbol/{{species}}/{{symbol}}',
        'method': 'GET',
        'content_type': 'application/json',
    },
    'getLookupByMultipleSymbols': {
        'doc': 'Find the species and database for a set of symbols in a linked external database. '
               'Unknown symbols are omitted from the response',
        'url': '/lookup/symbol/{{species}}',
        'method': 'POST',
        'content_type': 'application/json',
        'post_parameters': ['symbols']
    },


    # Mapping
    'getMapCdnaToRegion': {
        'doc': 'Convert from cDNA coordinates to genomic coordinates. '
               'Output reflects forward orientation coordinates as returned from the Ensembl API',
        'url': '/map/cdna/{{id}}/{{region}}',
        'method': 'GET',
        'content_type': 'application/json'
    },
    'getMapCdsToRegion': {
        'doc': 'Convert from CDS coordinates to genomic coordinates. '
               'Output reflects forward orientation coordinates as returned from the Ensembl API',
        'url': '/map/cds/{{id}}/{{region}}',
        'method': 'GET',
        'content_type': 'application/json'
    },
    'getMapAssemblyOneToTwo': {
        'doc': 'Convert the co-ordinates of one assembly to another',
        'url': '/map/{{species}}/{{asm_one}}/{{region}}/{{asm_two}}',
        'method': 'GET',
        'content_type': 'application/json'
    },
    'getMapTranslationToRegion': {
        'doc': 'Convert from protein (translation) coordinates to genomic coordinates. '
               'Output reflects forward orientation coordinates as returned from the Ensembl API',
        'url': '/map/translation/{{id}}/{{region}}',
        'method': 'GET',
        'content_type': 'application/json'
    },

    # Ontologies and Taxonomy
    'getAncestorsById': {
        'doc': 'Reconstruct the entire ancestry of a term from is_a and part_of relationships',
        'url': '/ontology/ancestors/{{id}}',
        'method': 'GET',
        'content_type': 'application/json'
    },
    'getAncestorsChartById': {
        'doc': 'Reconstruct the entire ancestry of a term from is_a and part_of relationships',
        'url': '/ontology/ancestors/chart/{{id}}',
        'method': 'GET',
        'content_type': 'application/json'
    },
    'getDescendantsById': {
        'doc': 'Find all the terms descended from a given term. '
               'By default searches are conducted within the namespace of the given identifier',
        'url': '/ontology/descendants/{{id}}',
        'method': 'GET',
        'content_type': 'application/json'
    },
    'getOntologyById': {
        'doc': 'Search for an ontological term by its namespaced identifier',
        'url': '/ontology/id/{{id}}',
        'method': 'GET',
        'content_type': 'application/json'
    },
    'getOntologyByName': {
        'doc': 'Search for a list of ontological terms by their name',
        'url': '/ontology/name/{{name}}',
        'method': 'GET',
        'content_type': 'application/json'
    },
    'getTaxonomyClassificationById': {
        'doc': 'Return the taxonomic classification of a taxon node',
        'url': '/taxonomy/classification/{{id}}',
        'method': 'GET',
        'content_type': 'application/json'
    },
    'getTaxonomyById': {
        'doc': 'Search for a taxonomic term by its identifier or name',
        'url': '/taxonomy/id/{{id}}',
        'method': 'GET',
        'content_type': 'application/json'
    },
    'getTaxonomyByName': {
        'doc': 'Search for a taxonomic id by a non-scientific name',
        'url': '/taxonomy/name/{{name}}',
        'method': 'GET',
        'content_type': 'application/json',
    },

    # Overlap
    'getOverlapById': {
        'doc': 'Retrieves features (e.g. genes, transcripts, variations etc.) '
               'that overlap a region defined by the given identifier',
        'url': '/overlap/id/{{id}}',
        'method': 'GET',
        'content_type': 'application/json',
    },
    'getOverlapByRegion': {
        'doc': 'Retrieves multiple types of features for a given region',
        'url': '/overlap/region/{{species}}/{{region}}',
        'method': 'GET',
        'content_type': 'application/json',
    },
    'getOverlapByTranslation': {
        'doc': 'Retrieve features related to a specific Translation '
               'as described by its stable ID (e.g. domains, variations)',
        'url': '/overlap/translation/{{id}}',
        'method': 'GET',
        'content_type': 'application/json',
    },

    
    # Regulation
    'getRegulatoryFeatureById': {
        'doc': 'Returns a RegulatoryFeature given its stable ID (e.g. ENSR00001348195)',
        'url': '/regulatory/species/{{species}}/id/{{id}}',
        'method': 'GET',
        'content_type': 'application/json'
    },


    # Sequences
    'getSequenceById': {
        'doc': 'Request multiple types of sequence by stable identifier',
        'url': '/sequence/id/{{id}}',
        'method': 'GET',
        'content_type': 'application/json'
    },
    'getSequenceByMultipleIds': {
        'doc': 'Request multiple types of sequence by a stable identifier list',
        'url': '/sequence/id',
        'method': 'POST',
        'content_type': 'application/json',
        'post_parameters': ['ids']
    },
    'getSequenceByRegion': {
        'doc': 'Returns the genomic sequence of the specified region of the given species',
        'url': '/sequence/region/{{species}}/{{region}}',
        'method': 'GET',
        'content_type': 'application/json'
    },
    'getSequenceByMultipleRegions': {
        'doc': 'Request multiple types of sequence by a list of regions',
        'url': '/sequence/region/{{species}}',
        'method': 'POST',
        'content_type': 'application/json',
        'post_parameters': ['regions']
    },


    # Transcript Haplotypes
    'getTranscripsHaplotypes': {
        'doc': 'Computes observed transcript haplotype sequences based on phased genotype data',
        'url': '/transcript_haplotypes/{{species}}/{{id}}',
        'method': 'GET',
        # Default ensembl content type
    },


    # VEP
    'getVariantConsequencesByHGVSnotation': {
        'doc': 'Request multiple types of sequence by a list of regions',
        'url': '/vep/{{species}}/hgvs/{{hgvs_notation}}',
        'method': 'GET',
        'content_type': 'application/json'
    },
    'getVariantConsequencesById': {
        'doc': 'Fetch variant consequences based on a variation identifier',
        'url': '/vep/{{species}}/id/{{id}}',
        'method': 'GET',
        'content_type': 'application/json'
    },
    'getVariantConsequencesByMultipleIds': {
        'doc': 'Fetch variant consequences for multiple ids',
        'url': '/vep/{{species}}/id',
        'method': 'POST',
        'content_type': 'application/json',
        'post_parameters': ['ids']
        
    },
    'getVariantConsequencesByRegion': {
        'doc': 'Fetch variant consequences',
        'url': '/vep/{{species}}/region/{{region}}/{{allele}}',
        'method': 'GET',
        'content_type': 'application/json'
    },
    'getVariantConsequencesByMultipleRegions': {
        'doc': 'Fetch variant consequences for multiple regions',
        'url': '/vep/{{species}}/region',
        'method': 'POST',
        'content_type': 'application/json',
        'post_parameters': ['variants']
    },
    
    
    # Variation
    'getVariationById': {
        'doc': 'Uses a variation identifier (e.g. rsID) to return the variation features',
        'url': '/variation/{{species}}/{{id}}',
        'method': 'GET',
        'content_type': 'application/json'
    },
    'getVariationByMultipleIds': {
        'doc': 'Uses a list of variant identifiers (e.g. rsID) to return the variation features '
               'including optional genotype, phenotype and population data',
        'url': '/variation/{{species}}',
        'method': 'POST',
        'content_type': 'application/json',
        'post_parameters': ['ids']
    },
    
    
    # Variation GA4GH
    'searchGA4GHCallSet': {
        'doc': 'Return a list of sets of genotype calls for specific samples in GA4GH format',
        'url': '/ga4gh/callsets/search',
        'method': 'POST',
        # Default ensembl content type
        'post_parameters': ["variantSetId", "name", "pageToken", "pageSize"],
    },
    'getGA4GHCallSetById': {
        'doc': "Return the GA4GH record for a specific CallSet given its identifier",
        'url': "/ga4gh/callsets/{{id}}",
        'method': 'GET',
        # Default ensembl content type
    },
    'searchGA4GHDataset': {
        'doc': 'Return a list of datasets in GA4GH format',
        'url': '/ga4gh/datasets/search',
        'method': 'POST',
        # Default ensembl content type
        'post_parameters': ["pageToken", "pageSize"],
    },
    'getGA4GHDatasetById': {
        'doc': "Return the GA4GH record for a specific dataset given its identifier",
        'url': "/ga4gh/datasets/{{id}}",
        'method': 'GET',
        # Default ensembl content type
    },
    'getGA4GHVariantsById': {
        'doc': "Return the GA4GH record for a specific variant given its identifier",
        'url': "/ga4gh/variants/{{id}}",
        'method': 'GET',
        # Default ensembl content type
    },
    'searchGA4GHVariants': {
        'doc': 'Return variant call information in GA4GH format for a region on a reference sequence',
        'url': '/ga4gh/variants/search',
        'method': 'POST',
        # Default ensembl content type
        'post_parameters': ["variantSetId", "callSetIds", "referenceName", "start", "end", "pageToken", "pageSize"],
    },
    'searchGA4GHVariantsets': {
        'doc': 'Return a list of variant sets in GA4GH format',
        'url': '/ga4gh/variantsets/search',
        'method': 'POST',
        # Default ensembl content type
        'post_parameters': ["datasetId", "pageToken", "pageSize"],
    },
    'getGA4GHVariantsetsById': {
        'doc': "Return the GA4GH record for a specific VariantSet given its identifier",
        'url': "/ga4gh/variantsets/{{id}}",
        'method': 'GET',
        # Default ensembl content type
    },
    'searchGA4GHReferences': {
        'doc': 'Return a list of reference sequences in GA4GH format',
        'url': '/ga4gh/references/search',
        'method': 'POST',
        # Default ensembl content type
        'post_parameters': ["referenceSetId", "md5checksum", "accession", "pageToken", "pageSize"],
    },
    'getGA4GHReferencesById': {
        'doc': "Return data for a specific reference in GA4GH format by id",
        'url': "/ga4gh/references/{{id}}",
        'method': 'GET',
        # Default ensembl content type
    },
    'searchGA4GHReferenceSets': {
        'doc': 'Return a list of reference sets in GA4GH format',
        'url': '/ga4gh/referencesets/search',
        'method': 'POST',
        # Default ensembl content type
        'post_parameters': ["accession", "pageToken", "pageSize"],
    },
    'getGA4GHReferenceSetsById': {
        'doc': "Return data for a specific reference set in GA4GH format",
        'url': "/ga4gh/referencesets/{{id}}",
        'method': 'GET',
        # Default ensembl content type
    },
}

# ensembl api lookup table. Specific of EnsEMBL genomes REST server. Specify here 
# functions defined in EnsemblGenomes REST server
ensemblgenomes_api_table = {
    # Comparative Genomics
    'getGeneFamilyById': {
        'doc': 'Retrieves gene family information by ID',
        'url': '/family/id/{{id}}',
        'method': 'GET',
        'content_type': 'application/json'
    },
    'getGeneFamilyMemberById': {
        'doc': 'Retrieves gene families to which a gene belongs',
        'url': '/family/member/id/{{id}}',
        'method': 'GET',
        'content_type': 'application/json'
    },
    'getGeneFamilyMemberBySymbol': {
        'doc': 'Retrieves gene families to which a gene belongs',
        'url': '/family/member/symbol/{{species}}/{{symbol}}',
        'method': 'GET',
        'content_type': 'application/json'
    },
    
    
    # Info
    'getInfoEgVersion': {
        'doc': 'Returns the Ensembl Genomes version of the databases backing this service',
        'url': '/info/eg_version',
        'method': 'GET',
        'content_type': 'application/json',
    },
    'getInfoDivisions': {
        'doc': 'Get list of all Ensembl divisions for which information is available',
        'url': '/info/divisions',
        'method': 'GET',
        'content_type': 'application/json',
    },    
    'getInfoGenomesByName': {
        'doc': 'Find information about a given genome',
        'url': '/info/genomes/{{name}}',
        'method': 'GET',
        'content_type': 'application/json',
    },    
    'getInfoGenomes': {
        'doc': 'Find information about all genomes. Response may be very large',
        'url': '/info/genomes',
        'method': 'GET',
        'content_type': 'application/json',
    },    
    'getInfoGenomesByAccession': {
        'doc': 'Find information about genomes containing a specified INSDC accession',
        'url': '/info/genomes/accession/{{division}}',
        'method': 'GET',
        'content_type': 'application/json',
    },    
    'getInfoGenomesByAssembly': {
        'doc': 'Find information about a genome with a specified assembly',
        'url': '/info/genomes/assembly/{{division}}',
        'method': 'GET',
        'content_type': 'application/json',
    },    
    'getInfoGenomesByDivision': {
        'doc': 'Find information about all genomes in a given division. May be large for Ensembl Bacteria',
        'url': '/info/genomes/division/{{division}}',
        'method': 'GET',
        'content_type': 'application/json',
    },    
    'getInfoGenomesByTaxonomy': {
        'doc': 'Find information about all genomes beneath a given node of the taxonomy',
        'url': '/info/genomes/taxonomy/{{division}}',
        'method': 'GET',
        'content_type': 'application/json',
    },

    
    # Lookup
    'getLookupByGenomeName': {
        'doc': 'Query for a named genome and retrieve the gene models',
        'url': '/lookup/genome/{{name}}',
        'method': 'GET',
        'content_type': 'application/json',
    },
}

# Add default ensemblrest methods to ensembgenome methods
for key, value in six.iteritems(ensembl_api_table):
    ensemblgenomes_api_table[key] = value

# http status codes
ensembl_http_status_codes = {
    200: ('OK', 'Request was a success. Only process data from the service when you receive this code'),
    400: ('Bad Request', 'Occurs during exceptional circumstances such as the service is unable to find an ID. '
                         'Check if the response Content-type was JSON. '
                         'If so the JSON object is an exception hash with the message keyed under error'),
    404: ('Not Found', 'Indicates a badly formatted request. Check your URL'),
    415: ('Unsupported Media Type', 'The server is refusing to service the request '
                                    'because the entity of the request is in a format not supported '
                                    'by the requested resource for the requested method'),
    429: ('Too Many Requests', 'You have been rate-limited; wait and retry. '
                               'The headers X-RateLimit-Reset, X-RateLimit-Limit and X-RateLimit-Remaining will '
                               'inform you of how long you have until your limit is reset and what that limit was. '
                               'If you get this response and have not exceeded your limit '
                               'then check if you have made too many requests per second.'),
    500: ('Internal Server Error', 'This error is not documented. Maybe there is an error in user input or '
                                   'REST server could have problems. Try to do the query with curl. '
                                   'If your data input and query are correct, contact ensembl team'),
    503: ('Service Unavailable', 'The service is temporarily down; retry after a pause'),
}

# set user agent
ensembl_user_agent = 'pyEnsemblRest v' + __version__
ensembl_header = {'User-Agent': ensembl_user_agent}
ensembl_content_type = 'application/json'

# define known errors
ensembl_known_errors = [
    "something bad has happened",
    "Something went wrong while fetching from LDFeatureContainerAdaptor",
    "%s timeout" % ensembl_user_agent
]
