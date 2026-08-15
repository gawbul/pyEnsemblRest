import importlib.metadata

__author__ = "Steve Moss"
__copyright__ = "Copyright (C) 2013-2024, Steve Moss"
__credits__ = ["Steve Moss"]
__license__ = "GNU GPLv3"
try:
    __version__: str = importlib.metadata.version("pyensemblrest")
except importlib.metadata.PackageNotFoundError:
    __version__ = "0.0.0"
__maintainer__ = "Steve Moss"
__email__ = "gawbul@gmail.com"
__status__ = "beta"

from .ensemblrest import EnsemblRest
from .exceptions import (
    EnsemblRestBadRequestError,
    EnsemblRestError,
    EnsemblRestNotFoundError,
    EnsemblRestRateLimitError,
    EnsemblRestServiceUnavailable,
    EnsemblRestTimeoutError,
)

__all__ = [
    "EnsemblRest",
    "EnsemblRestBadRequestError",
    "EnsemblRestError",
    "EnsemblRestNotFoundError",
    "EnsemblRestRateLimitError",
    "EnsemblRestServiceUnavailable",
    "EnsemblRestTimeoutError",
]
