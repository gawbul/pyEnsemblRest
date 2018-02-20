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
from collections import namedtuple

# import ensemblrest modules
from .ensembl_config import ensembl_default_url, ensembl_genomes_url, ensembl_api_table, ensemblgenomes_api_table,\
    ensembl_http_status_codes, ensembl_header, ensembl_content_type, ensembl_known_errors, ensembl_user_agent
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
        self.wall_time = 1
        
        # get rate limit parameters, if provided
        self.rate_reset = None
        self.rate_limit = None
        self.rate_remaining = None
        self.retry_after = None
        
        # to record the last parameters used (in order to redo the query with an ensembl known error)
        self.last_url = None
        self.last_headers = {}
        self.last_params = {}
        self.last_data = {}
        self.last_method = None
        self.last_attempt = 0
        self.last_response = None
        
        # the maximum number of attempts
        self.max_attempts = 5
        
        # setting a timeout
        self.timeout = 60
        
        # set default values if those values are not provided
        self.__set_default()
        
        # setup requests session
        self.session = requests.Session()
        
        # update headers
        self.__update_headers()

        # add class methods relying api_table
        self.__add_methods(api_table)
            
    def __set_default(self):
        """Set default values"""
        
        # initialise default values
        default_base_url = ensembl_default_url
        default_headers = ensembl_header
        default_content_type = ensembl_content_type
        default_proxies = {}
        
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
    
    def __update_headers(self):
        """Update headers"""
        
        # update requests client with arguments
        client_args_copy = self.session_args.copy()
        for key, val in client_args_copy.items():
            if key in ('base_url', 'proxies'):
                setattr(self.session, key, val)
                self.session_args.pop(key)
        
        # update headers as already exist within client
        self.session.headers.update(self.session_args.pop('headers'))
        
    def __add_methods(self, api_table):
        """Add methods to class object"""
        
        # iterate over api_table keys and add key to class namespace
        for fun_name in api_table.keys():
            #setattr(self, key, self.register_api_func(key))
            #Not as a class attribute, but a class method
            self.__dict__[fun_name] = self.register_api_func(fun_name, api_table)
            
            #Set __doc__ for generic class method
            if "doc" in api_table[fun_name]:
                self.__dict__[fun_name].__doc__ = api_table[fun_name]["doc"]
            
            #add function name to the class methods
            self.__dict__[fun_name].__name__ = fun_name
        
    # dynamic api registration function
    def register_api_func(self, api_call, api_table):
        return lambda **kwargs: self.call_api_func(api_call, api_table, **kwargs)

    @staticmethod
    def __check_params(func, kwargs):
        """Check for mandatory parameters"""
        
        #Verify required variables and raise an Exception if needed
        mandatory_params = re.findall('\{\{(?P<m>[a-zA-Z1-9_]+)\}\}', func['url'])
        
        for param in mandatory_params:
            if param not in kwargs:
                logger.critical("'%s' param not specified. Mandatory params are %s" % (param, mandatory_params))
                raise Exception("mandatory param '%s' not specified" % param)
            else:
                logger.debug("Mandatory param %s found" % param)
                
        return mandatory_params

    # dynamic api call function
    def call_api_func(self, api_call, api_table, **kwargs):
        # build url from api_table kwargs
        func = api_table[api_call]
        
        # check mandatory params
        mandatory_params = self.__check_params(func, kwargs)
        
        # resolving urls
        url = re.sub('\{\{(?P<m>[a-zA-Z1-9_]+)\}\}', lambda m: "%s" % kwargs.get(m.group(1)),
                     self.session.base_url + func['url'])
        
        # debug
        logger.debug("Resolved url: '%s'" % url)
        
        # Now I have to remove mandatory params from kwargs        
        for param in mandatory_params:
            del(kwargs[param])
            
        # Initialize with the ensembl default content type
        content_type = ensembl_content_type
        
        # Override content type if it is defined by function
        if "content_type" in func:
            content_type = func["content_type"]
        
        # Ovveride content type if it is provied when calling function
        if "content_type" in kwargs:
            content_type = kwargs["content_type"]
            del(kwargs["content_type"])
        
        #check the request type (GET or POST?)
        if func['method'] == 'GET':
            logger.debug("Submitting a GET request: url = '%s', headers = %s, params = %s"
                         % (url, {"Content-Type": content_type}, kwargs))
            
            # record this request
            self.last_url = url
            self.last_headers = {"Content-Type": content_type}
            self.last_params = kwargs
            self.last_data = {}
            self.last_method = "GET"
            self.last_attempt = 0
        
            resp = self.__get_response()
            
        elif func['method'] == 'POST':
            # in a POST request, separate post parameters from other parameters
            data = {}
            
            # pass key=value in POST data from kwargs
            for key in func['post_parameters']:
                if key in kwargs:
                    data[key] = kwargs[key]
                    del(kwargs[key])
                
            logger.debug("Submitting a POST request: url = '%s', headers = %s, params = %s, data = %s"
                         % (url, {"Content-Type": content_type}, kwargs, data))
            
            # record this request
            self.last_url = url
            self.last_headers = {"Content-Type": content_type}
            self.last_params = kwargs
            self.last_data = data
            self.last_method = "POST"
            self.last_attempt = 0
            
            resp = self.__get_response()
                
        else:
            raise NotImplementedError("Method '%s' not yet implemented" % (func['method']))
            
        #call response and return content
        return self.parseResponse(resp, content_type)
        
    # A function to get reponse from ensembl REST api
    def __get_response(self):
        """Call session get and post method. Return response"""
        
        # updating last_req time
        self.last_req = time.time()
        
        #Increment the request counter to rate limit requests    
        self.req_count += 1
        
        # Evaluating the numer of request in a second (according to EnsEMBL rest specification)
        if self.req_count >= self.reqs_per_sec:
            delta = time.time() - self.last_req

            # sleep upto wall_time
            if delta < self.wall_time:
                to_sleep = self.wall_time - delta
                logger.debug("waiting %s" % to_sleep)
                time.sleep(to_sleep)
                
            self.req_count = 0
        
        # my response
        resp = None
        
        # deal with exceptions
        try:
            # another request using the correct method
            if self.last_method == "GET":
                resp = self.session.get(
                    self.last_url,
                    headers=self.last_headers,
                    params=self.last_params,
                    timeout=self.timeout
                )
            elif self.last_method == "POST":
                # post parameters are load as POST data, other parameters are url parameters as GET requests
                resp = self.session.post(
                    self.last_url,
                    headers=self.last_headers,
                    data=json.dumps(self.last_data),
                    params=self.last_params,
                    timeout=self.timeout
                )
            # other methods are verifiedby others functions
                    
        except requests.ConnectionError as e:
            raise EnsemblRestServiceUnavailable(e)
                    
        except requests.Timeout as e:
            logger.error("%s request timeout: %s" % (self.last_method, e))
            
            # create a fake response in order to redo the query
            resp = namedtuple("fakeResponse", ["headers", "status_code", "text"])
            
            # add some data
            resp.headers = {}
            resp.status_code = 400
            resp.text = json.dumps({'message': repr(e), 'error': "%s timeout" % ensembl_user_agent})
        
        # return response
        return resp

    # A function to deal with a generic response
    def parseResponse(self, resp, content_type="application/json"):
        """Deal with a generic REST response"""
        
        logger.debug("Got %s" % resp.text)
        
        #record response for debug intent
        self.last_response = resp
        
        # initialize some values. Check if I'm rate limited
        self.rate_reset, self.rate_limit, self.rate_remaining, self.retry_after = self.__get_rate_limit(resp.headers)
        
        # parse status code
        if self.__check_retry(resp):
            return self.__retry_request()

        #handle content in different way relying on content-type
        if content_type == 'application/json':
            content = json.loads(resp.text)
        
        else:
            #default 
            content = resp.text
            
        return content
    
    def __check_retry(self, resp):
        """Parse status code and print warnings. Return True if a retry is needed"""
        
        # default status code
        message = ensembl_http_status_codes[resp.status_code][1]
        
        # parse status codes
        if resp.status_code > 304:
            ExceptionType = EnsemblRestError
            
            #Try to derive a more useful message than ensembl default message
            if resp.status_code == 400:
                json_message = json.loads(resp.text)
                if "error" in json_message:
                    message = json_message["error"]
                    
                #TODO: deal with special cases errors
                if message in ensembl_known_errors:
                    # call a function that will re-execute the REST request and then call again parseResponse
                    # if everithing is ok, a processed content is returned
                    logger.warning("EnsEMBL REST Service returned: %s" % message)
                    
                    # return true if retry needed
                    return True
            
            if resp.status_code == 429:
                ExceptionType = EnsemblRestRateLimitError

            raise ExceptionType(
                message,
                error_code=resp.status_code,
                rate_reset=self.rate_reset,
                rate_limit=self.rate_limit,
                rate_remaining=self.rate_remaining,
                retry_after=self.retry_after
            )
        
        # return a flag if status is ok
        return False

    @staticmethod
    def __get_rate_limit(headers):
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
            logger.debug("X-RateLimit-Reset: %s" % rate_reset)
            
        if "X-RateLimit-Limit".lower() in keys:
            rate_limit = int(headers["X-RateLimit-Limit"])
            logger.debug("X-RateLimit-Limit: %s" % rate_limit)
            
        if "X-RateLimit-Remaining".lower() in keys:
            rate_remaining = int(headers["X-RateLimit-Remaining"])
            logger.debug("X-RateLimit-Remaining: %s" % rate_remaining)
            
        if "Retry-After".lower() in keys:
            retry_after = float(headers["Retry-After"])
            logger.debug("Retry-After: %s" % retry_after)
            
        return rate_reset, rate_limit, rate_remaining, retry_after
        
    def __retry_request(self):
        """Retry last request in case of failure"""
        
        # update last attempt
        self.last_attempt += 1
        
        # a max of three attempts
        if self.last_attempt > self.max_attempts:
            # default status code
            message = ensembl_http_status_codes[self.last_response.status_code][1]
            
            # parse error if possible
            json_message = json.loads(self.last_response.text)
            if "error" in json_message:
                message = json_message["error"]
        
            raise EnsemblRestError("Max number of retries attempts reached. Last message was: %s"
                                   % message,
                                   error_code=self.last_response.status_code,
                                   rate_reset=self.rate_reset,
                                   rate_limit=self.rate_limit,
                                   rate_remaining=self.rate_remaining,
                                   retry_after=self.retry_after
                                   )
            
        # sleep a while. Increment on each attempt
        to_sleep = (self.wall_time + 1) * self.last_attempt
        
        logger.debug("Sleeping %s" % to_sleep)
        time.sleep(to_sleep)
    
        # another request using the correct method
        if self.last_method == "GET":
            #debug
            logger.debug("Retring last GET request (%s/%s): url = '%s', headers = %s, params = %s"
                         % (self.last_attempt, self.max_attempts, self.last_url, self.last_headers, self.last_params))
            
            resp = self.__get_response()
                
        elif self.last_method == "POST":
            #debug
            logger.debug("Retring last POST request (%s/%s): url = '%s', headers = %s, params = %s, data = %s" % (
                self.last_attempt,
                self.max_attempts,
                self.last_url,
                self.last_headers,
                self.last_params,
                self.last_data
            ))
            
            resp = self.__get_response()
        else:
            resp = None
        
        #call response and return content
        return self.parseResponse(resp, self.last_headers["Content-Type"])


class EnsemblGenomeRest(EnsemblRest):
    """EnsEMBL Genome REST API object"""

    def __init__(self, api_table=ensemblgenomes_api_table, base_url=ensembl_genomes_url, **kwargs):
        # Override default base_url
        kwargs["base_url"] = base_url
        
        # Call the Base Class init method
        EnsemblRest.__init__(self, api_table=api_table, **kwargs)
