from ensemblrest import EnsemblRest

erest = EnsemblRest()

# Assembly
print erest.getAssemblyInfo(species='homo_sapiens')
print erest.getAssemblyInfoRegion(species='homo_sapiens', region_name=1)

# Info
print erest.getInfoComparas()
print erest.getInfoData()
print erest.getInfoPing()
print erest.getInfoRest()
print erest.getInfoSoftware()
print erest.getInfoSpecies()
