"""
	Configuration information for the EnsEMBL REST API
"""
base_url = 'http://beta.rest.ensembl.org'
genomes_url = 'http://test.rest.ensemblgenomes.org'

api_table = {
	# Information
	'getRestVersion': {
		'url': '/info/rest?',
		'method': 'GET',
	},
	'getSpeciesInfo': {
		'url': '/info/species',
		'method': 'GET',
	},

}

http_status_codes = {
	200: ('OK', 'Success!'),
}