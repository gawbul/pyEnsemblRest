"""
	This script allows testing of all pyEnsemblRest functionality.
"""

# import required modules
from ensemblrest import EnsemblRest
from time import sleep
import nose
import glob, json, md5, os, sys

# setup new EnsemblRest object
ensemblrest = EnsemblRest()

class TestEnsemblRest(unittest.TestCase):
	def test_archive(self):
		self.assertEqual(md5.new(ensemblrest.getArchiveById(id='ENSG00000157764')).hexdigest(), '7f34655ad100ad0650e4814d24c9091e')

	def test_comparative_genomics(self):
		# Comparative Genomics
		self.assertEqual(md5.new(ensemblrest.getGeneTreeById(id='ENSGT00390000003602')).hexdigest(), 'bbde0d491222726ac0f63846f99c0a6b')
		self.assertEqual(md5.new(ensemblrest.getGeneTreeByMemberId(id='ENSG00000157764')).hexdigest(), 'f7b0667ffb52d39f702ab32a7a748a40')
		sleep(1) # sleep for a second so we don't get rate-limited
		self.assertEqual(md5.new(ensemblrest.getGeneTreeByMemberSymbol(species='human', symbol='BRCA2')).hexdigest(), '1f8b34d923def96e919d047107886584')
		self.assertEqual(md5.new(ensemblrest.getAlignmentBySpeciesRegion(species='human', region='2:106040000-106040050:1')).hexdigest(), '09df11f8e63bfc65e4830288bc3adf85')
		self.assertEqual(md5.new(ensemblrest.getHomologyById(id='ENSG00000157764')).hexdigest(), '3ed5e55d97ac91cd92a61f1f0e3920b0')
		sleep(1) # sleep for a second so we don't get rate-limited
		self.assertEqual(md5.new(ensemblrest.getHomologyBySymbol(species='human', symbol='BRCA2')).hexdigest(), 'eb0ad0a949e9e083fc05718590b57be0')

