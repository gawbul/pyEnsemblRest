from typing import Any

from requests.exceptions import ConnectionError

from .ensembl_config import ensembl_http_status_codes


class EnsemblRestError(Exception):
    """
    Generic error class, catch-all for most EnsemblRest issues.
    Special cases are handled by subclasses like EnsemblRestRateLimitError and EnsemblRestServiceUnavailable.
    """

    def __init__(
        self,
        msg: str | ConnectionError,
        error_code: int | None = None,
        rate_reset: int | None = None,
        rate_limit: int | None = None,
        rate_remaining: int | None = None,
        retry_after: float | int | None = None,
    ) -> None:
        self.error_code = error_code
        self.rate_reset = rate_reset
        self.rate_limit = rate_limit
        self.rate_remaining = rate_remaining
        self.retry_after = float(retry_after) if retry_after is not None else None

        if error_code is not None and error_code in ensembl_http_status_codes:
            status_name = ensembl_http_status_codes[error_code][0]
            msg = f"EnsEMBL REST API returned a {error_code} ({status_name}): {msg}"

        super().__init__(msg)

    @property
    def msg(self) -> Any:
        return self.args[0]


class EnsemblRestRateLimitError(EnsemblRestError):
    """
    Raised when you've hit a rate limit.
    The amount of seconds to retry your request in will be appended to the message.
    """

    def __init__(
        self,
        msg: str | ConnectionError,
        error_code: int | None = None,
        rate_reset: int | None = None,
        rate_limit: int | None = None,
        rate_remaining: int | None = None,
        retry_after: float | int | None = None,
    ) -> None:
        if isinstance(retry_after, (int, float)):
            msg = f"{msg} (Rate limit hit:  Retry after {int(retry_after)} seconds)"

        super().__init__(
            msg,
            error_code=error_code,
            rate_reset=rate_reset,
            rate_limit=rate_limit,
            rate_remaining=rate_remaining,
            retry_after=retry_after,
        )


class EnsemblRestServiceUnavailable(EnsemblRestError):
    """
    Raised when the service is down or unreachable.
    """

    pass


class EnsemblRestTimeoutError(EnsemblRestError):
    """
    Raised when a request times out after all retry attempts.
    """

    pass


class EnsemblRestNotFoundError(EnsemblRestError):
    """
    Raised when a resource or URL is not found (HTTP 404).
    """

    pass


class EnsemblRestBadRequestError(EnsemblRestError):
    """
    Raised when a bad request is submitted (HTTP 400).
    """

    pass
