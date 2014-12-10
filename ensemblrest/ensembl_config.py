"""
	Configuration information for the EnsEMBL REST API
"""

# import pyensemblrest version
from . import __version__

# set urls
ensembl_default_url = 'http://rest.ensembl.org'
ensembl_genomes_url = 'http://rest.ensemblgenomes.org'

# api lookup table
ensembl_api_table = {
	# Archive
	'getArchiveById': {
		'doc' : 'Uses the given identifier to return the archived sequence',
		'url': '/archive/id/{{id}}',
		'method': 'GET',
		'content_type': 'application/json'
	},
	'getArchiveByMultipleIds': {
		'doc' : 'Retrieve the archived sequence for a set of identifiers',
		'url': '/archive/id',
		'method': 'POST',
		'content_type': 'application/json'
	},
	

	# Comparative Genomics
	# Specific of EnsEMBL genomes REST server
	'getGeneFamilyById': {
		'doc' : 'Retrieves gene family information by ID',
		'url': '/family/id/{{id}}',
		'method': 'GET',
		'content_type': 'application/json'
	},
	#Specific of EnsEMBL genomes REST server
	'getGeneFamilyMemberById': {
		'doc' : 'Retrieves gene families to which a gene belongs',
		'url': '/family/member/id/{{id}}',
		'method': 'GET',
		'content_type': 'application/json'
	},
	#Specific of EnsEMBL genomes REST server
	'getGeneFamilyMemberBySymbol': {
		'doc' : 'Retrieves gene families to which a gene belongs',
		'url': '/family/member/symbol/{{species}}/{{symbol}}',
		'method': 'GET',
		'content_type': 'application/json'
	},
	'getGeneTreeById': {
		'doc' : 'Retrieves a gene tree dump for a gene tree stable identifier',
		'url': '/genetree/id/{{id}}',
		'method': 'GET',
		'content_type': 'text/x-nh'
	},
	'getGeneTreeMemberById': {
		'doc' : 'Retrieves a gene tree that contains the stable identifier',
		'url': '/genetree/member/id/{{id}}',
		'method': 'GET',
		'content_type': 'text/x-phyloxml+xml'
	},
	'getGeneTreeMemberBySymbol': {
		'doc' : 'Retrieves a gene tree containing the gene identified by a symbol',
		'url': '/genetree/member/symbol/{{species}}/{{symbol}}',
		'method': 'GET',
		'content_type': 'text/x-phyloxml+xml'
	},
	'getAlignmentByRegion': {
		'doc' : 'Retrieves genomic alignments as separate blocks based on a region and species',
		'url': '/alignment/region/{{species}}/{{region}}',
		'method': 'GET',
		'content_type': 'application/json'
	},
	'getHomologyById': {
		'doc' : 'Retrieves homology information (orthologs) by Ensembl gene id',
		'url': '/homology/id/{{id}}',
		'method': 'GET',
		'content_type': 'application/json'
	},
	'getHomologyBySymbol': {
		'doc' : 'Retrieves homology information (orthologs) by symbol',
		'url': '/homology/symbol/{{species}}/{{symbol}}',
		'method': 'GET',
		'content_type': 'application/json'
	},
	

	# Cross References
	'getXrefsBySymbol': {
		'doc' : """Looks up an external symbol and returns all Ensembl objects linked to it. This can be a display name for a gene/transcript/translation, a synonym or an externally linked reference. If a gene's transcript is linked to the supplied symbol the service will return both gene and transcript (it supports transient links).""",
		'url': '/xrefs/symbol/{{species}}/{{symbol}}',
		'method': 'GET',
		'content_type': 'application/json'
	},
	'getXrefsById': {
		'doc' : "Perform lookups of Ensembl Identifiers and retrieve their external references in other databases",
		'url': '/xrefs/id/{{id}}',
		'method': 'GET',
		'content_type': 'application/json'
	},
	'getXrefsByName': {
		'doc' : "Performs a lookup based upon the primary accession or display label of an external reference and returning the information we hold about the entry",
		'url': '/xrefs/name/{{species}}/{{name}}',
		'method': 'GET',
		'content_type': 'application/json'
	},
	

	# Information
	'getInfoAnalysis': {
		'doc' : 'List the names of analyses involved in generating Ensembl data',
		'url': '/info/analysis/{{species}}',
		'method': 'GET',
		'content_type': 'application/json'
	},
	'getInfoAssembly': {
		'doc' : 'List the currently available assemblies for a species',
		'url': '/info/assembly/{{species}}',
		'method': 'GET',
		'content_type': 'application/json'
	},
	'getInfoAssemblyRegion': {
		'doc' : 'Returns information about the specified toplevel sequence region for the given species',
		'url': '/info/assembly/{{species}}/{{region_name}}',
		'method': 'GET',
		'content_type': 'application/json'
	},
	'getInfoBiotypes': {
		'doc' : 'List the functional classifications of gene models that Ensembl associates with a particular species. Useful for restricting the type of genes/transcripts retrieved by other endpoints',
		'url': '/info/biotypes/{{species}}',
		'method': 'GET',
		'content_type': 'application/json',
	},
	'getInfoComparaMethods': {
		'doc' : 'List all compara analyses available (an analysis defines the type of comparative data)',
		'url': '/info/compara/methods',
		'method': 'GET',
		'content_type': 'application/json',
	},
	'getInfoComparaSpeciesSets': {
		'doc' : 'List all collections of species analysed with the specified compara method',
		'url': '/info/compara/species_sets/{{methods}}',
		'method': 'GET',
		'content_type': 'application/json',
	},
	'getInfoComparas': {
		'doc' : 'Lists all available comparative genomics databases and their data release',
		'url': '/info/comparas',
		'method': 'GET',
		'content_type': 'application/json'
	},
	'getInfoData': {
		'doc' : 'Shows the data releases available on this REST server. May return more than one release (unfrequent non-standard Ensembl configuration)',
		'url': '/info/data',
		'method': 'GET',
		'content_type': 'application/json'
	},
	#Specific of EnsEMBL genomes REST server
	'getInfoEgVersion': {
		'doc' : 'Returns the Ensembl Genomes version of the databases backing this service',
		'url': '/info/eg_version',
		'method': 'GET',
		'content_type': 'application/json',
	},
	'getInfoExternalDbs': {
		'doc' : 'Lists all available external sources for a species',
		'url': '/info/external_dbs/{{species}}',
		'method': 'GET',
		'content_type': 'application/json',
	},
	#Specific of EnsEMBL genomes REST server
	'getInfoDivisions': {
		'doc' : 'Get list of all Ensembl divisions for which information is available',
		'url': '/info/divisions',
		'method': 'GET',
		'content_type': 'application/json',
	},
	#Specific of EnsEMBL genomes REST server
	'getInfoGenomesByName': {
		'doc' : 'Find information about a given genome',
		'url': '/info/genomes/{{name}}',
		'method': 'GET',
		'content_type': 'application/json',
	},
	#Specific of EnsEMBL genomes REST server
	'getInfoGenomes': {
		'doc' : 'Find information about all genomes. Response may be very large',
		'url': '/info/genomes',
		'method': 'GET',
		'content_type': 'application/json',
	},
	#Specific of EnsEMBL genomes REST server
	'getInfoGenomesByAccession': {
		'doc' : 'Find information about genomes containing a specified INSDC accession',
		'url': '/info/genomes/accession/{{division}}',
		'method': 'GET',
		'content_type': 'application/json',
	},
	#Specific of EnsEMBL genomes REST server
	'getInfoGenomesByAssembly': {
		'doc' : 'Find information about a genome with a specified assembly',
		'url': '/info/genomes/assembly/{{division}}',
		'method': 'GET',
		'content_type': 'application/json',
	},
	#Specific of EnsEMBL genomes REST server
	'getInfoGenomesByDivision': {
		'doc' : 'Find information about all genomes in a given division. May be large for Ensembl Bacteria',
		'url': '/info/genomes/division/{{division}}',
		'method': 'GET',
		'content_type': 'application/json',
	},
	#Specific of EnsEMBL genomes REST server
	'getInfoGenomesByTaxonomy': {
		'doc' : 'Find information about all genomes beneath a given node of the taxonomy',
		'url': '/info/genomes/taxonomy/{{division}}',
		'method': 'GET',
		'content_type': 'application/json',
	},	
	'getInfoPing': {
		'doc' : 'Checks if the service is alive',
		'url': '/info/ping',
		'method': 'GET',
		'content_type': 'application/json'
	},
	'getInfoRest': {
		'doc' : 'Shows the current version of the Ensembl REST API',
		'url': '/info/rest',
		'method': 'GET',
		'content_type': 'application/json'
	},
	'getInfoSoftware': {
		'doc' : 'Shows the current version of the Ensembl API used by the REST server',
		'url': '/info/software',
		'method': 'GET',
		'content_type': 'application/json'
	},
	'getInfoSpecies': {
		'doc' : 'Lists all available species, their aliases, available adaptor groups and data release',
		'url': '/info/species',
		'method': 'GET',
		'content_type': 'application/json'
	},
	

	# Lookup
	'getLookupById': {
		'doc' : 'Find the species and database for a single identifier',
		'url': '/lookup/id/{{id}}',
		'method': 'GET',
		'content_type': 'application/json'
	},
	'getLookupByMultipleIds': {
		'doc' : 'Find the species and database for several identifiers. IDs that are not found are returned with no data',
		'url': '/lookup/id',
		'method': 'POST',
		'content_type': 'application/json'
	},
	#Specific of EnsEMBL genomes REST server
	'getLookupByGenomeName': {
		'doc' : 'Query for a named genome and retrieve the gene models',
		'url': '/lookup/genome/{{name}}',
		'method': 'GET',
		'content_type': 'application/json',
	},
	'getLookupBySpeciesSymbol': {
		'doc' : 'Find the species and database for a symbol in a linked external database',
		'url': '/lookup/symbol/{{species}}/{{symbol}}',
		'method': 'GET',
		'content_type': 'application/json',
	},
	'getLookupByMultipleSpeciesSymbols': {
		'doc' : 'Find the species and database for a set of symbols in a linked external database. Unknown symbols are omitted from the response',
		'url': '/lookup/symbol/{{species}}',
		'method': 'POST',
		'content_type': 'application/json',
	},


	# Mapping
	'getMapCdnaToRegion': {
		'doc' : 'Convert from cDNA coordinates to genomic coordinates. Output reflects forward orientation coordinates as returned from the Ensembl API',
		'url': '/map/cdna/{{id}}/{{region}}',
		'method': 'GET',
		'content_type': 'application/json'
	},
	'getMapCdsToRegion': {
		'doc' : 'Convert from CDS coordinates to genomic coordinates. Output reflects forward orientation coordinates as returned from the Ensembl API',
		'url': '/map/cds/{{id}}/{{region}}',
		'method': 'GET',
		'content_type': 'application/json'
	},
	'getMapAssemblyOneToTwo': {
		'doc' : 'Convert the co-ordinates of one assembly to another',
		'url': '/map/{{species}}/{{asm_one}}/{{region}}/{{asm_two}}',
		'method': 'GET',
		'content_type': 'application/json'
	},
	'getMapTranslationToRegion': {
		'doc' : 'Convert from protein (translation) coordinates to genomic coordinates. Output reflects forward orientation coordinates as returned from the Ensembl API',
		'url': '/map/translation/{{id}}/{{region}}',
		'method': 'GET',
		'content_type': 'application/json'
	},

	# Ontologies and Taxonomy
	'getAncestorsById': {
		'doc' : 'Reconstruct the entire ancestry of a term from is_a and part_of relationships',
		'url': '/ontology/ancestors/{{id}}',
		'method': 'GET',
		'content_type': 'application/json'
	},
	'getAncestorsChartById': {
		'doc' : 'Reconstruct the entire ancestry of a term from is_a and part_of relationships',
		'url': '/ontology/ancestors/chart/{{id}}',
		'method': 'GET',
		'content_type': 'application/json'
	},
	'getDescendantsById': {
		'doc' : 'Find all the terms descended from a given term. By default searches are conducted within the namespace of the given identifier',
		'url': '/ontology/descendants/{{id}}',
		'method': 'GET',
		'content_type': 'application/json'
	},
	'getOntologyById': {
		'doc' : 'Search for an ontological term by its namespaced identifier',
		'url': '/ontology/id/{{id}}',
		'method': 'GET',
		'content_type': 'application/json'
	},
	'getOntologyByName': {
		'doc' : 'Search for a list of ontological terms by their name',
		'url': '/ontology/name/{{name}}',
		'method': 'GET',
		'content_type': 'application/json'
	},
	'getTaxonomyClassificationById': {
		'doc' : 'Return the taxonomic classification of a taxon node',
		'url': '/taxonomy/classification/{{id}}',
		'method': 'GET',
		'content_type': 'application/json'
	},
	'getTaxonomyById': {
		'doc' : 'Search for a taxonomic term by its identifier or name',
		'url': '/taxonomy/id/{{id}}',
		'method': 'GET',
		'content_type': 'application/json'
	},
	'getTaxonomyByName': {
		'doc' : 'Search for a taxonomic id by a non-scientific name',
		'url': '/taxonomy/name/{{name}}',
		'method': 'GET',
		'content_type': 'application/json',
	},

	# Overlap
	'getOverlapById': {
		'doc' : 'Retrieves features (e.g. genes, transcripts, variations etc.) that overlap a region defined by the given identifier',
		'url': '/overlap/id/{{id}}',
		'method': 'GET',
		'content_type': 'application/json',
	},
	'getOverlapByRegion': {
		'doc' : 'Retrieves multiple types of features for a given region',
		'url': '/overlap/region/{{species}}/{{region}}',
		'method': 'GET',
		'content_type': 'application/json',
	},
	'getOverlapByTranslation': {
		'doc' : 'Retrieve features related to a specific Translation as described by its stable ID (e.g. domains, variations)',
		'url': '/overlap/translation/{{id}}',
		'method': 'GET',
		'content_type': 'application/json',
	},

	
	# Regulation
	'getRegulatoryFeatureById': {
		'doc' : 'Returns a RegulatoryFeature given its stable ID (e.g. ENSR00001348195)',
		'url': '/regulatory/{{species}}/{{id}}',
		'method': 'GET',
		'content_type': 'application/json'
	},


	# Sequences
	'getSequenceById': {
		'doc' : 'Request multiple types of sequence by stable identifier',
		'url': '/sequence/id/{{id}}',
		'method': 'GET',
		'content_type': 'application/json'
	},
	#Specific of EnsEMBL REST server ?
	'getSequenceByMultipleIds': {
		'doc' : 'Request multiple types of sequence by a stable identifier list',
		'url': '/sequence/id',
		'method': 'POST',
		'content_type': 'application/json'
	},
	'getSequenceByRegion': {
		'doc' : 'Returns the genomic sequence of the specified region of the given species',
		'url': '/sequence/region/{{species}}/{{region}}',
		'method': 'GET',
		'content_type': 'application/json'
	},
	#Specific of EnsEMBL REST server ?
	'getSequenceByMultipleRegions': {
		'doc' : 'Request multiple types of sequence by a list of regions',
		'url': '/sequence/region/{{species}}',
		'method': 'POST',
		'content_type': 'application/json'
	},


	# VEP
	'getVariantConsequencesByHGVSnotation': {
		'doc' : 'Request multiple types of sequence by a list of regions',
		'url': '/vep/{{species}}/hgvs/{{hgvs_notation}}',
		'method': 'GET',
		'content_type': 'application/json'
	},
	'getVariantConsequencesById': {
		'doc' : 'Fetch variant consequences based on a variation identifier',
		'url': '/vep/{{species}}/id/{{id}}',
		'method': 'GET',
		'content_type': 'application/json'
	},
	'getVariantConsequencesByMultipleIds': {
		'doc' : 'Fetch variant consequences for multiple ids',
		'url': '/vep/{{species}}/id',
		'method': 'POST',
		'content_type': 'application/json'
	},
	'getVariantConsequencesByRegion': {
		'doc' : 'Fetch variant consequences',
		'url': '/vep/{{species}}/region/{{region}}/{{allele}}',
		'method': 'GET',
		'content_type': 'application/json'
	},
	'getVariantConsequencesByMultipleRegions': {
		'doc' : 'Fetch variant consequences for multiple regions',
		'url' : '/vep/{{species}}/region',
		'method' : 'POST',
		'content_type': 'application/json',
	},
	
	
	# Variation
	'getVariationBySpeciesId': {
		'doc' : 'Uses a variation identifier (e.g. rsID) to return the variation features',
		'url': '/variation/{{species}}/{{id}}',
		'method': 'GET',
		'content_type': 'application/json'
	},
	
}

