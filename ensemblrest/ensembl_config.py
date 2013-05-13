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
		'content_type': 'text/x-nh'
	},
	'getGeneTreeByMemberId': {
		'url': '/genetree/member/id/{{id}}?content-type=text/x-nh',
		'method': 'GET',
		'content_type': 'text/x-phyloxml+xml'
	},
	'getGeneTreeByMemberSymbol': {
		'url': '/genetree/member/symbol/{{species}}/{{symbol}}?content-type=text/x-nh',
		'method': 'GET',
		'content_type': 'text/x-phyloxml+xml'
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

	# Features
	'getFeatureById': {
		'url': '/feature/id/{{id}}?feature={{feature}}',
		'method': 'GET',
		'content_type': 'application/json'
	},
	'getFeatureByRegion': {
		'url': '/feature/region/{{species}}/{{region}}?feature={{feature}}',
		'method': 'GET',
		'content_type': 'application/json'
	},

	# Information
	'getAssemblyInfo': {
		'url': '/assembly/info/{{species}}',
		'method': 'GET',
		'content_type': 'application/json'
	},
	'getAssemblyInfoRegion': {
		'url': '/assembly/info/{{species}}/{{region_name}}',
		'method': 'GET',
		'content_type': 'application/json'
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
	'getVariantConsequencesByRegion': {
		'url': '/vep/{{species}}/{{region}}/{{allele}}/consequences',
		'method': 'GET',
		'content_type': 'application/json'
	},
	'getVariantConsequencesById': {
		'url': '/vep/{{species}}/id/{{id}}/consequences',
		'method': 'GET',
		'content_type': 'application/json'
	},
}

ensembl_http_status_codes = {
	200: ('OK', 'Request was a success. Only process data from the service when you receive this code'),
	400: ('Bad Request', 'Occurs during exceptional circumstances such as the service is unable to find an ID. Check if the response Content-type was JSON. If so the JSON object is an exception hash with the message keyed under error'),
	404: ('Not Found', 'Indicates a badly formatted request. Check your URL'),
	415: ('Unsupported Media Type', 'The server is refusing to service the request because the entity of the request is in a format not supported by the requested resource for the requested method'),
	429: ('Too Many Requests', 'You have been rate-limited; wait and retry. The headers X-RateLimit-Reset, X-RateLimit-Limit and X-RateLimit-Remaining will inform you of how long you have until your limit is reset and what that limit was. If you get this response and have not exceeded your limit then check if you have made too many requests per second.'),
	503: ('Service Unavailable', 'The service is temporarily down; retry after a pause'),
}