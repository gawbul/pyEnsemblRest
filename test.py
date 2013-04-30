"""
	This script allows testing of all pyEnsemblRest functionality.
"""

# import required modules
from ensemblrest import EnsemblRest
from time import sleep
import unittests

# setup new EnsemblRest object
ensemblrest = EnsemblRest()

# Comparative Genomics
print ensemblrest.getGeneTreeById(id='ENSGT00390000003602')
print ensemblrest.getGeneTreeByMemberId(id='ENSG00000157764')
print ensemblrest.getGeneTreeByMemberSymbol(species='human', symbol='BRCA2')

sleep(1) # sleep for a second so we don't get rate-limited

print ensemblrest.getHomologyById(id='ENSG00000157764')
print ensemblrest.getHomologyBySymbol(species='human', symbol='BRCA2')

# Cross References
print ensemblrest.getXrefsById(id='ENSG00000157764')
sleep(1)
print ensemblrest.getXrefsByName(species='human', name='BRCA2')
print ensemblrest.getXrefsBySymbol(species='human', symbol='BRCA2')

# Features
print ensemblrest.getFeatureById(id='ENSG00000157764')
sleep(1)
print ensemblrest.getFeatureByRegion(species='human', region='7:140424943-140624564')

# Information
print ensemblrest.getAssemblyInfo(species='human')
print ensemblrest.getAssemblyInfoRegion(species='human', region_name='X')

print ensemblrest.getInfoComparas()
print ensemblrest.getInfoData()
print ensemblrest.getInfoPing()
print ensemblrest.getInfoRest()
print ensemblrest.getInfoSoftware()
print ensemblrest.getInfoSpecies()


print ensemblrest.getLookupyId(id='ENSG00000157764')

print ensemblrest.getSequenceById(id='ENSG00000157764')
print ensemblrest.getSequenceByRegion(species='human', region='X:1000000..1000100')