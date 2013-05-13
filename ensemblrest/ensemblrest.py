"""
	EnsemblRest is a library for Python that wrap the EnsEMBL REST API.
	It simplifies all the API endpoints by abstracting them away from the
	end user and thus also ensures that an amendments to the library and/or
	EnsEMBL REST API won't cause major problems to the end user.

	Thanks to Ryan McGrath's <ryan@venodesigns.net> Twython API for
	assisting with designing this code <https://github.com/ryanmcgrath/twython>.

	Any questions, comments or issues can be addressed to gawbul@gmail.com.
"""

__author__ = "Steve Moss"
__copyright__ = "Copyright 2013, Steve Moss"
__credits__ = ["Steve Moss"]
__license__ = "GPL"
__version__ = "0.1.1b"
__maintainer__ = "Steve Moss"
__email__ = "gawbul@gmail.com"
__status__ = "beta"

import re
import sys
import requests
import json

from .ensembl_config import ensembl_default_url, ensembl_genomes_url, ensembl_api_table
from .exceptions import EnsemblRestError, EnsemblRestRateLimitError, EnsemblRestServiceUnavailable

class EnsemblRest(object):
	""" The REST API object """
	def __init__(self, server=None, proxies=None):
		# set REST API server url
		if not server == None:
			if server == "default":
				self.base_url = ensembl_default_url
			elif server == "genomes":
				self.base_url = ensembl_genomes_url
			else:
				self.base_url = server
		else:
			self.base_url = ensembl_default_url

		# setup requests session
		self.client = requests.Session()
		self.client.headers = {'User-Agent': 'pyEnsemblRest v' + __version__}
		self.client.proxies = proxies

        # register available functions to allow listing name when debugging
		def regFunc(key):
			return lambda **kwargs: self._constructFunc(key, **kwargs)

		# iterate over ensembl_api_table keys and add key to class namespace
		for key in ensembl_api_table.keys():
			self.__dict__[key] = regFunc(key)

	def _constructFunc(self, api_call, **kwargs):
		""" Function constructor """
		# Go through and replace any moustaches that are in the API url.
		fn = ensembl_api_table[api_call]
		url = re.sub('\{\{(?P<m>[a-zA-Z_]+)\}\}',
						lambda m: "%s" % kwargs.get(m.group(1)), self.base_url + fn['url'])
		content = self._request(url, method=fn['method'], content_type=fn['content_type'], params=kwargs)

		return content

	def _request(self, url, method='GET', content_type='application/json', params=None, files=None, api_call=None):
		""" Internal response generator, no sense in repeating the same code twice, right? ;) """
		method = method.lower()
		if not method in ('get', 'post'):
			raise Exception('Method must be either GET or POST')

		# set content type
		if not content_type:
			raise Exception('Content-Type must be provided')
		self.client.headers['Content-Type'] = content_type

		params = params or {}
		# convert params.items to unicode to be nice to requests
		for k, v in params.items():
			if isinstance(v, (int, bool)):
				params[k] = u'%s' % v

		func = getattr(self.client, method)
		if method == 'get':
			response = func(url, params=params)
		else:
			response = func(url, data=params, files=files)
		content = response.content.decode('utf-8')

		# store last call to api for debugging purposes
		self._last_call = {
			'api_call': api_call,
			'api_error': None,
			'cookies': response.cookies,
			'headers': response.headers,
			'status_code': response.status_code,
			'url': response.url,
			'content': content,
		}
		
		# wrap the json loads in a try, and defer an error
        # why? EnsEMBL REST API will return invalid json with an error code in the headers
		json_error = False
		if content_type == 'application/json':
			try:
				try:
					# try to get json
					content = content.json()
				except AttributeError:
					# if unicode detected
					content = json.loads(content)
			except ValueError:
				json_error = True
				content = {}
		
		if response.status_code > 304:
			# If there is no error message, use a default.
			error_message = content.get('error', 'An error occurred processing your request.')
			self._last_call['api_error'] = error_message

			ExceptionType = EnsemblRestError
			if response.status_code == 429:
				# EnsEMBL REST API always returns 429 when rate limit is exceeded
				ExceptionType = EnsemblRestRateLimitError

			raise ExceptionType(error_message,
								error_code=response.status_code,
								rate_reset=response.headers.get('X-RateLimit-Reset'),
								rate_limit=response.headers.get('X-RateLimit-Limit'),
								rate_remaining=response.headers.get('X-RateLimit-Remaining')
								)

		# if we have a json error here, then it's not an official EnsEMBL REST API error
		if json_error and not response.status_code in (200, 201, 202):
			raise EnsemblRestError('Response was not valid JSON, unable to decode.')

		return content