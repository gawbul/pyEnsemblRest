"""
	EnsemblRest is a library for Python that wrap the EnsEMBL REST API.
	It simplifies all the API endpoints by abstracting them away from the
	end user and thus also ensures that an amendments to the library and/or
	EnsEMBL REST API won't cause major problems to the end user.

	Any questions, comments or issues can be addressed to gawbul@gmail.com.
"""

# import system modules
import re
import json
import types
import requests

# import ensemblrest modules
from . import __version__
from .ensembl_config import ensembl_default_url, ensembl_genomes_url, ensembl_api_table, ensembl_http_status_codes, ensembl_user_agent, ensembl_content_type
from .exceptions import EnsemblRestError, EnsemblRestRateLimitError, EnsemblRestServiceUnavailable

# EnsEMBL REST API object
class EnsemblRest(object):
	# class initialisation function
	def __init__(self, args=None):
		# read args variable into object as session_args
		self.session_args = args or {}
		
		# initialise default values
		default_base_url = ensembl_default_url
		default_headers = ensembl_user_agent
		default_content_type = ensembl_content_type
		default_proxies = {}
		
		# set default values if not client arguments
		if 'base_url' not in self.session_args:
			self.session_args['base_url'] = default_base_url
		if 'headers' not in self.session_args:
			self.session_args['headers'] = default_headers
		elif 'User-Agent' not in self.session_args['headers']:
			self.session_args['headers'].update(default_headers)
		elif 'Content-Type' not in self.session_args['headers']:
			self.session_args['headers'].update(default_content_type)
		if 'proxies' not in self.session_args:
			self.session_args['proxies'] = default_proxies
		
		# setup requests session
		self.session = requests.Session()
		
		# update requests client with arguments
		client_args_copy = self.session_args.copy()
		for key, val in client_args_copy.items():
			if key in ('base_url', 'proxies'):
				setattr(self.session, key, val)
				self.session_args.pop(key)
		
		# update headers as already exist within client
		self.session.headers.update(self.session_args.pop('headers'))

		# iterate over ensembl_api_table keys and add key to class namespace
		for fun_name in ensembl_api_table.keys():
			#setattr(self, key, self.register_api_func(key))
			#Not as a class attribute, but a class method
			self.__dict__[fun_name] = self.register_api_func(fun_name)
			
			#Set __doc__ for generic class method
			if ensembl_api_table[fun_name].has_key("doc"):
				self.__dict__[fun_name].__doc__ = ensembl_api_table[fun_name]["doc"]
			
			#add function name to the class methods
			self.__dict__[fun_name].__name__ = fun_name
			

	# dynamic api registration function
	def register_api_func(self, api_call):
		return lambda **kwargs: self.call_api_func(api_call, **kwargs)

	# dynamic api call function
	def call_api_func(self, api_call, **kwargs):
		# build url from ensembl_api_table kwargs
		func = ensembl_api_table[api_call]
		
		#TODO: check required parameters
		url = re.sub('\{\{(?P<m>[a-zA-Z_]+)\}\}', lambda m: "%s" % kwargs.get(m.group(1)), self.session.base_url + func['url'])
		
		#check the request type (GET or POST?)
		if func['method'] == 'GET':
			resp = self.session.get(url, headers={"Content-Type": func['content_type']})
			
		elif func['method'] == 'POST':
			#do the request
			resp = self.session.post(url, headers={"Content-Type": func['content_type']}, data=json.dumps(kwargs))
				
		else:
			raise NotImplementedError, "Method '%s' not yet implemented" %(func['method'])
		
		# parse status codes
		if resp.status_code > 304:
			ExceptionType = EnsemblRestError
			if resp.status_code == 429:
				ExceptionType = EnsemblRestRateLimitError

			raise ExceptionType(ensembl_http_status_codes[resp.status_code][1], error_code=resp.status_code)

		content = resp.text
		return content
