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
from ensemblrest import EnsemblRest
import md5
from nose.tools import assert_equals
from time import sleep

# setup new EnsemblRest object
ensemblrest = EnsemblRest()

def test_archive():
  print('in test_archive')
  assert_equals(md5.new(ensemblrest.getArchiveById(id='ENSG00000157764')).hexdigest(), '7f34655ad100ad0650e4814d24c9091e')

def test_comparative_genomics():
  print('in test_comparative_genomics')
  # Comparative Genomics
  assert_equals(md5.new(ensemblrest.getGeneTreeById(id='ENSGT00390000003602')).hexdigest(), 'bbde0d491222726ac0f63846f99c0a6b')
  assert_equals(len(ensemblrest.getGeneTreeByMemberId(id='ENSG00000157764')), 2235232)
  sleep(1) # sleep for a second so we don't get rate-limited
  assert_equals(len(ensemblrest.getGeneTreeByMemberSymbol(species='human', symbol='BRCA2')), 265673)
  assert_equals(len(ensemblrest.getAlignmentBySpeciesRegion(species='human', region='2:106040000-106040050:1')), 2972)
  assert_equals(md5.new(ensemblrest.getHomologyById(id='ENSG00000157764')).hexdigest(), '3ed5e55d97ac91cd92a61f1f0e3920b0')
  sleep(1) # sleep for a second so we don't get rate-limited
  assert_equals(md5.new(ensemblrest.getHomologyBySymbol(species='human', symbol='BRCA2')).hexdigest(), 'eb0ad0a949e9e083fc05718590b57be0')

