"""
	Configuration information for the EnsEMBL REST API
"""

ensembl_default_url = 'http://beta.rest.ensembl.org'
ensembl_genomes_url = 'http://test.rest.ensemblgenomes.org'

ensembl_api_table = {
	# Comparative Genomics
	'getGeneTreeById': {
		'url': '/genetree/id/{{id}}',
		'method': 'GET',
	},
	'getGeneTreeByMemberId': {
		'url': '/genetree/member/id/{{id}}',
		'method': 'GET',
	},
	'getGeneTreeByMemberSymbol': {
		'url': '/genetree/member/symbol/{{species}}/{{symbol}}',
		'method': 'GET',
	},
	'getHomologyById': {
		'url': '/homology/id/{{id}}',
		'method': 'GET',
	},
	'getHomologyBySymbol': {
		'url': '/homology/symbol/{{species}}/{{symbol}}',
		'method': 'GET',
	},

	# Cross References
	'getXrefsById': {
		'url': '/xrefs/id/{{id}}',
		'method': 'GET',
	},
	'getXrefsByName': {
		'url': '/xrefs/name/{{species}}/{{name}}',
		'method': 'GET',
	},
	'getXrefsBySymbol': {
		'url': '/xrefs/symbol/{{species}}/{{symbol}}',
		'method': 'GET',
	},

	# Features
	'getFeatureById': {
		'url': '/feature/id/{{id}}',
		'method': 'GET',
	},
	'getFeatureByRegion': {
		'url': '/feature/region/{{species}}/{{region}}',
		'method': 'GET',
	},

	# Information
	'getAssemblyInfo': {
		'url': '/assembly/info/{{species}}',
		'method': 'GET',
	},
	'getAssemblyInfoRegion': {
		'url': '/assembly/info/{{species}}/{{region_name}}',
		'method': 'GET',
	},
	'getInfoComparas': {
		'url': '/info/comparas',
		'method': 'GET',
	},
	'getInfoData': {
		'url': '/info/data',
		'method': 'GET',
	},
	'getInfoPing': {
		'url': '/info/ping',
		'method': 'GET',
	},
	'getInfoRest': {
		'url': '/info/rest',
		'method': 'GET',
	},
	'getInfoSoftware': {
		'url': '/info/software',
		'method': 'GET',
	},
	'getInfoSpecies': {
		'url': '/info/species',
		'method': 'GET',
	},

	# Lookup
	'getLookupById': {
		'url': '/lookup/id/{{id}}',
		'method': 'GET',
	},

	# Mapping
	'getMapAssemblyOneToTwo': {
		'url': '/map/{{species}}/{{asm_one}}/{{region}}/{{asm_two}}',
		'method': 'GET',
	},
	'getMapCdnaToRegion': {
		'url': '/map/cdna/{{id}}/{{region}}',
		'method': 'GET',
	},
	'getMapCdsToRegion': {
		'url': '/map/cds/{{id}}/{{region}}',
		'method': 'GET',
	},
	'getMapTranslationToRegion': {
		'url': '/map/translation/{{id}}/{{region}}',
		'method': 'GET',
	},

	# Ontologies and Taxonomy
	'getAncestorsById': {
		'url': '/ontology/ancestors/{{id}}',
		'method': 'GET',
	},
	'getAncestorsChartById': {
		'url': '/ontology/ancestors/chart/{{id}}',
		'method': 'GET',
	},
	'getDescendentsById': {
		'url': '/ontology/descendents/{{id}}',
		'method': 'GET',
	},
	'getOntologyById': {
		'url': '/ontology/id/{{id}}',
		'method': 'GET',
	},
	'getOntologyByName': {
		'url': '/ontology/name/{{name}}',
		'method': 'GET',
	},
	'getTaxonomyClassificationById': {
		'url': '/taxonomy/classification/{{id}}',
		'method': 'GET',
	},
	'getTaxonomyById': {
		'url': '/taxonomy/id/{{id}}',
		'method': 'GET',
	},

	# Sequences
	'getSequenceById': {
		'url': '/sequence/id/{{id}}',
		'method': 'GET',
	},
	'getSequenceByRegion': {
		'url': '/sequence/region/{{species}}/{{region}}',
		'method': 'GET',
	},

	# Variation
	'getVariantConsequencesByRegion': {
		'url': '/vep/{{species}}/{{region}}/{{allele}}/consequences',
		'method': 'GET',
	},
	'getVariantConsequencesById': {
		'url': '/vep/{{species}}/id/{{id}}/consequences',
		'method': 'GET',
	},
}

ensembl_http_status_codes = {
	200: ('OK', 'Request was a success. Only process data from the service when you receive this code'),
	400: ('Bad Request', 'Occurs during exceptional circumstances such as the service is unable to find an ID. Check if the response Content-type was JSON. If so the JSON object is an exception hash with the message keyed under error'),
	404: ('Not Found', 'Indicates a badly formatted request. Check your URL'),
	429: ('Too Many Requests', 'You have been rate-limited; wait and retry. The headers X-RateLimit-Reset, X-RateLimit-Limit and X-RateLimit-Remaining will inform you of how long you have until your limit is reset and what that limit was. If you get this response and have not exceeded your limit then check if you have made too many requests per second.'),
	503: ('Service Unavailable', 'The service is temporarily down; retry after a pause'),
}