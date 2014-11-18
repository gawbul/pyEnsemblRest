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
		'url': '/archive/id/{{id}}',
		'method': 'GET',
		'content_type': 'application/json'
	},	

	# Comparative Genomics
	'getGeneTreeById': {
		'url': '/genetree/id/{{id}}',
		'method': 'GET',
		'content_type': 'text/x-nh'
	},
	'getGeneTreeByMemberId': {
		'url': '/genetree/member/id/{{id}}',
		'method': 'GET',
		'content_type': 'text/x-phyloxml+xml'
	},
	'getGeneTreeByMemberSymbol': {
		'url': '/genetree/member/symbol/{{species}}/{{symbol}}',
		'method': 'GET',
		'content_type': 'text/x-phyloxml+xml'
	},
	'getAlignmentBySpeciesRegion': {
		'url': '/alignment/region/{{species}}/{{region}}',
		'method': 'GET',
		'content_type': 'application/json'
	},
	'getHomologyById': {
		'url': '/homology/id/{{id}}',
		'method': 'GET',
		'content_type': 'application/json'
	},
	'getHomologyBySymbol': {
		'url': '/homology/symbol/{{species}}/{{symbol}}',
		'method': 'GET',
		'content_type': 'application/json'
	},

	# Cross References
	'getXrefsById': {
		'url': '/xrefs/id/{{id}}',
		'method': 'GET',
		'content_type': 'application/json'
	},
	'getXrefsByName': {
		'url': '/xrefs/name/{{species}}/{{name}}',
		'method': 'GET',
		'content_type': 'application/json'
	},
	'getXrefsBySymbol': {
		'url': '/xrefs/symbol/{{species}}/{{symbol}}',
		'method': 'GET',
		'content_type': 'application/json'
	},

	# Information
	'getInfoAnalysis': {
		'url': '/info/analysis/{{species}}',
		'method': 'GET',
		'content_type': 'application/json'
	},
	'getInfoAssembly': {
		'url': '/info/assembly/{{species}}',
		'method': 'GET',
		'content_type': 'application/json'
	},
	'getInfoAssemblyRegion': {
		'url': '/info/assembly/{{species}}/{{region_name}}',
		'method': 'GET',
		'content_type': 'application/json'
	},
	'getInfoBiotypes': {
		'url': '/info/biotypes/{{species}}',
		'method': 'GET',
		'content_type': 'application/json',
	},
	'getInfoComparaMethods': {
		'url': '/info/compara/methods',
		'method': 'GET',
		'content_type': 'application/json',
	},
	'getInfoComparaSpeciesSets': {
		'url': '/info/compara/species_sets/{{methods}}',
		'method': 'GET',
		'content_type': 'application/json',
	},
	'getInfoComparas': {
		'url': '/info/comparas',
		'method': 'GET',
		'content_type': 'application/json'
	},
	'getInfoData': {
		'url': '/info/data',
		'method': 'GET',
		'content_type': 'application/json'
	},
	'getInfoEgVersion': {
		'url': '/info/eg_version',
		'method': 'GET',
		'content_type': 'application/json',
	},
	'getInfoExternalDbs': {
		'url': '/info/external_dbs/{{species}}',
		'method': 'GET',
		'content_type': 'application/json',
	},
	'getInfoDivisions': {
		'url': '/info/divisions',
		'method': 'GET',
		'content_type': 'application/json',
	},
	'getInfoGenomesByName': {
		'url': '/info/genomes/{{name}}',
		'method': 'GET',
		'content_type': 'application/json',
	},
	'getInfoGenomesByAccession': {
		'url': '/info/genomes/{{accession}}',
		'method': 'GET',
		'content_type': 'application/json',
	},
	'getInfoGenomesByAssembly': {
		'url': '/info/genomes/{{assembly}}',
		'method': 'GET',
		'content_type': 'application/json',
	},
	'getInfoGenomesByDivision': {
		'url': '/info/genomes/{{division}}',
		'method': 'GET',
		'content_type': 'application/json',
	},
	'getInfoGenomesByTaxonomy': {
		'url': '/info/genomes/{{taxonomy}}',
		'method': 'GET',
		'content_type': 'application/json',
	},	
	'getInfoPing': {
		'url': '/info/ping',
		'method': 'GET',
		'content_type': 'application/json'
	},
	'getInfoRest': {
		'url': '/info/rest',
		'method': 'GET',
		'content_type': 'application/json'
	},
	'getInfoSoftware': {
		'url': '/info/software',
		'method': 'GET',
		'content_type': 'application/json'
	},
	'getInfoSpecies': {
		'url': '/info/species',
		'method': 'GET',
		'content_type': 'application/json'
	},

	# Lookup
	'getLookupById': {
		'url': '/lookup/id/{{id}}',
		'method': 'GET',
		'content_type': 'application/json'
	},
	'getLookupByGenomeName': {
		'url': '/lookup/genome/{{name}}',
		'method': 'GET',
		'content_type': 'application/json',
	},
	'getLookupBySpeciesSymbol': {
		'url': '/lookup/symbol/{{species}}/{{symbol}}',
		'method': 'GET',
		'content_type': 'application/json',
	},

	# Mapping
	'getMapAssemblyOneToTwo': {
		'url': '/map/{{species}}/{{asm_one}}/{{region}}/{{asm_two}}',
		'method': 'GET',
		'content_type': 'application/json'
	},
	'getMapCdnaToRegion': {
		'url': '/map/cdna/{{id}}/{{region}}',
		'method': 'GET',
		'content_type': 'application/json'
	},
	'getMapCdsToRegion': {
		'url': '/map/cds/{{id}}/{{region}}',
		'method': 'GET',
		'content_type': 'application/json'
	},
	'getMapTranslationToRegion': {
		'url': '/map/translation/{{id}}/{{region}}',
		'method': 'GET',
		'content_type': 'application/json'
	},

	# Ontologies and Taxonomy
	'getAncestorsById': {
		'url': '/ontology/ancestors/{{id}}',
		'method': 'GET',
		'content_type': 'application/json'
	},
	'getAncestorsChartById': {
		'url': '/ontology/ancestors/chart/{{id}}',
		'method': 'GET',
		'content_type': 'application/json'
	},
	'getDescendentsById': {
		'url': '/ontology/descendents/{{id}}',
		'method': 'GET',
		'content_type': 'application/json'
	},
	'getOntologyById': {
		'url': '/ontology/id/{{id}}',
		'method': 'GET',
		'content_type': 'application/json'
	},
	'getOntologyByName': {
		'url': '/ontology/name/{{name}}',
		'method': 'GET',
		'content_type': 'application/json'
	},
	'getTaxonomyClassificationById': {
		'url': '/taxonomy/classification/{{id}}',
		'method': 'GET',
		'content_type': 'application/json'
	},
	'getTaxonomyById': {
		'url': '/taxonomy/id/{{id}}',
		'method': 'GET',
		'content_type': 'application/json'
	},
	'getTaxonomyByName': {
		'url': '/taxonomy/name/{{name}}',
		'method': 'GET',
		'content_type': 'application/json',
	},

	# Overlap
	'getOverlapById': {
		'url': '/overlap/id/{{id}}',
		'method': 'GET',
		'content_type': 'application/json',
	},
	'getOverlapBySpeciesRegion': {
		'url': '/overlap/region/{{species}}/{{region}}',
		'method': 'GET',
		'content_type': 'application/json',
	},
	'getOverlapByTranslation': {
		'url': '/overlap/translation/{{id}}',
		'method': 'GET',
		'content_type': 'application/json',
	},

	# Sequences
	'getSequenceById': {
		'url': '/sequence/id/{{id}}',
		'method': 'GET',
		'content_type': 'application/json'
	},
	'getSequenceByRegion': {
		'url': '/sequence/region/{{species}}/{{region}}',
		'method': 'GET',
		'content_type': 'application/json'
	},

	# Variation
	'getVariationBySpeciesId': {
		'url': '/vep/{{species}}/{{id}}',
		'method': 'GET',
		'content_type': 'application/json'
	},
	'getVariantConsequencesBySpeciesId': {
		'url': '/vep/{{species}}/id/{{id}}',
		'method': 'GET',
		'content_type': 'application/json'
	},
	'getVariantConsequencesBySpeciesRegionAllele': {
		'url': '/vep/{{species}}/region/{{region}}/{{allele}}',
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
	503: ('Service Unavailable', 'The service is temporarily down; retry after a pause'),
}

# set user agent
ensembl_user_agent = {'User-Agent': 'pyEnsemblRest v' + __version__}
ensembl_content_type = {'Content-Type': 'application/json'}