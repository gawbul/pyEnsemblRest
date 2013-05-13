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
sleep(1) # sleep for a second so we don't get rate-limited
print ensemblrest.getXrefsByName(species='human', name='BRCA2')
print ensemblrest.getXrefsBySymbol(species='human', symbol='BRCA2')

# Features
print ensemblrest.getFeatureById(id='ENSG00000157764')
sleep(1) # sleep for a second so we don't get rate-limited
print ensemblrest.getFeatureByRegion(species='human', region='7:140424943..140624564')

# Information
print ensemblrest.getAssemblyInfo(species='human')
print ensemblrest.getAssemblyInfoRegion(species='human', region_name='X')
sleep(1) # sleep for a second so we don't get rate-limited
print ensemblrest.getInfoComparas()
print ensemblrest.getInfoData()
print ensemblrest.getInfoPing()
sleep(1) # sleep for a second so we don't get rate-limited
print ensemblrest.getInfoRest()
print ensemblrest.getInfoSoftware()
print ensemblrest.getInfoSpecies()
sleep(1) # sleep for a second so we don't get rate-limited

# Lookup
print ensemblrest.getLookupyId(id='ENSG00000157764')

# Mapping
print ensemblrest.getMapAssemblyOneToTwo(asm_one='NCBI36', region='X:1000000..1000100:1', asm_two='GRCh37')
print ensemblrest.getMapCdnaToRegion(id='ENST00000288602', region='100..300')
sleep(1) # sleep for a second so we don't get rate-limited
print ensemblrest.getMapCdsToRegion(id='ENST00000288602', region='1..1000')
print ensemblrest.getMapTranslationToRegion(id='ENSP00000288602', region='100..300')

# Ontologies and Taxonomy
print ensemblrest.getAncestorsById(id='GO:0005667')
sleep(1) # sleep for a second so we don't get rate-limited
print ensemblrest.getAncestorsChartById(id='GO:0005667')
print ensemblrest.getDescendentsById(id='GO:0005667')
print ensemblrest.getOntologyById(id='')
sleep(1) # sleep for a second so we don't get rate-limited
print ensemblrest.getOntologyByName(name='transcription factor complex')
print ensemblrest.getTaxonomyClassificationById(id='9606')
print ensemblrest.getTaxonomyById(id='9606')

sleep(1) # sleep for a second so we don't get rate-limited
# Sequences
print ensemblrest.getSequenceById(id='ENSG00000157764')
print ensemblrest.getSequenceByRegion(species='human', region='X:1000000..1000100')

# Variation
print ensemblrest.getVariantConsequencesByRegion(species='human', region='9:22125503-22125502:1', allele='C')
sleep(1) # sleep for a second so we don't get rate-limited
print ensemblrest.getVariantConsequencesById(species='human', id='COSM476')
