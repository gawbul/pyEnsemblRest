"""

    This file is part of pyEnsemblRest.

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


	This script allows testing of all pyEnsemblRest functionality.
"""

# import required modules
from ensemblrest import EnsemblRest, EnsemblGenomeRest
from time import sleep

# setup new EnsemblRest object
ensRest = EnsemblRest()

# setup a new EnsemblGenomeRest on ensemblgenome
ensGenomeRest = EnsemblGenomeRest()

# Archive endpoints
print ensRest.getArchiveById(id="ENSG00000157764")
print ensRest.getArchiveByMultipleIds(id=["ENSG00000157764", "ENSG00000248378"])

# Comparative Genomics
print ensGenomeRest.getGeneFamilyById(id="MF_01687", compara="bacteria")
print ensGenomeRest.getGeneFamilyMemberById(id="b0344", compara="bacteria")
print ensGenomeRest.getGeneFamilyMemberBySymbol(symbol="lacZ", species="escherichia_coli_str_k_12_substr_mg1655", compara="bacteria")


print ensRest.getGeneTreeById(id='ENSGT00390000003602')
print ensRest.getGeneTreeMemberById(id='ENSG00000157764')
print ensRest.getGeneTreeMemberBySymbol(species='human', symbol='BRCA2')

#TODO: remove this sleep is not necessary. EnsEMBL limit policy is implemented in EnsemblRest.call_api_func
sleep(1) # sleep for a second so we don't get rate-limited

print ensRest.getAlignmentByRegion(species="taeniopygia_guttata", region="2:106040000-106040050:1", species_set_group="sauropsids")
print ensRest.getHomologyById(id='ENSG00000157764')
print ensRest.getHomologyBySymbol(species='human', symbol='BRCA2')

# Cross References
print ensRest.getXrefsById(id='ENSG00000157764')
sleep(1) # sleep for a second so we don't get rate-limited
print ensRest.getXrefsByName(species='human', name='BRCA2')
print ensRest.getXrefsBySymbol(species='human', symbol='BRCA2')

# Features endpoints were removed

# Information
print ensRest.getInfoAnalysis(species="homo_sapiens")
print ensRest.getInfoAssembly(species="homo_sapiens", bands=1) #bands is an optional parameter
print ensRest.getInfoAssemblyRegion(species="homo_sapiens", region_name="X")
sleep(1)
print ensRest.getInfoBiotypes(species="homo_sapiens")
print ensRest.getInfoComparaMethods()
print ensRest.getInfoComparaSpeciesSets(methods="EPO")
sleep(1)
print ensRest.getInfoComparas()
print ensRest.getInfoData()
print ensGenomeRest.getInfoEgVersion()
sleep(1)
print ensRest.getInfoExternalDbs(species="homo_sapiens")
print ensGenomeRest.getInfoDivisions()
print ensGenomeRest.getInfoGenomesByName(name="campylobacter_jejuni_subsp_jejuni_bh_01_0142")
sleep(1)

#This response is very heavy
#print ensGenomeRest.getInfoGenomes()

print ensGenomeRest.getInfoGenomesByAccession(division="U00096")
print ensGenomeRest.getInfoGenomesByAssembly(division="GCA_000005845")
sleep(1)
print ensGenomeRest.getInfoGenomesByDivision(division="EnsemblPlants")
print ensGenomeRest.getInfoGenomesByTaxonomy(division="Arabidopsis")
print ensRest.getInfoPing()
sleep(1)
print ensRest.getInfoRest()
print ensRest.getInfoSoftware()
print ensRest.getInfoSpecies()
sleep(1) # sleep for a second so we don't get rate-limited

# Linkage Disequilibrium
print ensRest.getLdId(species="human", id="rs1042779", population_name="1000GENOMES:phase_3:KHV", window_size=500, d_prime=1.0)
print ensRest.getLdPairwise(species="human", id1="rs6792369", id2="rs1042779")
print ensRest.getLdRegion(species="human", region="6:25837556..25843455", population_name="1000GENOMES:phase_3:KHV")
sleep(1)

# Lookup
print ensRest.getLookupById(id='ENSG00000157764')
print ensGenomeRest.getLookupByGenomeName(name="campylobacter_jejuni_subsp_jejuni_bh_01_0142")
print ensRest.getLookupByMultipleIds(ids=["ENSG00000157764", "ENSG00000248378" ])
print ensRest.getLookupBySymbol(species="homo_sapiens", symbol="BRCA2", expand=1)
sleep(1)
print ensRest.getLookupByMultipleSymbols(species="homo_sapiens", symbols=["BRCA2", "BRAF"])

# Mapping
print ensRest.getMapCdnaToRegion(id='ENST00000288602', region='100..300')
print ensRest.getMapCdsToRegion(id='ENST00000288602', region='1..1000')
sleep(1) # sleep for a second so we don't get rate-limited
print ensRest.getMapAssemblyOneToTwo(species='human', asm_one='NCBI36', region='X:1000000..1000100:1', asm_two='GRCh37')
print ensRest.getMapTranslationToRegion(id='ENSP00000288602', region='100..300')

# Ontologies and Taxonomy
print ensRest.getAncestorsById(id='GO:0005667')
sleep(1) # sleep for a second so we don't get rate-limited
print ensRest.getAncestorsChartById(id='GO:0005667')
print ensRest.getDescendantsById(id='GO:0005667')
print ensRest.getOntologyById(id='GO:0005667')
sleep(1) # sleep for a second so we don't get rate-limited
print ensRest.getOntologyByName(name='transcription factor complex')
print ensRest.getTaxonomyClassificationById(id='9606')
print ensRest.getTaxonomyById(id='9606')
sleep(1) # sleep for a second so we don't get rate-limited
print ensRest.getTaxonomyByName(name="Homo%25")

# Overlap
print ensRest.getOverlapById(id="ENSG00000157764", feature="gene")
print ensRest.getOverlapByRegion(species="human", region="7:140424943-140624564", feature="gene")
sleep(1)
print ensRest.getOverlapByTranslation(id="ENSP00000288602")

# Regulation
print ensRest.getRegulatoryFeatureById(species="homo_sapiens", id="ENSR00001348195")

# Sequences
print ensRest.getSequenceById(id='ENSG00000157764')
sleep(1)
print ensRest.getSequenceByMultipleIds(ids=["ENSG00000157764", "ENSG00000248378" ])
print ensRest.getSequenceByRegion(species='human', region='X:1000000..1000100')
print ensRest.getSequenceByMultipleRegions(species="homo_sapiens", regions=["X:1000000..1000100:1", "ABBA01004489.1:1..100"])
sleep(1)

# Transcript Haplotypes
print ensRest.getTranscripsHaplotypes(species="homo_sapiens", id="ENST00000288602")

# VEP
print ensRest.getVariantConsequencesByHGVSnotation(species="human", hgvs_notation="AGT:c.803T>C")
print ensRest.getVariantConsequencesById(species='human', id='COSM476')
print ensRest.getVariantConsequencesByMultipleIds(species="human", ids=[ "rs116035550", "COSM476" ])
sleep(1)
print ensRest.getVariantConsequencesByRegion(species='human', region='9:22125503-22125502:1', allele='C')
print ensRest.getVariantConsequencesByMultipleRegions(species="human", variants=["21 26960070 rs116645811 G A . . .", "21 26965148 rs1135638 G A . . ." ] )

# Variation
print ensRest.getVariationById(id="rs56116432", species="homo_sapiens")
print ensRest.getVariationByMultipleIds(ids=["rs56116432", "COSM476" ], species="homo_sapiens")