"""
def test_cross_references():
	# Cross References
	assert_equals(md5.new(ensemblrest.getXrefsById(id='ENSG00000157764')).hexdigest(), '')
	assert_equals(md5.new(ensemblrest.getXrefsByName(species='human', name='BRCA2')).hexdigest(), '')
	assert_equals(md5.new(ensemblrest.getXrefsBySymbol(species='human', symbol='BRCA2')).hexdigest(), '')

def test_information():
	# Information
	assert_equals(md5.new(ensemblrest.getInfoAnalysis(species='human')).hexdigest(), test_fh_map['getinfoanalysis'])
	sleep(1) # sleep for a second so we don't get rate-limited
	assert_equals(md5.new(ensemblrest.getInfoAssembly(species='human')).hexdigest(), test_fh_map['getinfoassembly'])
	assert_equals(md5.new(ensemblrest.getInfoAssemblyRegion(species='human', region_name='X')).hexdigest(), test_fh_map['getinfoassemblyregion'])
	assert_equals(md5.new(ensemblrest.getInfoBiotypes(species='human')), test_fh_map['getinfobiotypes'])
	assert_equals(md5.new(ensemblrest.getInfoComparaMethods()), test_fh_map['getinfocomparamethods'])
	assert_equals(md5.new(ensemblrest.getInfoComparaSpeciesSets(methods='')), test_fh_map['getinfocomparaspeciessets'])
	sleep(1) # sleep for a second so we don't get rate-limited
	assert_equals(md5.new(ensemblrest.getInfoComparas()), test_fh_map['getinfocomparas'])
	assert_equals(md5.new(ensemblrest.getInfoData()), test_fh_map['getinfodata'])
	assert_equals(md5.new(ensemblrest.getInfoEgVersion()), test_fh_map['getinfoegversion'])
	assert_equals(md5.new(ensemblrest.getInfoExternalDbs(species='human')), test_fh_map['getinfoexternaldbs'])
	assert_equals(md5.new(ensemblrest.getInfoDivisions()), test_fh_map['getinfodivisions'])
	sleep(1) # sleep for a second so we don't get rate-limited
	assert_equals(md5.new(ensemblrest.getInfoGenomesByName(name='')), test_fh_map['getinfogenomesbyname'])
	assert_equals(md5.new(ensemblrest.getInfoGenomesByAccession(accession='')), test_fh_map['getinfogenomesbyaccession'])
	assert_equals(md5.new(ensemblrest.getInfoGenomesByAssembly(assembly='')), test_fh_map['getinfogenomesbyassembly'])
	assert_equals(md5.new(ensemblrest.getInfoGenomesByDivision(division='')), test_fh_map['getinfogenomesbydivision'])
	assert_equals(md5.new(ensemblrest.getInfoGenomesByTaxonomy(taxonomy='')), test_fh_map['getinfogenomesbytaxonomy'])
	sleep(1) # sleep for a second so we don't get rate-limited
	assert_equals(md5.new(ensemblrest.getInfoPing()), test_fh_map['getinfoping'])
	assert_equals(md5.new(ensemblrest.getInfoRest()), test_fh_map['getinforest'])
	assert_equals(md5.new(ensemblrest.getInfoSoftware()), test_fh_map['getinfosoftware'])
	self.maxDiff = None
	self.assertItemsEqual(json.dumps(ensemblrest.getInfoSpecies()), test_fh_map['getinfospecies']) # use len here due to changing order of returned dict

def test_lookup():
	# Lookup
	assert_equals(md5.new(ensemblrest.getLookupById(id='ENSG00000157764')), test_fh_map['getlookupbyid'])
	sleep(1) # sleep for a second so we don't get rate-limited
	assert_equals(md5.new(ensemblrest.getLookupByGenomeName(name='')), test_fh_map['getlookupbygenomename'])
	assert_equals(md5.new(ensemblrest.getLookupBySpeciesSymbol(species='human', symbol='BRCA2')), test_fh_map['getlookupbyspeciessymbol'])

def test_mapping():
	# Mapping
	assert_equals(md5.new(ensemblrest.getMapAssemblyOneToTwo(species='human', asm_one='NCBI36', region='X:1000000..1000100:1', asm_two='GRCh37')), test_fh_map['getmapassemblyonetotwo'])
	assert_equals(md5.new(ensemblrest.getMapCdnaToRegion(id='ENST00000288602', region='100..300')), test_fh_map['getmapcdnatoregion'])
	assert_equals(md5.new(ensemblrest.getMapCdsToRegion(id='ENST00000288602', region='1..1000')), test_fh_map['getmapcdstoregion'])
	sleep(1) # sleep for a second so we don't get rate-limited
	assert_equals(md5.new(ensemblrest.getMapTranslationToRegion(id='ENSP00000288602', region='100..300')), test_fh_map['getmaptranslationtoregion'])

def test_ontologies_and_taxonomy():
	# Ontologies and Taxonomy
	assert_equals(md5.new(ensemblrest.getAncestorsById(id='GO:0005667')), test_fh_map['getancestorsbyid'])
	assert_equals(md5.new(ensemblrest.getAncestorsChartById(id='GO:0005667')), test_fh_map['getancestorschartbyid'])
	assert_equals(md5.new(ensemblrest.getDescendentsById(id='GO:0005667')), test_fh_map['getdescendentsbyid'])
	assert_equals(md5.new(ensemblrest.getOntologyById(id='GO:0005667')), test_fh_map['getontologybyid'])
	sleep(1) # sleep for a second so we don't get rate-limited
	assert_equals(md5.new(ensemblrest.getOntologyByName(name='transcription factor complex')), test_fh_map['getontologybyname'])
	assert_equals(md5.new(ensemblrest.getTaxonomyClassificationById(id='9606')), test_fh_map['gettaxonomyclassificationbyid'])
	assert_equals(md5.new(ensemblrest.getTaxonomyById(id='9606')), len(test_fh_map['gettaxonomybyid']))
	assert_equals(md5.new(ensemblrest.getTaxonomyByName(name='')), len(test_fh_map['gettaxonomybyname']))

def test_overlap():
	# Overlap
	assert_equals(md5.new(ensemblrest.getOverlapById(id='ENSG00000157764')), test_fh_map['getoverlapbyid'])
	assert_equals(md5.new(ensemblrest.getOverlapBySpeciesRegion(species='', region='')), test_fh_map['getoverlapbyspeciesregion'])
	sleep(1) # sleep for a second so we don't get rate-limited
	assert_equals(md5.new(ensemblrest.getOverlapByTranslation(id='ENSG00000157764')), test_fh_map['getoverlapbytranslation'])
	
def test_sequences():
	# Sequences
	assert_equals(md5.new(ensemblrest.getSequenceById(id='ENSG00000157764')), test_fh_map['getsequencebyid'])
	assert_equals(md5.new(ensemblrest.getSequenceByRegion(species='human', region='X:1000000..1000100')), test_fh_map['getsequencebyregion'])

def test_variation():
	# Variation
	assert_equals(md5.new(ensemblrest.getVariationBySpeciesId(species='human', id='')), test_fh_map['getvariationbyspeciesid'])
	assert_equals(md5.new(ensemblrest.getVariantConsequencesBySpeciesId(species='human', id='')), test_fh_map['getvariantconsequencesbyspeciesid'])
	assert_equals(md5.new(ensemblrest.getVariantConsequencesBySpeciesRegionAllele(species='human', region='9:22125503-22125502:1', allele='C')), test_fh_map['getvariantconsequencesbyspeciesregionallele'])
"""
