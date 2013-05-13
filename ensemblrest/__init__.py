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
__version__ = "0.1.7b"

from .ensemblrest import EnsemblRest
from .exceptions import EnsemblRestError, EnsemblRestRateLimitError, EnsemblRestServiceUnavailable