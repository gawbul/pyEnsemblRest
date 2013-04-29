from ensemblrest import EnsemblRest

erest = EnsemblRest()

print erest.getRestVersion()
print erest.getEnsemblVersion()
print erest.doPing()
print erest.getComparaReleases()
print erest.getDataReleases()
