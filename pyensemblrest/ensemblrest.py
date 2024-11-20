import json
import logging
import re
import time
from typing import Any

import requests
from requests import Response
from requests.structures import CaseInsensitiveDict

# import ensemblrest modules
from .ensembl_config import (
    ensembl_api_table,
    ensembl_content_type,
    ensembl_default_url,
    ensembl_header,
    ensembl_http_status_codes,
    ensembl_known_errors,
    ensembl_user_agent,
)
from .exceptions import (
    EnsemblRestError,
    EnsemblRestRateLimitError,
    EnsemblRestServiceUnavailable,
)

# Logger instance
logger = logging.getLogger(__name__)


# FakeResponse object
class FakeResponse(object):
    def __init__(self, response: Response | Any, text: str = ""):
        self.headers: CaseInsensitiveDict[str] | dict[str, Any] = response.headers
        self.status_code: int = 400
        self.text: str = text


# EnsEMBL REST API object
class EnsemblRest(object):
    # class initialisation function
    def __init__(
        self, api_table: dict[str, Any] = ensembl_api_table, **kwargs: dict[str, Any]
    ) -> None:
        # read args variable into object as session_args
        self.session_args: dict[str, Any] = kwargs or {}

        # In order to rate limit the requests, like https://github.com/Ensembl/ensembl-rest/wiki/Example-Python-Client
        self.reqs_per_sec: int = 15
        self.req_count: int = 0
        self.last_req: float = 0
        self.wall_time: int = 1

        # get rate limit parameters, if provided
        self.rate_reset: int | None = None
        self.rate_limit: int | None = None
        self.rate_remaining: int | None = None
        self.rate_period: int | None = None
        self.retry_after: float | None = None

        # to record the last parameters used (in order to redo the query with an ensembl known error)
        self.last_url: str = ""
        self.last_headers: CaseInsensitiveDict[str] | dict[str, Any] = {}
        self.last_params: dict[str, Any] = {}
        self.last_data: dict[Any, Any] = {}
        self.last_method: str = ""
        self.last_attempt: int = 0
        self.last_response: Response | FakeResponse

        # the maximum number of attempts
        self.max_attempts: int = 5

        # setting a timeout
        self.timeout: int = 60

        # set default values if those values are not provided
        self.__set_default()

        # setup requests session
        self.session = requests.Session()

        # update headers
        self.__update_headers()

        # add class methods relying api_table
        self.__add_methods(api_table)

    def __set_default(self) -> None:
        """Set default values"""

        # initialise default values
        default_base_url = ensembl_default_url
        default_headers = ensembl_header
        default_content_type = ensembl_content_type
        default_proxies: dict[str, str] = {}

        if "base_url" not in self.session_args:
            self.session_args["base_url"] = default_base_url

        if "headers" not in self.session_args:
            self.session_args["headers"] = default_headers

        if "User-Agent" not in self.session_args["headers"]:
            self.session_args["headers"].update(default_headers)

        if "Content-Type" not in self.session_args["headers"]:
            self.session_args["headers"]["Content-Type"] = default_content_type

        if "proxies" not in self.session_args:
            self.session_args["proxies"] = default_proxies

    def __update_headers(self) -> None:
        """Update headers"""

        # update requests client with arguments
        client_args_copy = self.session_args.copy()
        for key, val in client_args_copy.items():
            if key in ("base_url", "proxies"):
                setattr(self.session, key, val)
                self.session_args.pop(key)

        # update headers as already exist within client
        self.session.headers.update(self.session_args.pop("headers"))

    def __add_methods(self, api_table: dict[str, Any]) -> None:
        """Add methods to class object"""

        # iterate over api_table keys and add key to class namespace
        for fun_name in api_table.keys():
            # setattr(self, key, self.register_api_func(key))
            # Not as a class attribute, but a class method
            self.__dict__[fun_name] = self.register_api_func(fun_name, api_table)

            # Set __doc__ for generic class method
            if "doc" in api_table[fun_name]:
                self.__dict__[fun_name].__doc__ = api_table[fun_name]["doc"]

            # add function name to the class methods
            self.__dict__[fun_name].__name__ = fun_name

    # dynamic api registration function
    def register_api_func(self, api_call: str, api_table: dict[str, Any]) -> Any:
        return lambda **kwargs: self.call_api_func(api_call, api_table, **kwargs)

    @staticmethod
    def __check_params(func: Any, kwargs: Any) -> list[Any]:
        """Check for mandatory parameters"""

        # Verify required variables and raise an Exception if needed
        mandatory_params = re.findall(r"\{\{(?P<m>[a-zA-Z1-9_]+)\}\}", func["url"])

        for param in mandatory_params:
            if param not in kwargs:
                logger.critical(
                    "'%s' param not specified. Mandatory params are %s"
                    % (param, mandatory_params)
                )
                raise Exception("mandatory param '%s' not specified" % param)
            else:
                logger.debug("Mandatory param %s found" % param)

        return mandatory_params

    # dynamic api call function
    def call_api_func(
        self, api_call: str, api_table: dict[str, Any], **kwargs: dict[str, Any]
    ) -> Any:
        # build url from api_table kwargs
        func = api_table[api_call]

        # check mandatory params
        mandatory_params = self.__check_params(func, kwargs)

        # resolving urls
        url = re.sub(
            r"\{\{(?P<m>[a-zA-Z1-9_]+)\}\}",
            lambda m: "%s" % kwargs.get(m.group(1)),
            self.session.base_url + func["url"],  # type: ignore[attr-defined]
        )

        # debug
        logger.debug("Resolved url: '%s'" % url)

        # Now I have to remove mandatory params from kwargs
        for param in mandatory_params:
            del kwargs[param]

        # Initialize with the ensembl default content type
        content_type: str | dict[str, Any] = ensembl_content_type

        # Override content type if it is defined by function
        if "content_type" in func:
            content_type = func["content_type"]

        # Ovveride content type if it is provied when calling function
        if "content_type" in kwargs:
            content_type = kwargs["content_type"]
            del kwargs["content_type"]

        # check the request type (GET or POST?)
        if func["method"] == "GET":
            logger.debug(
                "Submitting a GET request: url = '%s', headers = %s, params = %s"
                % (url, {"Content-Type": content_type}, kwargs)
            )

            # record this request
            self.last_url = url
            self.last_headers = {"Content-Type": content_type}
            self.last_params = kwargs
            self.last_data = {}
            self.last_method = "GET"
            self.last_attempt = 0

            resp = self.__get_response()

        elif func["method"] == "POST":
            # in a POST request, separate post parameters from other parameters
            data = {}

            # pass key=value in POST data from kwargs
            for key in func["post_parameters"]:
                if key in kwargs:
                    data[key] = kwargs[key]
                    del kwargs[key]

            logger.debug(
                "Submitting a POST request: url = '%s', headers = %s, params = %s, data = %s"
                % (url, {"Content-Type": content_type}, kwargs, data)
            )

            # record this request
            self.last_url = url
            self.last_headers = {"Content-Type": content_type}
            self.last_params = kwargs
            self.last_data = data
            self.last_method = "POST"
            self.last_attempt = 0

            resp = self.__get_response()

        else:
            raise NotImplementedError(
                "Method '%s' not yet implemented" % (func["method"])
            )

        # call response and return content
        return self.parseResponse(resp, content_type)

    # A function to get reponse from ensembl REST api
    def __get_response(self) -> Response | FakeResponse:
        """Call session get and post method. Return response"""

        # updating last_req time
        self.last_req = time.time()

        # Increment the request counter to rate limit requests
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
        resp: Response | FakeResponse

        # deal with exceptions
        try:
            # another request using the correct method
            if self.last_method == "GET":
                resp = self.session.get(
                    self.last_url,
                    headers=self.last_headers,
                    params=self.last_params,
                    timeout=self.timeout,
                )
            elif self.last_method == "POST":
                # post parameters are load as POST data, other parameters are url parameters as GET requests
                resp = self.session.post(
                    self.last_url,
                    headers=self.last_headers,
                    data=json.dumps(self.last_data),
                    params=self.last_params,
                    timeout=self.timeout,
                )
            # other methods are verifiedby others functions

        except requests.ConnectionError as e:
            raise EnsemblRestServiceUnavailable(e)

        except requests.Timeout as e:
            logger.error("%s request timeout: %s" % (self.last_method, e))

            # create a fake response in order to redo the query
            resp = FakeResponse(
                self.last_response,
                json.dumps(
                    {"message": repr(e), "error": "%s timeout" % ensembl_user_agent}
                ),
            )

        # return response
        return resp

    # A function to deal with a generic response
    def parseResponse(
        self,
        resp: Response | FakeResponse,
        content_type: str | dict[str, Any] = "application/json",
    ) -> Any:
        """Deal with a generic REST response"""

        logger.debug("Got %s" % resp.text)

        # Record response for debug intent
        self.last_response = resp

        # Initialize some values. Check if I'm rate limited
        (
            self.rate_reset,
            self.rate_limit,
            self.rate_remaining,
            self.retry_after,
            self.rate_period,
        ) = self.__get_rate_limit(resp.headers)

        # parse status code
        if self.__check_retry(resp):
            return self.__retry_request()

        # Handle content in different way relying on content-type
        if content_type == "application/json":
            content = json.loads(resp.text)

        else:
            # Default
            content = resp.text

        return content

    def __check_retry(self, resp: Response | FakeResponse) -> bool:
        """Parse status code and print warnings. Return True if a retry is needed"""

        # default status code
        message = ensembl_http_status_codes[resp.status_code][1]

        # parse status codes
        if resp.status_code > 304:
            ExceptionType = EnsemblRestError

            # Try to derive a more useful message than ensembl default message
            if resp.status_code == 400:
                json_message = json.loads(resp.text)
                if "error" in json_message:
                    message = json_message["error"]

                # TODO: deal with special cases errors
                if message in ensembl_known_errors:
                    # call a function that will re-execute the REST request and then call again parseResponse
                    # if everithing is ok, a processed content is returned
                    logger.warning("EnsEMBL REST Service returned: %s" % message)

                    # return true if retry needed
                    return True
            elif resp.status_code == 500:
                # Retrying when we get a 500 error.
                # Due to Ensembl's condition on randomly returning 500s on valid requests.
                return True
            elif resp.status_code == 429:
                ExceptionType = EnsemblRestRateLimitError

            raise ExceptionType(
                message,
                error_code=resp.status_code,
                rate_reset=self.rate_reset,
                rate_limit=self.rate_limit,
                rate_remaining=self.rate_remaining,
                retry_after=self.retry_after,
            )

        # return a flag if status is ok
        return False

    @staticmethod
    def __get_rate_limit(
        headers: CaseInsensitiveDict[str] | dict[str, Any],
    ) -> tuple[int | None, int | None, int | None, float | None, None]:
        """Read rate limited attributes"""

        # initialize some values
        retry_after = None
        rate_reset = None
        rate_limit = None
        rate_remaining = None
        rate_period = None

        # for semplicity
        keys = [key.lower() for key in headers.keys()]

        if "X-RateLimit-Reset".lower() in keys:
            rate_reset = int(headers["X-RateLimit-Reset"])
            logger.debug("X-RateLimit-Reset: %s" % rate_reset)

        if "X-RateLimit-Period".lower() in keys:
            rate_reset = int(headers["X-RateLimit-Period"])
            logger.debug("X-RateLimit-Period: %s" % rate_period)

        if "X-RateLimit-Limit".lower() in keys:
            rate_limit = int(headers["X-RateLimit-Limit"])
            logger.debug("X-RateLimit-Limit: %s" % rate_limit)

        if "X-RateLimit-Remaining".lower() in keys:
            rate_remaining = int(headers["X-RateLimit-Remaining"])
            logger.debug("X-RateLimit-Remaining: %s" % rate_remaining)

        if "Retry-After".lower() in keys:
            retry_after = float(headers["Retry-After"])
            logger.debug("Retry-After: %s" % retry_after)

        return rate_reset, rate_limit, rate_remaining, retry_after, rate_period

    def __retry_request(self) -> Any:
        """Retry last request in case of failure"""

        # update last attempt
        self.last_attempt += 1

        # a max of three attempts
        if self.last_attempt > self.max_attempts:
            # default status code
            message = ensembl_http_status_codes[self.last_response.status_code][1]

            # parse error if possible
            try:
                json_message = json.loads(self.last_response.text)
                if "error" in json_message:
                    message = json_message["error"]
            except ValueError:
                # In this case we didn't even get a JSON back.
                message = "Server returned invalid JSON."

            raise EnsemblRestError(
                "Max number of retries attempts reached. Last message was: %s"
                % message,
                error_code=self.last_response.status_code,
                rate_reset=self.rate_reset,
                rate_limit=self.rate_limit,
                rate_remaining=self.rate_remaining,
                retry_after=self.retry_after,
            )

        # sleep a while. Increment on each attempt
        to_sleep = (self.wall_time + 1) * self.last_attempt

        logger.debug("Sleeping %s" % to_sleep)
        time.sleep(to_sleep)

        # another request using the correct method
        if self.last_method == "GET":
            # debug
            logger.debug(
                "Retring last GET request (%s/%s): url = '%s', headers = %s, params = %s"
                % (
                    self.last_attempt,
                    self.max_attempts,
                    self.last_url,
                    self.last_headers,
                    self.last_params,
                )
            )

            resp = self.__get_response()

        elif self.last_method == "POST":
            # debug
            logger.debug(
                "Retring last POST request (%s/%s): url = '%s', headers = %s, params = %s, data = %s"
                % (
                    self.last_attempt,
                    self.max_attempts,
                    self.last_url,
                    self.last_headers,
                    self.last_params,
                    self.last_data,
                )
            )

            resp = self.__get_response()
        else:
            raise NotImplementedError(
                "Method '%s' not yet implemented" % (self.last_method)
            )

        # call response and return content
        return self.parseResponse(resp, self.last_headers["Content-Type"])
