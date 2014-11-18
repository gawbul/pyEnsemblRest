"""
	This script allows testing of all pyEnsemblRest functionality.
"""

# import required modules
from ensemblrest import EnsemblRest
from time import sleep
import unittest
import os, glob, sys
import json

# setup new EnsemblRest object
ensemblrest = EnsemblRest()

# get all test files and load each into test file handle dict
test_fh_map = {}
alltests_path = os.path.split(os.path.realpath(__file__))[0]
testfiles = glob.glob(os.path.join(alltests_path, '*.*'))
for testfile in testfiles:
	testfile = os.path.split(testfile)[-1]
	(filename, extension) = testfile.split('.')
	if testfile == os.path.basename(__file__) or extension.startswith('py'):
		pass
	testfile_fh = open(os.path.join(alltests_path, testfile), 'r')
	test_fh_map[filename] = testfile_fh.read().rstrip()
	testfile_fh.close()

class TestEnsemblRest(unittest.TestCase):
	def test_archive(self):
		self.assertEqual(ensemblrest.getArchiveById(id='ENSG00000157764'), test_fh_map['getarchivebyid'])

	def test_comparative_genomics(self):
		# Comparative Genomics
		self.assertEqual(str(ensemblrest.getGeneTreeById(id='ENSGT00390000003602')), test_fh_map['getgenetreebyid'])
		self.assertEqual(str(ensemblrest.getGeneTreeByMemberId(id='ENSG00000157764')), test_fh_map['getgenetreebymemberid'])
		self.assertEqual(str(ensemblrest.getGeneTreeByMemberSymbol(species='human', symbol='BRCA2')), test_fh_map['getgenetreebymembersymbol'])
		self.assertEqual(str(ensemblrest.getAlignmentBySpeciesRegion(species='human', region='2:106040000-106040050:1')), test_fh_map['gethomologybyid'])
		self.assertEqual(str(ensemblrest.getHomologyById(id='ENSG00000157764')), test_fh_map['gethomologybyid'])
		sleep(1) # sleep for a second so we don't get rate-limited
		self.assertEqual(str(ensemblrest.getHomologyBySymbol(species='human', symbol='BRCA2')), test_fh_map['gethomologybysymbol'])

