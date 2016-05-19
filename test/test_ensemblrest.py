# -*- coding: utf-8 -*-
"""
    
    This file is part of pyEnsemblRest.
    Copyright (C) 2013-2016, Steve Moss

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

# import my module
import ensemblrest

# import other modules
import json
import time
import shlex
import logging
import subprocess
import unittest

#An useful way to defined a logger lever, handler, and formatter
#logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)

#logger instance
logger = logging.getLogger(__name__)

def launch(cmd):
    """calling a cmd with subprocess"""
    
    logger.debug("Executing: %s" %(cmd))
    
    args = shlex.split(cmd)
    p = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = p.communicate()
    
    if len(stderr) > 0: 
        logger.debug(stderr)
        
    # debug
    logger.debug("Got: %s" %(stdout))
        
    return stdout

def jsonFromCurl(curl_cmd):
    """Parsing a JSON curl result"""
    
    # execute the curl cmd
    result = launch(curl_cmd)
    
    # load it as a dictionary
    data = json.loads(result)
    
    return data

class EnsemblRest(unittest.TestCase):
    """A class to test EnsemblRest methods"""
    
    def setUp(self):
        """Create a EnsemblRest object"""
        self.EnsEMBL = ensemblrest.EnsemblRest()
        
    def tearDown(self):
        """Sleep a while before doing next request"""
        time.sleep(0.1)
        
    def test_setHeaders(self):
        """Testing EnsemblRest with no headers provided"""
        
        user_agent = ensemblrest.ensembl_config.ensembl_user_agent
        self.EnsEMBL = ensemblrest.EnsemblRest(headers={})
        self.assertEqual(self.EnsEMBL.session.headers.get("User-Agent"), user_agent)
        
    def test_mandatoryParameters(self):
        """Testing EnsemblRest with no mandatory parameters"""
        
        self.assertRaisesRegexp(Exception, "mandatory param .* not specified", self.EnsEMBL.getArchiveById)

    def test_getArchiveById(self):
        """Test archive GET endpoint"""
      
        # get the curl cmd from ensembl site:
        curl_cmd = "curl 'http://rest.ensembl.org/archive/id/ENSG00000157764?' -H 'Content-type:application/json'"
        
        # execute the curl cmd an get data as a dictionary
        reference = jsonFromCurl(curl_cmd)
      
        # execute EnsemblRest function
        test = self.EnsEMBL.getArchiveById(id='ENSG00000157764')
        
        # testing values
        self.assertDictEqual(reference, test)
        
    def test_getXMLArchiveById(self):
        """text archive GET endpoint returning XML"""
        
        # get the curl cmd from ensembl site:
        curl_cmd = "curl 'http://rest.ensembl.org/archive/id/ENSG00000157764?' -H 'Content-type:text/xml'"
        
        # execute the curl cmd an get data as a dictionary
        reference = launch(curl_cmd)
      
        # execute EnsemblRest function
        test = self.EnsEMBL.getArchiveById(id='ENSG00000157764', content_type="text/xml")
        
        # testing values
        self.assertEqual(reference, test)
        
        
    def test_getArchiveByMultipleIds(self):
        """Test archive POST endpoint"""
        
        curl_cmd = """curl 'http://rest.ensembl.org/archive/id' -H 'Content-type:application/json' \
-H 'Accept:application/json' -X POST -d '{ "id" : ["ENSG00000157764", "ENSG00000248378"] }'"""

        # execute the curl cmd an get data as a dictionary
        reference = jsonFromCurl(curl_cmd)
      
        # execute EnsemblRest function
        test = self.EnsEMBL.getArchiveByMultipleIds(id=["ENSG00000157764", "ENSG00000248378"])
        
        # testing values
        self.assertListEqual(reference, test)
        
    def test_getGeneTreeById(self):
        """Test genetree by id GET method"""
        
        curl_cmd = """curl 'http://rest.ensembl.org/genetree/id/ENSGT00390000003602?' -H 'Content-type:application/json'"""
                
        # execute the curl cmd an get data as a dictionary
        reference = jsonFromCurl(curl_cmd)
      
        # execute EnsemblRest function. Dealing with application/json is simpler, since text/x-phyloxml+xml may change elements order
        test = self.EnsEMBL.getGeneTreeById(id='ENSGT00390000003602', content_type="application/json")
        
        # testing values
        self.assertEqual(reference, test)
        
        """        
    def test_getGeneTreeMemberById(self):
        print ensRest.getGeneTreeMemberById(id='ENSG00000157764')
        
    def test_getGeneTreeMemberBySymbol(self):
        print ensRest.getGeneTreeMemberBySymbol(species='human', symbol='BRCA2')
        
    def test_getAlignmentByRegion(self):
        print ensRest.getAlignmentByRegion(species="taeniopygia_guttata", region="2:106040000-106040050:1", species_set_group="sauropsids")
        
    def test_getHomologyById(self):
        print ensRest.getHomologyById(id='ENSG00000157764')
        
    def test_getHomologyBySymbol(self):
        print ensRest.getHomologyBySymbol(species='human', symbol='BRCA2')

        """

    def test_getSequenceByMultipleIds_additional_arguments(self):
        """Testing getSequenceByMultipleIds with mask="soft" and expand_3prime=100"""

        curl_cmd = """curl 'http://rest.ensembl.org/sequence/region/human?mask=soft;expand_3prime=100' -H 'Content-type:application/json' -H 'Accept:application/json' -X POST -d '{ "regions" : ["X:1000000..1000100:1", "ABBA01004489.1:1..100"] }'"""
        
        # execute the curl cmd an get data as a dictionary
        reference = jsonFromCurl(curl_cmd)
      
        # execute EnsemblRest function
        test = self.EnsEMBL.getSequenceByMultipleRegions(species="human", regions=["X:1000000..1000100:1", "ABBA01004489.1:1..100"], expand_3prime=100, mask="soft")
        
        # testing values
        self.assertEqual(reference, test)

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

class EnsemblGenomeRest(unittest.TestCase):
    """A class to test EnsemblGenomeRest methods"""
    
    def setUp(self):
        """Create a EnsemblRest object"""
        self.EnsEMBL = ensemblrest.EnsemblGenomeRest()
        
    def tearDown(self):
        """Sleep a while before doing next request"""
        time.sleep(0.1)

    #TODO
#    print ensGenomeRest.getGeneFamilyById(id="MF_01687", compara="bacteria")
#    print ensGenomeRest.getGeneFamilyMemberById(id="b0344", compara="bacteria")
#    print ensGenomeRest.getGeneFamilyMemberBySymbol(symbol="lacZ", species="escherichia_coli_str_k_12_substr_mg1655", compara="bacteria")

if __name__ == "__main__":
    unittest.main()

    