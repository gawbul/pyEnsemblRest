import importlib.metadata

__author__ = "Steve Moss"
__copyright__ = "Copyright (C) 2013-2024, Steve Moss"
__credits__ = ["Steve Moss"]
__license__ = "GNU GPLv3"
__version__: str = importlib.metadata.version("pyensemblrest")
__maintainer__ = "Steve Moss"
__email__ = "gawbul@gmail.com"
__status__ = "beta"

__all__ = [
    "EnsemblRest",
    "EnsemblRestError",
    "EnsemblRestRateLimitError",
    "EnsemblRestServiceUnavailable",
]

from .ensemblrest import EnsemblRest
from .exceptions import (
    EnsemblRestError,
    EnsemblRestRateLimitError,
    EnsemblRestServiceUnavailable,
)