"""
	def test_cross_references(self):
		# Cross References
		self.assertEqual(str(ensemblrest.getXrefsById(id='ENSG00000157764')), test_fh_map['getxrefsbyid'])
		self.assertEqual(str(ensemblrest.getXrefsByName(species='human', name='BRCA2')), test_fh_map['getxrefsbyname'])
		self.assertEqual(str(ensemblrest.getXrefsBySymbol(species='human', symbol='BRCA2')), test_fh_map['getxrefsbysymbol'])
	
	def test_information(self):
		# Information
		self.assertEqual(str(ensemblrest.getInfoAnalysis(species='human')), test_fh_map['getinfoanalysis'])
		sleep(1) # sleep for a second so we don't get rate-limited
		self.assertEqual(str(ensemblrest.getInfoAssembly(species='human')), test_fh_map['getinfoassembly'])
		self.assertEqual(str(ensemblrest.getInfoAssemblyRegion(species='human', region_name='X')), test_fh_map['getinfoassemblyregion'])
		self.assertEqual(str(ensemblrest.getInfoBiotypes(species='human')), test_fh_map['getinfobiotypes'])
		self.assertEqual(str(ensemblrest.getInfoComparaMethods()), test_fh_map['getinfocomparamethods'])
		self.assertEqual(str(ensemblrest.getInfoComparaSpeciesSets(methods='')), test_fh_map['getinfocomparaspeciessets'])
		sleep(1) # sleep for a second so we don't get rate-limited
		self.assertEqual(str(ensemblrest.getInfoComparas()), test_fh_map['getinfocomparas'])
		self.assertEqual(str(ensemblrest.getInfoData()), test_fh_map['getinfodata'])
		self.assertEqual(str(ensemblrest.getInfoEgVersion()), test_fh_map['getinfoegversion'])
		self.assertEqual(str(ensemblrest.getInfoExternalDbs(species='human')), test_fh_map['getinfoexternaldbs'])
		self.assertEqual(str(ensemblrest.getInfoDivisions()), test_fh_map['getinfodivisions'])
		sleep(1) # sleep for a second so we don't get rate-limited
		self.assertEqual(str(ensemblrest.getInfoGenomesByName(name='')), test_fh_map['getinfogenomesbyname'])
		self.assertEqual(str(ensemblrest.getInfoGenomesByAccession(accession='')), test_fh_map['getinfogenomesbyaccession'])
		self.assertEqual(str(ensemblrest.getInfoGenomesByAssembly(assembly='')), test_fh_map['getinfogenomesbyassembly'])
		self.assertEqual(str(ensemblrest.getInfoGenomesByDivision(division='')), test_fh_map['getinfogenomesbydivision'])
		self.assertEqual(str(ensemblrest.getInfoGenomesByTaxonomy(taxonomy='')), test_fh_map['getinfogenomesbytaxonomy'])
		sleep(1) # sleep for a second so we don't get rate-limited
		self.assertEqual(str(ensemblrest.getInfoPing()), test_fh_map['getinfoping'])
		self.assertEqual(str(ensemblrest.getInfoRest()), test_fh_map['getinforest'])
		self.assertEqual(str(ensemblrest.getInfoSoftware()), test_fh_map['getinfosoftware'])
		self.maxDiff = None
		self.assertItemsEqual(json.dumps(ensemblrest.getInfoSpecies()), test_fh_map['getinfospecies']) # use len here due to changing order of returned dict

	def test_lookup(self):
		# Lookup
		self.assertEqual(str(ensemblrest.getLookupById(id='ENSG00000157764')), test_fh_map['getlookupbyid'])
		sleep(1) # sleep for a second so we don't get rate-limited
		self.assertEqual(str(ensemblrest.getLookupByGenomeName(name='')), test_fh_map['getlookupbygenomename'])
		self.assertEqual(str(ensemblrest.getLookupBySpeciesSymbol(species='human', symbol='BRCA2')), test_fh_map['getlookupbyspeciessymbol'])

	def test_mapping(self):
		# Mapping
		self.assertEqual(str(ensemblrest.getMapAssemblyOneToTwo(species='human', asm_one='NCBI36', region='X:1000000..1000100:1', asm_two='GRCh37')), test_fh_map['getmapassemblyonetotwo'])
		self.assertEqual(str(ensemblrest.getMapCdnaToRegion(id='ENST00000288602', region='100..300')), test_fh_map['getmapcdnatoregion'])
		self.assertEqual(str(ensemblrest.getMapCdsToRegion(id='ENST00000288602', region='1..1000')), test_fh_map['getmapcdstoregion'])
		sleep(1) # sleep for a second so we don't get rate-limited
		self.assertEqual(str(ensemblrest.getMapTranslationToRegion(id='ENSP00000288602', region='100..300')), test_fh_map['getmaptranslationtoregion'])

	def test_ontologies_and_taxonomy(self):
		# Ontologies and Taxonomy
		self.assertEqual(str(ensemblrest.getAncestorsById(id='GO:0005667')), test_fh_map['getancestorsbyid'])
		self.assertEqual(str(ensemblrest.getAncestorsChartById(id='GO:0005667')), test_fh_map['getancestorschartbyid'])
		self.assertEqual(str(ensemblrest.getDescendentsById(id='GO:0005667')), test_fh_map['getdescendentsbyid'])
		self.assertEqual(str(ensemblrest.getOntologyById(id='GO:0005667')), test_fh_map['getontologybyid'])
		sleep(1) # sleep for a second so we don't get rate-limited
		self.assertEqual(str(ensemblrest.getOntologyByName(name='transcription factor complex')), test_fh_map['getontologybyname'])
		self.assertEqual(str(ensemblrest.getTaxonomyClassificationById(id='9606')), test_fh_map['gettaxonomyclassificationbyid'])
		self.assertEqual(len(str(ensemblrest.getTaxonomyById(id='9606'))), len(test_fh_map['gettaxonomybyid']))
		self.assertEqual(len(str(ensemblrest.getTaxonomyByName(name=''))), len(test_fh_map['gettaxonomybyname']))

	def test_overlap(self):
		# Overlap
		self.assertEqual(str(ensemblrest.getOverlapById(id='ENSG00000157764')), test_fh_map['getoverlapbyid'])
		self.assertEqual(str(ensemblrest.getOverlapBySpeciesRegion(species='', region='')), test_fh_map['getoverlapbyspeciesregion'])
		sleep(1) # sleep for a second so we don't get rate-limited
		self.assertEqual(str(ensemblrest.getOverlapByTranslation(id='ENSG00000157764')), test_fh_map['getoverlapbytranslation'])
		
	def test_sequences(self):
		# Sequences
		self.assertEqual(str(ensemblrest.getSequenceById(id='ENSG00000157764')), test_fh_map['getsequencebyid'])
		self.assertEqual(str(ensemblrest.getSequenceByRegion(species='human', region='X:1000000..1000100')), test_fh_map['getsequencebyregion'])

	def test_variation(self):
		# Variation
		self.assertEqual(str(ensemblrest.getVariationBySpeciesId(species='human', id='')), test_fh_map['getvariationbyspeciesid'])
		self.assertEqual(str(ensemblrest.getVariantConsequencesBySpeciesId(species='human', id='')), test_fh_map['getvariantconsequencesbyspeciesid'])
		self.assertEqual(str(ensemblrest.getVariantConsequencesBySpeciesRegionAllele(species='human', region='9:22125503-22125502:1', allele='C')), test_fh_map['getvariantconsequencesbyspeciesregionallele'])
"""
if __name__ == '__main__':
	unittest.main()
