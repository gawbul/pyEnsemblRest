from ensembl_config import ensembl_http_status_codes

"""
	Implements custom exceptions for the EnsEMBL REST API
"""

class EnsemblRestError(Exception):
	"""
		Generic error class, catch-all for most EnsemblRest issues.
		Special cases are handled by EnsemblRestRateLimitError and EnsemblRestServiceUnavailable.
	"""
	def __init__(self, msg, error_code=None, rate_reset=None, rate_limit=None, rate_remaining=None):
		self.error_code = error_code

		if error_code is not None and error_code in ensembl_http_status_codes:
			msg = 'EnsEMBL REST API returned a %s (%s), %s' % \
            		(error_code, ensembl_http_status_codes[error_code][0], msg)

		super(EnsemblRestError, self).__init__(msg)

	@property
	def msg(self):
		return self.args[0]

class EnsemblRestRateLimitError(EnsemblRestError):
	"""
		Raised when you've hit a rate limit.
		The amount of seconds to retry your request in will be appended to the message.
	"""
	def __init__(self, msg, error_code, rate_reset=None, rate_limit=None, rate_remaining=None):
		if isinstance(rate_limit, int):
			msg = '%s (Rate limit hit:  %d seconds)' % (msg, rate_reset, rate_limit, rate_remaining)
		EnsemblRestError.__init__(self, msg, error_code=error_code)

class EnsemblRestServiceUnavailable(EnsemblRestError):
	"""
		Raised when the service is down.
	"""	
	pass