"""
	EnsemblRest is a library for Python that wrap the EnsEMBL REST API.
	It simplifies all the API endpoints by abstracting them away from the
	end user and thus also ensures that an amendments to the library and/or
	EnsEMBL REST API won't cause major problems to the end user.

	Any questions, comments or issues can be addressed to gawbul@gmail.com.
"""

__author__ = "Steve Moss"
__copyright__ = "Copyright 2013-2014, Steve Moss"
__credits__ = ["Steve Moss"]
__license__ = "GNU GPLv3"
__version__ = "0.2.1"
__maintainer__ = "Steve Moss"
__email__ = "gawbul@gmail.com"
__status__ = "beta"

from .ensemblrest import EnsemblRest, EnsemblGenomeRest
from .exceptions import EnsemblRestError, EnsemblRestRateLimitError, EnsemblRestServiceUnavailable
