import collections
import json
import logging
import re
import time
import urllib.parse
from typing import Any

import requests
from requests import Response
from requests.structures import CaseInsensitiveDict

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
    EnsemblRestBadRequestError,
    EnsemblRestError,
    EnsemblRestNotFoundError,
    EnsemblRestRateLimitError,
    EnsemblRestServiceUnavailable,
    EnsemblRestTimeoutError,
)

logger = logging.getLogger(__name__)

PARAM_REGEX = re.compile(r"\{\{(?P<m>[a-zA-Z0-9_]+)\}\}")


class FakeResponse:
    """Mock Response object for timeout/error simulations."""

    def __init__(
        self,
        headers: CaseInsensitiveDict[str] | dict[str, Any],
        status_code: int,
        text: str,
    ) -> None:
        self.headers = headers
        self.status_code = status_code
        self.text: str = text


class EnsemblRest:
    """
    EnsEMBL REST API Client.

    Provides a dynamic Pythonic interface to all Ensembl REST endpoints.
    Handles rate limiting (15 req/s), automatic retries on transient errors,
    and multiple response formats.
    """

    def __init__(
        self, api_table: dict[str, Any] = ensembl_api_table, **kwargs: Any
    ) -> None:
        self.api_table = api_table
        self.session_args: dict[str, Any] = kwargs.copy()

        # Rate limiting configuration (15 requests/second sliding window)
        self.reqs_per_sec: int = int(self.session_args.pop("reqs_per_sec", 15))
        self.wall_time: float = float(self.session_args.pop("wall_time", 1.0))
        self._request_timestamps: collections.deque[float] = collections.deque()
        self.req_count: int = 0
        self.last_req: float = 0.0

        # Rate limit metadata from response headers
        self.rate_reset: int | None = None
        self.rate_limit: int | None = None
        self.rate_remaining: int | None = None
        self.rate_period: int | None = None
        self.retry_after: float | None = None

        # Tracking state for retrying requests
        self.last_url: str = ""
        self.last_headers: CaseInsensitiveDict[str] | dict[str, Any] = {}
        self.last_params: dict[str, Any] = {}
        self.last_data: Any = {}
        self.last_method: str = ""
        self.last_attempt: int = 0
        self.last_response: Response | FakeResponse = Response()

        # Request tuning
        self.max_attempts: int = int(self.session_args.pop("max_attempts", 5))
        self.timeout: int | float = self.session_args.pop("timeout", 60)

        # Base URL & Proxies
        self.base_url: str = self.session_args.pop("base_url", ensembl_default_url)
        proxies: dict[str, str] = self.session_args.pop("proxies", {})

        # Setup requests session
        self.session = requests.Session()
        setattr(self.session, "base_url", self.base_url)
        self.session.proxies.update(proxies)

        # Update headers
        self._setup_headers()

        # Register dynamic API methods
        self.__add_methods(self.api_table)

    def _setup_headers(self) -> None:
        """Initialize session headers with default User-Agent and Content-Type."""
        headers: dict[str, str] = self.session_args.pop("headers", {})
        merged_headers = ensembl_header.copy()
        merged_headers["Content-Type"] = ensembl_content_type
        if headers:
            merged_headers.update(headers)
        self.session.headers.update(merged_headers)

    def __add_methods(self, api_table: dict[str, Any]) -> None:
        """Add dynamic API endpoint methods to instance dictionary."""
        for fun_name in api_table:
            func = self.register_api_func(fun_name, api_table)
            if "doc" in api_table[fun_name]:
                func.__doc__ = api_table[fun_name]["doc"]
            func.__name__ = fun_name
            self.__dict__[fun_name] = func

    def __dir__(self) -> list[str]:
        """Expose dynamic API methods for dir() and autocompletion tools."""
        return sorted(set(super().__dir__()) | set(self.api_table.keys()))

    def __getattr__(self, name: str) -> Any:
        """Fallback to resolve API methods if not already bound."""
        if name in self.api_table:
            func = self.register_api_func(name, self.api_table)
            if "doc" in self.api_table[name]:
                func.__doc__ = self.api_table[name]["doc"]
            func.__name__ = name
            self.__dict__[name] = func
            return func
        raise AttributeError(
            f"'{self.__class__.__name__}' object has no attribute '{name}'"
        )

    def register_api_func(self, api_call: str, api_table: dict[str, Any]) -> Any:
        """Create a callable lambda for an API endpoint."""
        return lambda **kwargs: self.call_api_func(api_call, api_table, **kwargs)

    @staticmethod
    def __check_params(func: dict[str, Any], kwargs: dict[str, Any]) -> list[str]:
        """Check that all mandatory template parameters are provided."""
        mandatory_params = PARAM_REGEX.findall(func["url"])
        for param in mandatory_params:
            if param not in kwargs:
                logger.critical(
                    f"'{param}' param not specified. Mandatory params are {mandatory_params}"
                )
                raise ValueError(f"mandatory param '{param}' not specified")
            logger.debug(f"Mandatory param {param} found")
        return mandatory_params

    def _resolve_url(self, template: str, kwargs: dict[str, Any]) -> str:
        """Interpolate path parameters into endpoint URL with proper quoting."""

        def _replace(match: re.Match[str]) -> str:
            key = match.group("m")
            val = kwargs.get(key)
            return urllib.parse.quote(str(val), safe=":")

        resolved_path = PARAM_REGEX.sub(_replace, template)
        base = self.base_url.rstrip("/")
        path = resolved_path.lstrip("/")
        return f"{base}/{path}"

    def call_api_func(
        self, api_call: str, api_table: dict[str, Any], **kwargs: Any
    ) -> Any:
        """Execute dynamic API call, handling parameter resolution, HTTP method, and parsing."""
        func = api_table[api_call]
        call_kwargs = kwargs.copy()

        # Check and validate mandatory params
        mandatory_params = self.__check_params(func, call_kwargs)

        # Build resolved URL
        url = self._resolve_url(func["url"], call_kwargs)
        logger.debug(f"Resolved url: '{url}'")

        # Remove mandatory path parameters from query/body kwargs
        for param in mandatory_params:
            call_kwargs.pop(param, None)

        # Determine content type
        content_type: str = func.get("content_type", ensembl_content_type)
        if "content_type" in call_kwargs:
            content_type = call_kwargs.pop("content_type")

        # Handle GET or POST
        if func["method"] == "GET":
            logger.debug(
                f"Submitting a GET request: url = '{url}', headers = {{'Content-Type': '{content_type}'}}, params = {call_kwargs}"
            )
            self.last_url = url
            self.last_headers = {"Content-Type": content_type}
            self.last_params = call_kwargs
            self.last_data = {}
            self.last_method = "GET"
            self.last_attempt = 0

            resp = self.__get_response()

        elif func["method"] == "POST":
            data: dict[str, Any] = {}
            for key in func.get("post_parameters", []):
                if key in call_kwargs:
                    data[key] = call_kwargs.pop(key)

            logger.debug(
                f"Submitting a POST request: url = '{url}', headers = {{'Content-Type': '{content_type}'}}, params = {call_kwargs}, data = {data}"
            )
            self.last_url = url
            self.last_headers = {"Content-Type": content_type}
            self.last_params = call_kwargs
            self.last_data = data
            self.last_method = "POST"
            self.last_attempt = 0

            resp = self.__get_response()

        else:
            raise NotImplementedError(f"Method '{func['method']}' not yet implemented")

        return self.parseResponse(resp, content_type)

    def _wait_for_rate_limit(self) -> None:
        """Enforce rate limiting using a sliding window deque."""
        now = time.time()
        # Purge timestamps outside the sliding window
        while (
            self._request_timestamps
            and (now - self._request_timestamps[0]) >= self.wall_time
        ):
            self._request_timestamps.popleft()

        # If window limit is reached, sleep until the oldest request expires
        if len(self._request_timestamps) >= self.reqs_per_sec:
            oldest = self._request_timestamps[0]
            to_sleep = self.wall_time - (now - oldest)
            if to_sleep > 0:
                logger.debug(
                    f"Rate limit reached ({self.reqs_per_sec} req/s). Waiting {to_sleep:.4f}s"
                )
                time.sleep(to_sleep)
            now = time.time()
            while (
                self._request_timestamps
                and (now - self._request_timestamps[0]) >= self.wall_time
            ):
                self._request_timestamps.popleft()

        self._request_timestamps.append(now)
        self.last_req = now
        self.req_count = len(self._request_timestamps)

    def __get_response(self) -> Response | FakeResponse:
        """Perform HTTP request with rate limiting and network exception handling."""
        self._wait_for_rate_limit()

        resp: Response | FakeResponse
        try:
            if self.last_method == "GET":
                resp = self.session.get(
                    self.last_url,
                    headers=self.last_headers,
                    params=self.last_params,
                    timeout=self.timeout,
                )
            elif self.last_method == "POST":
                resp = self.session.post(
                    self.last_url,
                    headers=self.last_headers,
                    data=json.dumps(self.last_data),
                    params=self.last_params,
                    timeout=self.timeout,
                )
            else:
                raise NotImplementedError(
                    f"Method '{self.last_method}' not yet implemented"
                )

        except requests.ConnectionError as e:
            raise EnsemblRestServiceUnavailable(e) from e

        except requests.Timeout as e:
            logger.error(f"{self.last_method} request timeout: {e}")
            resp = FakeResponse(
                headers=getattr(self.last_response, "headers", {}),
                status_code=408,
                text=json.dumps(
                    {"message": repr(e), "error": f"{ensembl_user_agent} timeout"}
                ),
            )

        return resp

    def parseResponse(
        self,
        resp: Response | FakeResponse,
        content_type: str | dict[str, Any] = "application/json",
    ) -> Any:
        """Process API response, extract rate limits, handle retries, and parse content."""
        logger.debug(f"Got {resp.text}")
        self.last_response = resp

        # Extract rate limit headers
        (
            self.rate_reset,
            self.rate_limit,
            self.rate_remaining,
            self.retry_after,
            self.rate_period,
        ) = self.__get_rate_limit(resp.headers)

        # Check for errors and retries
        if self.__check_retry(resp):
            return self.__retry_request()

        # Parse response content
        if content_type == "application/json":
            try:
                content = json.loads(resp.text)
            except (ValueError, json.JSONDecodeError):
                content = resp.text
        else:
            content = resp.text

        return content

    def __check_retry(self, resp: Response | FakeResponse) -> bool:
        """Evaluate status codes for retrying or raising appropriate exceptions."""
        status_info = ensembl_http_status_codes.get(
            resp.status_code, ("Error", "Unknown HTTP error")
        )
        message = status_info[1]

        if resp.status_code > 304:
            exception_type = EnsemblRestError

            # Parse JSON error payload if available
            try:
                json_message = json.loads(resp.text)
                if isinstance(json_message, dict) and "error" in json_message:
                    message = json_message["error"]
            except (ValueError, json.JSONDecodeError):
                pass

            if resp.status_code == 400:
                if message in ensembl_known_errors:
                    logger.warning(f"EnsEMBL REST Service returned: {message}")
                    return True
                exception_type = EnsemblRestBadRequestError

            elif resp.status_code == 404:
                exception_type = EnsemblRestNotFoundError

            elif resp.status_code == 408:
                if message in ensembl_known_errors or "timeout" in message:
                    return True
                exception_type = EnsemblRestTimeoutError

            elif resp.status_code == 429:
                exception_type = EnsemblRestRateLimitError

            elif resp.status_code == 500:
                # Retry transient Ensembl 500 errors
                return True

            elif resp.status_code == 503:
                exception_type = EnsemblRestServiceUnavailable

            raise exception_type(
                message,
                error_code=resp.status_code,
                rate_reset=self.rate_reset,
                rate_limit=self.rate_limit,
                rate_remaining=self.rate_remaining,
                retry_after=self.retry_after,
            )

        return False

    @staticmethod
    def __get_rate_limit(
        headers: CaseInsensitiveDict[str] | dict[str, Any],
    ) -> tuple[int | None, int | None, int | None, float | None, int | None]:
        """Parse rate limit headers safely."""
        retry_after: float | None = None
        rate_reset: int | None = None
        rate_limit: int | None = None
        rate_remaining: int | None = None
        rate_period: int | None = None

        if not headers:
            return rate_reset, rate_limit, rate_remaining, retry_after, rate_period

        lower_headers = {k.lower(): v for k, v in headers.items()}

        if "x-ratelimit-reset" in lower_headers:
            try:
                rate_reset = int(lower_headers["x-ratelimit-reset"])
                logger.debug(f"X-RateLimit-Reset: {rate_reset}")
            except (ValueError, TypeError):
                pass

        if "x-ratelimit-period" in lower_headers:
            try:
                rate_period = int(lower_headers["x-ratelimit-period"])
                logger.debug(f"X-RateLimit-Period: {rate_period}")
            except (ValueError, TypeError):
                pass

        if "x-ratelimit-limit" in lower_headers:
            try:
                rate_limit = int(lower_headers["x-ratelimit-limit"])
                logger.debug(f"X-RateLimit-Limit: {rate_limit}")
            except (ValueError, TypeError):
                pass

        if "x-ratelimit-remaining" in lower_headers:
            try:
                rate_remaining = int(lower_headers["x-ratelimit-remaining"])
                logger.debug(f"X-RateLimit-Remaining: {rate_remaining}")
            except (ValueError, TypeError):
                pass

        if "retry-after" in lower_headers:
            try:
                retry_after = float(lower_headers["retry-after"])
                logger.debug(f"Retry-After: {retry_after}")
            except (ValueError, TypeError):
                pass

        return rate_reset, rate_limit, rate_remaining, retry_after, rate_period

    def __retry_request(self) -> Any:
        """Retry the last request using exponential backoff."""
        self.last_attempt += 1

        if self.last_attempt > self.max_attempts:
            status_code = getattr(self.last_response, "status_code", 500)
            status_info = ensembl_http_status_codes.get(
                status_code, ("Error", "Unknown HTTP error")
            )
            message = status_info[1]

            try:
                json_message = json.loads(self.last_response.text)
                if isinstance(json_message, dict) and "error" in json_message:
                    message = json_message["error"]
            except (ValueError, json.JSONDecodeError, AttributeError):
                message = "Server returned invalid JSON."

            raise EnsemblRestError(
                f"Max number of retries attempts reached. Last message was: {message}",
                error_code=status_code,
                rate_reset=self.rate_reset,
                rate_limit=self.rate_limit,
                rate_remaining=self.rate_remaining,
                retry_after=self.retry_after,
            )

        to_sleep = (self.wall_time + 1) * self.last_attempt
        logger.debug(
            f"Sleeping {to_sleep}s before retry {self.last_attempt}/{self.max_attempts}"
        )
        time.sleep(to_sleep)

        if self.last_method == "GET":
            logger.debug(
                f"Retrying last GET request ({self.last_attempt}/{self.max_attempts}): url = '{self.last_url}'"
            )
            resp = self.__get_response()
        elif self.last_method == "POST":
            logger.debug(
                f"Retrying last POST request ({self.last_attempt}/{self.max_attempts}): url = '{self.last_url}'"
            )
            resp = self.__get_response()
        else:
            raise NotImplementedError(
                f"Method '{self.last_method}' not yet implemented"
            )

        content_type = self.last_headers.get("Content-Type", ensembl_content_type)
        return self.parseResponse(resp, content_type)

    def close(self) -> None:
        """Close the underlying HTTP session connection pools."""
        self.session.close()

    def __enter__(self) -> "EnsemblRest":
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        self.close()

    def get_user_agent(self) -> str:
        """Return the pyEnsemblRest user agent string."""
        return ensembl_user_agent
