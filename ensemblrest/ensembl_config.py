"""
	Configuration information for the EnsEMBL REST API
"""

ensembl_default_url = 'http://beta.rest.ensembl.org'
ensembl_genomes_url = 'http://test.rest.ensemblgenomes.org'

ensembl_api_table = {
	# Assembly
	'getAssemblyInfo': {
		'url': '/assembly/info/{{species}}',
		'method': 'GET',
	},
	'getAssemblyInfoRegion': {
		'url': '/assembly/info/{{species}}/{{region_name}}',
		'method': 'GET',
	},

	# Information
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

}

ensembl_http_status_codes = {
	200: ('OK', 'Request was a success. Only process data from the service when you receive this code'),
	400: ('Bad Request', 'Occurs during exceptional circumstances such as the service is unable to find an ID. Check if the response Content-type was JSON. If so the JSON object is an exception hash with the message keyed under error'),
	404: ('Not Found', 'Indicates a badly formatted request. Check your URL'),
	429: ('Too Many Requests', 'You have been rate-limited; wait and retry. The headers X-RateLimit-Reset, X-RateLimit-Limit and X-RateLimit-Remaining will inform you of how long you have until your limit is reset and what that limit was. If you get this response and have not exceeded your limit then check if you have made too many requests per second.'),
	503: ('Service Unavailable', 'The service is temporarily down; retry after a pause'),
}