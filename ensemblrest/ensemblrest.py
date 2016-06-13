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

    EnsemblRest is a library for Python that wrap the EnsEMBL REST API.
    It simplifies all the API endpoints by abstracting them away from the
    end user and thus also ensures that an amendments to the library and/or
    EnsEMBL REST API won't cause major problems to the end user.

    Any questions, comments or issues can be addressed to gawbul@gmail.com.
    
"""

# import system modules
import re
import json
import time
import logging
import requests

# import ensemblrest modules
from . import __version__
from .ensembl_config import ensembl_default_url, ensembl_genomes_url, ensembl_api_table, ensemblgenomes_api_table, ensembl_http_status_codes, ensembl_header, ensembl_content_type
from .exceptions import EnsemblRestError, EnsemblRestRateLimitError, EnsemblRestServiceUnavailable

# Logger instance
logger = logging.getLogger(__name__)

# EnsEMBL REST API object
class EnsemblRest(object):
    # class initialisation function
    def __init__(self, api_table=ensembl_api_table, **kwargs):
        # read args variable into object as session_args
        self.session_args = kwargs or {}
        
        #In order to rate limiting the requests, like https://github.com/Ensembl/ensembl-rest/wiki/Example-Python-Client
        self.reqs_per_sec = 15
        self.req_count = 0
        self.last_req = 0
        
        # initialise default values
        default_base_url = ensembl_default_url
        default_headers = ensembl_header
        default_content_type = ensembl_content_type
        default_proxies = {}
        
        # set default values if those values are not provided
        if 'base_url' not in self.session_args:
            self.session_args['base_url'] = default_base_url
            
        if 'headers' not in self.session_args:
            self.session_args['headers'] = default_headers
        
        if 'User-Agent' not in self.session_args['headers']:
            self.session_args['headers'].update(default_headers)
                            
        if 'Content-Type' not in self.session_args['headers']:
            self.session_args['headers']['Content-Type'] = default_content_type
            
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

        # iterate over api_table keys and add key to class namespace
        for fun_name in api_table.keys():
            #setattr(self, key, self.register_api_func(key))
            #Not as a class attribute, but a class method
            self.__dict__[fun_name] = self.register_api_func(fun_name, api_table)
            
            #Set __doc__ for generic class method
            if api_table[fun_name].has_key("doc"):
                self.__dict__[fun_name].__doc__ = api_table[fun_name]["doc"]
            
            #add function name to the class methods
            self.__dict__[fun_name].__name__ = fun_name
            

    # dynamic api registration function
    def register_api_func(self, api_call, api_table):
        return lambda **kwargs: self.call_api_func(api_call, api_table, **kwargs)

    # dynamic api call function
    def call_api_func(self, api_call, api_table, **kwargs):
        # build url from api_table kwargs
        func = api_table[api_call]
        
        #Verify required variables and raise an Exception if needed
        mandatory_params = re.findall('\{\{(?P<m>[a-zA-Z1-9_]+)\}\}', func['url'])
        
        for param in mandatory_params:
            if not kwargs.has_key(param):
                logger.critical("'%s' param not specified. Mandatory params are %s" %(param, mandatory_params))
                raise Exception, "mandatory param '%s' not specified" %(param)
            else:
                logger.debug("Mandatory param %s found" %(param))
        
        url = re.sub('\{\{(?P<m>[a-zA-Z1-9_]+)\}\}', lambda m: "%s" % kwargs.get(m.group(1)), self.session.base_url + func['url'])
        
        # debug
        logger.debug("Resolved url: '%s'" %(url))
        
        # Now I have to remove mandatory params from kwargs        
        for param in mandatory_params:
            del(kwargs[param])
            
        # Initialize with the ensembl default content type
        content_type = ensembl_content_type
        
        # Override content type if it is defined by function
        if func.has_key("content_type"):
            content_type = func["content_type"]
        
        # Ovveride content type if it is provied when calling function
        if kwargs.has_key("content_type"):
            content_type = kwargs["content_type"]
            del(kwargs["content_type"])
        
        #Evaluating the numer of request in a second (according to EnsEMBL rest specification)
        if self.req_count >= self.reqs_per_sec:
            delta = time.time() - self.last_req
            if delta < 1:
                logger.debug("waiting %s" %(delta))
                time.sleep(1 - delta)
            self.req_count = 0
        
        #check the request type (GET or POST?)
        if func['method'] == 'GET':
            logger.debug("Submitting a GET request. url = '%s', headers = %s, params = %s" %(url, {"Content-Type": content_type}, kwargs))
            resp = self.session.get(url, headers={"Content-Type": content_type}, params=kwargs)
            
        elif func['method'] == 'POST':
            # in a POST request, separate post parameters from other parameters
            data = {}
            
            # pass key=value in POST data from kwargs
            for key in func['post_parameters']:
                if kwargs.has_key(key):
                    data[key] = kwargs[key]
                    del(kwargs[key])
                
            logger.debug("Submitting a POST request. url = '%s', headers = %s, params = %s, data = %s" %(url, {"Content-Type": content_type}, kwargs, data))
            # post parameters are load as POST data, other parameters are url parameters as GET requests
            resp = self.session.post(url, headers={"Content-Type": content_type}, data=json.dumps(data), params=kwargs)
                
        else:
            raise NotImplementedError, "Method '%s' not yet implemented" %(func['method'])
            
        #call response and return content
        return self.parseResponse(resp, content_type)
            
    # A function to deal with a generic response
    def parseResponse(self, resp, content_type="application/json"):
        """Deal with a generic REST response"""
        
        # updating last_req time
        self.last_req = time.time()
        
        #Increment the request counter to rate limit requests    
        self.req_count += 1
        
        #record response for debug intent
        self.last_response = resp
        
        # initialize some values. Check if I'm rate limited
        rate_reset, rate_limit, rate_remaining, retry_after = self.__get_rate_limit(resp.headers)
        
        # default status code
        message = ensembl_http_status_codes[resp.status_code][1]
        
        # parse status codes
        if resp.status_code > 304:
            ExceptionType = EnsemblRestError
            
            #Try to derive a more useful message than ensembl default message
            if resp.status_code == 400:
                json_message = json.loads(resp.text)
                if json_message.has_key("error"):
                    message = json_message["error"]
            
            if resp.status_code == 429:
                ExceptionType = EnsemblRestRateLimitError

            raise ExceptionType(message, error_code=resp.status_code, rate_reset=rate_reset, rate_limit=rate_limit, rate_remaining=rate_remaining, retry_after=retry_after)

        #handle content in different way relying on content-type
        if content_type == 'application/json':
            content = json.loads(resp.text)
        
        else:
            #default 
            content = resp.text
            
        return content
        
    def __get_rate_limit(self, headers):
        """Read rate limited attributes"""
        
        # initialize some values
        retry_after = None
        rate_reset = None
        rate_limit = None
        rate_remaining = None
        
        # for semplicity
        keys = [key.lower() for key in headers.keys()]
        
        if "X-RateLimit-Reset".lower() in keys:
            rate_reset = int(headers["X-RateLimit-Reset"])
            logger.debug("X-RateLimit-Reset: %s" %(rate_reset))
            
        if "X-RateLimit-Limit".lower() in keys:
            rate_limit = int(headers["X-RateLimit-Limit"])
            logger.debug("X-RateLimit-Limit: %s" %(rate_limit))
            
        if "X-RateLimit-Remaining".lower() in keys:
            rate_remaining = int(headers["X-RateLimit-Remaining"])
            logger.debug("X-RateLimit-Remaining: %s" %(rate_remaining))
            
        if "Retry-After".lower() in keys:
            retry_after = float(headers["Retry-After"])
            logger.debug("Retry-After: %s" %(retry_after))
            
        return rate_reset, rate_limit, rate_remaining, retry_after

# EnsEMBL Genome REST API object
class EnsemblGenomeRest(EnsemblRest):
    # class initialisation function
    def __init__(self, api_table=ensemblgenomes_api_table, base_url=ensembl_genomes_url, **kwargs):
        #override default base_url
        kwargs["base_url"] = base_url
        
        #Call the Base Class init method
        EnsemblRest.__init__(self, api_table=api_table, **kwargs)
    
    
#module end

