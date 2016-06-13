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

__author__ = "Steve Moss"
__copyright__ = "Copyright (C) 2013-2016, Steve Moss"
__credits__ = ["Steve Moss"]
__license__ = "GNU GPLv3"
__version__ = "0.2.3"
__maintainer__ = "Steve Moss"
__email__ = "gawbul@gmail.com"
__status__ = "beta"

from .ensemblrest import EnsemblRest, EnsemblGenomeRest
from .exceptions import EnsemblRestError, EnsemblRestRateLimitError, EnsemblRestServiceUnavailable
