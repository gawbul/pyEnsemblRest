from typing import Any

from requests.exceptions import ConnectionError

from .ensembl_config import ensembl_http_status_codes


class EnsemblRestError(Exception):
    """
    Generic error class, catch-all for most EnsemblRest issues.
    Special cases are handled by EnsemblRestRateLimitError and EnsemblRestServiceUnavailable.
    """

    def __init__(
        self,
        msg: str | ConnectionError,
        error_code: int | None = None,
        rate_reset: int | None = None,
        rate_limit: int | None = None,
        rate_remaining: int | None = None,
        retry_after: float | None = None,
    ) -> None:
        self.error_code = error_code

        if error_code is not None and error_code in ensembl_http_status_codes:
            msg = "EnsEMBL REST API returned a %s (%s): %s" % (
                error_code,
                ensembl_http_status_codes[error_code][0],
                msg,
            )

        super(EnsemblRestError, self).__init__(msg)

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
        retry_after: float | None = None,
    ) -> None:
        if isinstance(retry_after, float):
            msg = "%s (Rate limit hit:  Retry after %d seconds)" % (msg, retry_after)

        EnsemblRestError.__init__(self, msg, error_code=error_code)


class EnsemblRestServiceUnavailable(EnsemblRestError):
    """
    Raised when the service is down.
    """

    pass