"""
	def test_cross_references(self):
		# Cross References
		self.assertEqual(md5.new(ensemblrest.getXrefsById(id='ENSG00000157764')).hexdigest(), '')
		self.assertEqual(md5.new(ensemblrest.getXrefsByName(species='human', name='BRCA2')).hexdigest(), '')
		self.assertEqual(md5.new(ensemblrest.getXrefsBySymbol(species='human', symbol='BRCA2')).hexdigest(), '')
	
	def test_information(self):
		# Information
		self.assertEqual(md5.new(ensemblrest.getInfoAnalysis(species='human')).hexdigest(), test_fh_map['getinfoanalysis'])
		sleep(1) # sleep for a second so we don't get rate-limited
		self.assertEqual(md5.new(ensemblrest.getInfoAssembly(species='human')).hexdigest(), test_fh_map['getinfoassembly'])
		self.assertEqual(md5.new(ensemblrest.getInfoAssemblyRegion(species='human', region_name='X')).hexdigest(), test_fh_map['getinfoassemblyregion'])
		self.assertEqual(md5.new(ensemblrest.getInfoBiotypes(species='human')), test_fh_map['getinfobiotypes'])
		self.assertEqual(md5.new(ensemblrest.getInfoComparaMethods()), test_fh_map['getinfocomparamethods'])
		self.assertEqual(md5.new(ensemblrest.getInfoComparaSpeciesSets(methods='')), test_fh_map['getinfocomparaspeciessets'])
		sleep(1) # sleep for a second so we don't get rate-limited
		self.assertEqual(md5.new(ensemblrest.getInfoComparas()), test_fh_map['getinfocomparas'])
		self.assertEqual(md5.new(ensemblrest.getInfoData()), test_fh_map['getinfodata'])
		self.assertEqual(md5.new(ensemblrest.getInfoEgVersion()), test_fh_map['getinfoegversion'])
		self.assertEqual(md5.new(ensemblrest.getInfoExternalDbs(species='human')), test_fh_map['getinfoexternaldbs'])
		self.assertEqual(md5.new(ensemblrest.getInfoDivisions()), test_fh_map['getinfodivisions'])
		sleep(1) # sleep for a second so we don't get rate-limited
		self.assertEqual(md5.new(ensemblrest.getInfoGenomesByName(name='')), test_fh_map['getinfogenomesbyname'])
		self.assertEqual(md5.new(ensemblrest.getInfoGenomesByAccession(accession='')), test_fh_map['getinfogenomesbyaccession'])
		self.assertEqual(md5.new(ensemblrest.getInfoGenomesByAssembly(assembly='')), test_fh_map['getinfogenomesbyassembly'])
		self.assertEqual(md5.new(ensemblrest.getInfoGenomesByDivision(division='')), test_fh_map['getinfogenomesbydivision'])
		self.assertEqual(md5.new(ensemblrest.getInfoGenomesByTaxonomy(taxonomy='')), test_fh_map['getinfogenomesbytaxonomy'])
		sleep(1) # sleep for a second so we don't get rate-limited
		self.assertEqual(md5.new(ensemblrest.getInfoPing()), test_fh_map['getinfoping'])
		self.assertEqual(md5.new(ensemblrest.getInfoRest()), test_fh_map['getinforest'])
		self.assertEqual(md5.new(ensemblrest.getInfoSoftware()), test_fh_map['getinfosoftware'])
		self.maxDiff = None
		self.assertItemsEqual(json.dumps(ensemblrest.getInfoSpecies()), test_fh_map['getinfospecies']) # use len here due to changing order of returned dict

	def test_lookup(self):
		# Lookup
		self.assertEqual(md5.new(ensemblrest.getLookupById(id='ENSG00000157764')), test_fh_map['getlookupbyid'])
		sleep(1) # sleep for a second so we don't get rate-limited
		self.assertEqual(md5.new(ensemblrest.getLookupByGenomeName(name='')), test_fh_map['getlookupbygenomename'])
		self.assertEqual(md5.new(ensemblrest.getLookupBySpeciesSymbol(species='human', symbol='BRCA2')), test_fh_map['getlookupbyspeciessymbol'])

	def test_mapping(self):
		# Mapping
		self.assertEqual(md5.new(ensemblrest.getMapAssemblyOneToTwo(species='human', asm_one='NCBI36', region='X:1000000..1000100:1', asm_two='GRCh37')), test_fh_map['getmapassemblyonetotwo'])
		self.assertEqual(md5.new(ensemblrest.getMapCdnaToRegion(id='ENST00000288602', region='100..300')), test_fh_map['getmapcdnatoregion'])
		self.assertEqual(md5.new(ensemblrest.getMapCdsToRegion(id='ENST00000288602', region='1..1000')), test_fh_map['getmapcdstoregion'])
		sleep(1) # sleep for a second so we don't get rate-limited
		self.assertEqual(md5.new(ensemblrest.getMapTranslationToRegion(id='ENSP00000288602', region='100..300')), test_fh_map['getmaptranslationtoregion'])

	def test_ontologies_and_taxonomy(self):
		# Ontologies and Taxonomy
		self.assertEqual(md5.new(ensemblrest.getAncestorsById(id='GO:0005667')), test_fh_map['getancestorsbyid'])
		self.assertEqual(md5.new(ensemblrest.getAncestorsChartById(id='GO:0005667')), test_fh_map['getancestorschartbyid'])
		self.assertEqual(md5.new(ensemblrest.getDescendentsById(id='GO:0005667')), test_fh_map['getdescendentsbyid'])
		self.assertEqual(md5.new(ensemblrest.getOntologyById(id='GO:0005667')), test_fh_map['getontologybyid'])
		sleep(1) # sleep for a second so we don't get rate-limited
		self.assertEqual(md5.new(ensemblrest.getOntologyByName(name='transcription factor complex')), test_fh_map['getontologybyname'])
		self.assertEqual(md5.new(ensemblrest.getTaxonomyClassificationById(id='9606')), test_fh_map['gettaxonomyclassificationbyid'])
		self.assertEqual(md5.new(ensemblrest.getTaxonomyById(id='9606')), len(test_fh_map['gettaxonomybyid']))
		self.assertEqual(md5.new(ensemblrest.getTaxonomyByName(name='')), len(test_fh_map['gettaxonomybyname']))

	def test_overlap(self):
		# Overlap
		self.assertEqual(md5.new(ensemblrest.getOverlapById(id='ENSG00000157764')), test_fh_map['getoverlapbyid'])
		self.assertEqual(md5.new(ensemblrest.getOverlapBySpeciesRegion(species='', region='')), test_fh_map['getoverlapbyspeciesregion'])
		sleep(1) # sleep for a second so we don't get rate-limited
		self.assertEqual(md5.new(ensemblrest.getOverlapByTranslation(id='ENSG00000157764')), test_fh_map['getoverlapbytranslation'])
		
	def test_sequences(self):
		# Sequences
		self.assertEqual(md5.new(ensemblrest.getSequenceById(id='ENSG00000157764')), test_fh_map['getsequencebyid'])
		self.assertEqual(md5.new(ensemblrest.getSequenceByRegion(species='human', region='X:1000000..1000100')), test_fh_map['getsequencebyregion'])

	def test_variation(self):
		# Variation
		self.assertEqual(md5.new(ensemblrest.getVariationBySpeciesId(species='human', id='')), test_fh_map['getvariationbyspeciesid'])
		self.assertEqual(md5.new(ensemblrest.getVariantConsequencesBySpeciesId(species='human', id='')), test_fh_map['getvariantconsequencesbyspeciesid'])
		self.assertEqual(md5.new(ensemblrest.getVariantConsequencesBySpeciesRegionAllele(species='human', region='9:22125503-22125502:1', allele='C')), test_fh_map['getvariantconsequencesbyspeciesregionallele'])
"""
if __name__ == '__main__':
	unittest.main()