# http status codes
ensembl_http_status_codes = {
	200: ('OK', 'Request was a success. Only process data from the service when you receive this code'),
	400: ('Bad Request', 'Occurs during exceptional circumstances such as the service is unable to find an ID. Check if the response Content-type was JSON. If so the JSON object is an exception hash with the message keyed under error'),
	404: ('Not Found', 'Indicates a badly formatted request. Check your URL'),
	415: ('Unsupported Media Type', 'The server is refusing to service the request because the entity of the request is in a format not supported by the requested resource for the requested method'),
	429: ('Too Many Requests', 'You have been rate-limited; wait and retry. The headers X-RateLimit-Reset, X-RateLimit-Limit and X-RateLimit-Remaining will inform you of how long you have until your limit is reset and what that limit was. If you get this response and have not exceeded your limit then check if you have made too many requests per second.'),
	500: ('Internal Server Error', 'This error is not documented. Maybe there is an error in user input or REST server could have problems. Try to do the query with curl. If your data input and query are correct, contact ensembl team'),
	503: ('Service Unavailable', 'The service is temporarily down; retry after a pause'),
}

# set user agent
ensembl_user_agent = {'User-Agent': 'pyEnsemblRest v' + __version__}
ensembl_content_type = {'Content-Type': 'application/json'}
