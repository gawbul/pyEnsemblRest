pyEnsemblRest
=============

A Python wrapper around the EnsEMBL REST API

# Usage:

	from ensemblrest import EnsemblRest
	erest = EnsemblRest()
	print erest.getRestVersion()
	print erest.getSpeciesInfo()