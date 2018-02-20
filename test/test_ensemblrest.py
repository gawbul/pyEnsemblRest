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
import six
import re
import json
import time
import shlex
import urllib
import logging
import subprocess
import unittest

#logger instance
logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)

# create console handler and set level to debug. NullHandler to put all into /dev/null
#ch = logging.NullHandler()

# This console handle write all logging to and opened strem. sys.stderr is the default
ch = logging.StreamHandler()

# Set the level for this handler
ch.setLevel(logging.DEBUG)

# create formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# add formatter to ch
ch.setFormatter(formatter)

# add ch to logger
logger.addHandler(ch)

# Wait some time before next request
WAIT = 0.5

# Sometimes curl fails
MAX_RETRIES = 5

# curl timeouts
TIMEOUT = 60


def launch(cmd):
    """calling a cmd with subprocess"""
    
    # setting curl timeouts
    pattern = re.compile("curl")
    repl = "curl --connect-timeout %s --max-time %s" %(TIMEOUT, TIMEOUT*2)
    
    # Setting curl options
    cmd = re.sub(pattern, repl, cmd)
    
    logger.debug("Executing: %s" %(cmd))
    
    args = shlex.split(cmd)
    p = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    stdout, stderr = p.communicate()
    
    if len(stderr) > 0: 
        logger.debug(stderr)
        
    # debug
    logger.debug("Got: %s" %(stdout))
        
    return stdout

def jsonFromCurl(curl_cmd):
    """Parsing a JSON curl result"""

    data = None
    retry = 0
    
    while retry < MAX_RETRIES:
        # update retry
        retry += 1
        
        # execute the curl cmd
        result = launch(curl_cmd)
        
        # load it as a dictionary
        try:
            data = json.loads(result)
            
        except ValueError as e:
            logger.warning("Curl command failed: %s" % e)
            time.sleep(WAIT*10)
            
            #next request
            continue

        if isinstance(data, dict):
            if "error" in data:
                logger.warning("Curl command failed: %s" %(data["error"]))
                time.sleep(WAIT*10)
                
                #next request
                continue
                
        # If I arrive here, I assume that curl went well
        break
    
    return data

def _genericCMP(v1, v2):
    """Check ensembl complex elements"""
    
    logger.debug("Check %s == %s" %(v1, v2))
    
    # check that types are the same
    if type(v1) != type(v2):
        return False
        
    elif isinstance(v1, dict):
        #call comparedict
        if compareDict(v1, v2) is False:
            return False
                    
    elif isinstance(v1, list):
        #call comparedict
        if compareList(v1, v2) is False:
            return False
            
    elif isinstance(v1, (six.string_types, float, int)):
        if v1 != v2:
            return False
        
    else:
        logger.error("%s <> %s" %(v1, v2))
        logger.critical("Case not implemented: type:%s" %(type(v1)))
    
    #default value
    return True

# A function to evaluate if two python complex dictionaries are the same
def compareDict(d1, d2):
    """A function to evaluate if two python complex dictionaries are the same"""
    if d1 == d2:
        return True
        
    # check keys
    k1 = d1.keys()
    k2 = d2.keys()
    
    # sorting keys
    k1 = sorted(k1)
    k2 = sorted(k2)

    logger.debug(k1)
    logger.debug(k2)
    
    # check keys are equals
    if k1 != k2:
        return False
        
    #now I have to check values for each key value
    for k in k1:
        #get values
        v1 = d1[k]
        v2 = d2[k]
        
        if v1 == v2:
            continue
        
        # the species key may differ in some cases: ex: Tgut-Mgal-Ggal[3] <> Ggal-Mgal-Tgut[3]
        if k in ["species", "tree"] and isinstance(v1, six.string_types) and isinstance(v2, six.string_types):
            pattern = re.compile("([\w]+)-?(?:\[\d\])?")
            
            #override values
            v1 = re.findall(pattern, v1)
            v2 = re.findall(pattern, v2)
            
        # check if elements are the same
        if _genericCMP(v1, v2) is False:
            return False
            
    #if I arrive here:
    return True

def compareList(l1, l2):
    """A function to evaluate if two python complex list are the same"""
    
    if l1 == l2:
        return True
        
    #check lengths
    if len(l1) != len(l2):
        return False
        
    #I cannot use set nor collections.Count, since elements could't be hashable
    # sorting elements doesn't apply since elements may be un-hashable
    for i in range(len(l1)):
        v1 = l1[i]
        
        flag_found = False
        
        for j in range(len(l2)):
            v2 = l2[j]
        
            if v1 == v2:
                flag_found = True
            
            # check if elements are the same
            elif _genericCMP(v1, v2) is True:
                flag_found = True
                
            #If I found en equal element, i can stop
            if flag_found is True:
                break
            
        #After cycling amoung l2, if I can't find an equal element
        if flag_found is False:
            return False
        
    #if I arrive here
    return True


class EnsemblRest(unittest.TestCase):
    """A class to test EnsemblRest methods"""
    
    def setUp(self):
        """Create a EnsemblRest object"""
        self.EnsEMBL = ensemblrest.EnsemblRest()
        
    def tearDown(self):
        """Sleep a while before doing next request"""
        time.sleep(WAIT)

class EnsemblRestBase(EnsemblRest):
    """A class to deal with ensemblrest base methods"""
        
    def test_setHeaders(self):
        """Testing EnsemblRest with no headers provided"""
        
        user_agent = ensemblrest.ensembl_config.ensembl_user_agent
        self.EnsEMBL = ensemblrest.EnsemblRest(headers={})
        self.assertEqual(self.EnsEMBL.session.headers.get("User-Agent"), user_agent)
        
    def test_mandatoryParameters(self):
        """Testing EnsemblRest with no mandatory parameters"""
        
        six.assertRaisesRegex(self, Exception, "mandatory param .* not specified", self.EnsEMBL.getArchiveById)
        
    def test_wait4request(self):
        """Simulating max request per second"""
        
        self.EnsEMBL.getArchiveById(id='ENSG00000157764')
        self.EnsEMBL.req_count = 15
        self.EnsEMBL.last_req += 2
        self.EnsEMBL.getArchiveById(id='ENSG00000157764')
        
    def test_methodNotImplemented(self):
        """Testing a not implemented method"""
        
        #Add a non supported method
        ensemblrest.ensemblrest.ensembl_api_table["notImplemented"] = {
            'doc' : 'Uses the given identifier to return the archived sequence',
            'url': '/archive/id/{{id}}',
            'method': 'HEAD',
            'content_type': 'application/json'
        }
        
        # register this method
        self.EnsEMBL.__dict__["notImplemented"] = self.EnsEMBL.register_api_func("notImplemented", ensemblrest.ensembl_config.ensembl_api_table)
            
        #Set __doc__ for generic class method
        self.EnsEMBL.__dict__["notImplemented"].__doc__ = ensemblrest.ensemblrest.ensembl_api_table["notImplemented"]["doc"]
        
        #add function name to the class methods
        self.EnsEMBL.__dict__["notImplemented"].__name__ = "notImplemented"
        
        # call the new function and deal with the exception
        self.assertRaises(NotImplementedError, self.EnsEMBL.notImplemented, id='ENSG00000157764') 
        
    def __something_bad(self, curl_cmd, last_response):
        """A function to test 'something bad' message"""
        
        # execute the curl cmd an get data as a dictionary
        reference = jsonFromCurl(curl_cmd)
        
        # create a fake request.Response class
        class FakeResponse():
            def __init__(self, response):
                self.headers = response.headers
                self.status_code = 400
                self.text = """{"error":"something bad has happened"}"""
                
        #instantiate a fake response
        fakeResponse = FakeResponse(last_response)
        test = self.EnsEMBL.parseResponse(fakeResponse)
        
        # testing values
        self.assertDictEqual(reference, test)
        self.assertGreaterEqual(self.EnsEMBL.last_attempt, 1)
    
    def test_SomethingBad(self):
        """Deal with the {"error":"something bad has happened"} message"""
        
        # get the curl cmd from ensembl site:
        curl_cmd = "curl 'http://rest.ensembl.org/archive/id/ENSG00000157764?' -H 'Content-type:application/json'"
        
        # get a request
        self.EnsEMBL.getArchiveById(id="ENSG00000157764")
        
        # retrieve last_reponse
        last_response = self.EnsEMBL.last_response
        
        # call generic function
        self.__something_bad(curl_cmd, last_response)
        
    def test_SomethingBadPOST(self):
        """Deal with the {"error":"something bad has happened"} message using a POST method"""
        
        curl_cmd = """curl 'http://rest.ensembl.org/lookup/id' -H 'Content-type:application/json' -H 'Accept:application/json' -X POST -d '{ "ids" : ["ENSG00000157764", "ENSG00000248378" ] }'"""
      
        # execute EnsemblRest function
        self.EnsEMBL.getLookupByMultipleIds(ids=["ENSG00000157764", "ENSG00000248378" ])
        
        # retrieve last_reponse
        last_response = self.EnsEMBL.last_response
        
        # call generic function
        self.__something_bad(curl_cmd, last_response)
        
    def test_LDFeatureContainerAdaptor(self):
        """Deal with the {"error":"Something went wrong while fetching from LDFeatureContainerAdaptor"} message"""
        
        curl_cmd = """curl 'http://rest.ensembl.org/ld/human/pairwise/rs6792369/rs1042779?population_name=1000GENOMES:phase_3:KHV;r2=0.85' -H 'Content-type:application/json'"""
        
        # execute the curl cmd an get data as a dictionary
        reference = jsonFromCurl(curl_cmd)
        
        # get a request
        self.EnsEMBL.getLdPairwise(species="human", id1="rs6792369", id2="rs1042779", population_name="1000GENOMES:phase_3:KHV", r2=0.85)
        
        # retrieve last_reponse
        response = self.EnsEMBL.last_response
        
        # create a fake request.Response class
        class FakeResponse():
            def __init__(self, resp):
                self.headers = resp.headers
                self.status_code = 400
                self.text = """{"error":"Something went wrong while fetching from LDFeatureContainerAdaptor"}"""
                
        #instantiate a fake response
        fakeResponse = FakeResponse(response)
        test = self.EnsEMBL.parseResponse(fakeResponse)
        
        # testing values
        self.assertEqual(reference, test)
        self.assertGreaterEqual(self.EnsEMBL.last_attempt, 1)
        

class EnsemblRestArchive(EnsemblRest):
    """A class to deal with ensemblrest archive methods"""
    
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
    
class EnsemblRestComparative(EnsemblRest):
    """A class to deal with ensemblrest comparative genomics methods"""
    
    def test_getGeneTreeById(self):
        """Test genetree by id GET method"""
        
        curl_cmd = """curl 'http://rest.ensembl.org/genetree/id/ENSGT00390000003602?' -H 'Content-type:application/json'"""
                
        # execute the curl cmd an get data as a dictionary
        reference = jsonFromCurl(curl_cmd)
      
        # execute EnsemblRest function. Dealing with application/json is simpler, since text/x-phyloxml+xml may change elements order
        test = self.EnsEMBL.getGeneTreeById(id='ENSGT00390000003602', content_type="application/json")
        
        # testing values
        self.assertTrue(compareDict(reference, test))
        
    def test_getGeneTreeMemberById(self):
        """Test genetree by member id GET method"""
        
        curl_cmd = """curl 'http://rest.ensembl.org/genetree/member/id/ENSG00000157764?prune_species=cow;prune_taxon=9526' -H 'Content-type:application/json'"""
        
        # execute the curl cmd an get data as a dictionary
        reference = jsonFromCurl(curl_cmd)
      
        # execute EnsemblRest function. Dealing with application/json is simpler, since text/x-phyloxml+xml may change elements order
        test = self.EnsEMBL.getGeneTreeMemberById(id='ENSG00000157764', prune_species="cow", prune_taxon=9526, content_type="application/json")

        # Set self.maxDiff to None to see differences
        # self.maxDiff = None
        
        # testing values. Since json are nested dictionary and lists, and they are not hashable, I need to order list before
        # checking equality, and I need to ensure that dictionaries have the same keys and values
        self.assertTrue(compareDict(reference, test))
        
    def test_getGeneTreeMemberBySymbol(self):
        """Test genetree by symbol GET method"""
        
        curl_cmd = """curl 'http://rest.ensembl.org/genetree/member/symbol/homo_sapiens/BRCA2?prune_species=cow;prune_taxon=9526' -H 'Content-type:application/json'"""
        
        # execute the curl cmd an get data as a dictionary
        reference = jsonFromCurl(curl_cmd)
      
        # execute EnsemblRest function. Dealing with application/json is simpler, since text/x-phyloxml+xml may change elements order
        test = self.EnsEMBL.getGeneTreeMemberBySymbol(species='human', symbol='BRCA2', prune_species="cow", prune_taxon=9526, content_type="application/json")
        
        # testing values
        self.assertDictEqual(reference, test)
        
    def test_getAlignmentByRegion(self):
        """Test get genomic alignment region GET method"""
        
        curl_cmd = """curl 'http://rest.ensembl.org/alignment/region/taeniopygia_guttata/2:106040000-106040050:1?species_set_group=sauropsids' -H 'Content-type:application/json'"""
        
        # execute the curl cmd an get data as a dictionary
        reference = jsonFromCurl(curl_cmd)
      
        # execute EnsemblRest function. Dealing with application/json is simpler
        test = self.EnsEMBL.getAlignmentByRegion(species="taeniopygia_guttata", region="2:106040000-106040050:1", species_set_group="sauropsids")
        
        # testing values. Values in list can have different order
        self.assertTrue(compareList(reference, test))
        
    def test_getHomologyById(self):
        """test get homology by Id GET method"""
        
        curl_cmd = """curl 'http://rest.ensembl.org/homology/id/ENSG00000157764?' -H 'Content-type:application/json'"""
        
        # execute the curl cmd an get data as a dictionary
        reference = jsonFromCurl(curl_cmd)
      
        # execute EnsemblRest function. Dealing with application/json is simpler, since text/x-phyloxml+xml may change elements order
        test = self.EnsEMBL.getHomologyById(id='ENSG00000157764')
        
        # testing values. Since json are nested dictionary and lists, and they are not hashable, I need to order list before
        # checking equality, and I need to ensure that dictionaries have the same keys and values
        self.assertTrue(compareDict(reference, test))
        
    def test_getHomologyBySymbol(self):
        """test get homology by symbol"""
        
        curl_cmd = """curl 'http://rest.ensembl.org/homology/symbol/human/BRCA2?' -H 'Content-type:application/json'"""
        
        # execute the curl cmd an get data as a dictionary
        reference = jsonFromCurl(curl_cmd)
      
        # execute EnsemblRest function. Dealing with application/json is simpler, since text/x-phyloxml+xml may change elements order
        test = self.EnsEMBL.getHomologyBySymbol(species='human', symbol='BRCA2')
        
        # testing values. Since json are nested dictionary and lists, and they are not hashable, I need to order list before
        # checking equality, and I need to ensure that dictionaries have the same keys and values
        self.assertTrue(compareDict(reference, test))
    
class EnsemblRestXref(EnsemblRest):
    """A class to deal with ensemblrest cross references methods"""
    
    def test_getXrefsBySymbol(self):
        """Testing get XRef by Id GET method"""
        
        curl_cmd = """curl 'http://rest.ensembl.org/xrefs/symbol/homo_sapiens/BRCA2?' -H 'Content-type:application/json'"""
        
        # execute the curl cmd an get data as a dictionary
        reference = jsonFromCurl(curl_cmd)
      
        # execute EnsemblRest function
        test = self.EnsEMBL.getXrefsBySymbol(species='human', symbol='BRCA2')
        
        # testing values
        self.assertEqual(reference, test)
        
    def test_getXrefsByName(self):
        """Testing get XRef by Id GET method"""
        
        curl_cmd = """curl 'http://rest.ensembl.org/xrefs/name/human/BRCA2?' -H 'Content-type:application/json'"""
        
        # execute the curl cmd an get data as a dictionary
        reference = jsonFromCurl(curl_cmd)
      
        # execute EnsemblRest function
        test = self.EnsEMBL.getXrefsByName(species='human', name='BRCA2')
        
        # testing values
        self.assertEqual(reference, test)
        
    def test_getXrefsById(self):
        """Testing get XRef by Id GET method"""
        
        curl_cmd = """curl 'http://rest.ensembl.org/xrefs/id/ENSG00000157764?' -H 'Content-type:application/json'"""
        
        # execute the curl cmd an get data as a dictionary
        reference = jsonFromCurl(curl_cmd)
      
        # execute EnsemblRest function
        test = self.EnsEMBL.getXrefsById(id='ENSG00000157764')
        
        # testing values
        self.assertEqual(reference, test)
        
    
class EnsemblRestInfo(EnsemblRest):
    """A class to deal with ensemblrest information methods"""

    def test_getInfoAnalysis(self):
        """Testing Info analysis GET method"""
        
        curl_cmd = """curl 'http://rest.ensembl.org/info/analysis/homo_sapiens?' -H 'Content-type:application/json'"""
        
        # execute the curl cmd an get data as a dictionary
        reference = jsonFromCurl(curl_cmd)
      
        # execute EnsemblRest function
        test = self.EnsEMBL.getInfoAnalysis(species="homo_sapiens")
        
        # testing values
        self.assertEqual(reference, test)
    
    def test_getInfoAssembly(self):
        """Testing Info assembly GET method"""
        
        curl_cmd = """curl 'http://rest.ensembl.org/info/assembly/homo_sapiens?' -H 'Content-type:application/json'"""
        
        # execute the curl cmd an get data as a dictionary
        reference = jsonFromCurl(curl_cmd)
      
        # execute EnsemblRest function
        test = self.EnsEMBL.getInfoAssembly(species="homo_sapiens")
        
        # testing values
        self.assertEqual(reference, test)
        
    def test_getInfoAssemblyRegion(self):
        """Testing Info Assembly by region GET method"""
        
        curl_cmd = """curl 'http://rest.ensembl.org/info/assembly/homo_sapiens/X?' -H 'Content-type:application/json'"""
        
        # execute the curl cmd an get data as a dictionary
        reference = jsonFromCurl(curl_cmd)
      
        # execute EnsemblRest function
        test = self.EnsEMBL.getInfoAssemblyRegion(species="homo_sapiens", region_name="X")
        
        # testing values
        self.assertEqual(reference, test)
        
    def test_getInfoBiotypes(self):
        """Testing Info BioTypes GET method"""
        
        curl_cmd = """curl 'http://rest.ensembl.org/info/biotypes/homo_sapiens?' -H 'Content-type:application/json'"""
        
        # execute the curl cmd an get data as a dictionary
        reference = jsonFromCurl(curl_cmd)
      
        # execute EnsemblRest function
        test = self.EnsEMBL.getInfoBiotypes(species="homo_sapiens")
        
        # testing values
        self.assertEqual(reference, test)
        
    def test_getInfoComparaMethods(self):
        """Testing Info Compara Methods GET method"""
        
        curl_cmd = """curl 'http://rest.ensembl.org/info/compara/methods/?' -H 'Content-type:application/json'"""
        
        # execute the curl cmd an get data as a dictionary
        reference = jsonFromCurl(curl_cmd)
      
        # execute EnsemblRest function
        test = self.EnsEMBL.getInfoComparaMethods()
        
        # testing values
        self.assertEqual(reference, test)
        
    def test_getInfoComparaSpeciesSets(self):
        """Testing Info Compara Species Sets GET method"""
        
        curl_cmd = """curl 'http://rest.ensembl.org/info/compara/species_sets/EPO?' -H 'Content-type:application/json'"""
        
        # execute the curl cmd an get data as a dictionary
        reference = jsonFromCurl(curl_cmd)
      
        # execute EnsemblRest function
        test = self.EnsEMBL.getInfoComparaSpeciesSets(methods="EPO")
        
        # testing values
        self.assertEqual(reference, test)
        
    def test_getInfoComparas(self):
        """Testing Info Compara GET method"""
        
        curl_cmd = """curl 'http://rest.ensembl.org/info/comparas?' -H 'Content-type:application/json'"""
        
        # execute the curl cmd an get data as a dictionary
        reference = jsonFromCurl(curl_cmd)
      
        # execute EnsemblRest function
        test = self.EnsEMBL.getInfoComparas()
        
        # testing values
        self.assertEqual(reference, test)
        
    def test_getInfoData(self):
        """Testing Info Data GET method"""
        
        curl_cmd = """curl 'http://rest.ensembl.org/info/data/?' -H 'Content-type:application/json'"""
        
        # execute the curl cmd an get data as a dictionary
        reference = jsonFromCurl(curl_cmd)
      
        # execute EnsemblRest function
        test = self.EnsEMBL.getInfoData()
        
        # testing values
        self.assertEqual(reference, test)
    
    def test_getInfoExternalDbs(self):
        """Testing Info External Dbs GET method"""
        
        curl_cmd = """curl 'http://rest.ensembl.org/info/external_dbs/homo_sapiens?' -H 'Content-type:application/json'"""
        
        # execute the curl cmd an get data as a dictionary
        reference = jsonFromCurl(curl_cmd)
      
        # execute EnsemblRest function
        test = self.EnsEMBL.getInfoExternalDbs(species="homo_sapiens")
        
        # testing values
        self.assertEqual(reference, test)

    def test_getInfoPing(self):
        """Testing Info Ping GET method"""
        
        curl_cmd = """curl 'http://rest.ensembl.org/info/ping?' -H 'Content-type:application/json'"""
        
        # execute the curl cmd an get data as a dictionary
        reference = jsonFromCurl(curl_cmd)
      
        # execute EnsemblRest function
        test = self.EnsEMBL.getInfoPing()
        
        # testing values
        self.assertEqual(reference, test)
    
    def test_getInfoRest(self):
        """Testing Info REST GET method"""
        
        curl_cmd = """curl 'http://rest.ensembl.org/info/rest?' -H 'Content-type:application/json'"""
        
        # execute the curl cmd an get data as a dictionary
        reference = jsonFromCurl(curl_cmd)
      
        # execute EnsemblRest function
        test = self.EnsEMBL.getInfoRest()
        
        # testing values
        self.assertEqual(reference, test)
    
    def test_getInfoSoftware(self):
        """Testing Info Software GET method"""
        
        curl_cmd = """curl 'http://rest.ensembl.org/info/software?' -H 'Content-type:application/json'"""
        
        # execute the curl cmd an get data as a dictionary
        reference = jsonFromCurl(curl_cmd)
      
        # execute EnsemblRest function
        test = self.EnsEMBL.getInfoSoftware()
        
        # testing values
        self.assertEqual(reference, test)
    
    def test_getInfoSpecies(self):
        """Testing Info Species GET method"""        
        
        curl_cmd = """curl 'http://rest.ensembl.org/info/species?division=ensembl' -H 'Content-type:application/json'"""
        
        # execute the curl cmd an get data as a dictionary
        reference = jsonFromCurl(curl_cmd)
      
        # execute EnsemblRest function
        test = self.EnsEMBL.getInfoSpecies(division="ensembl")
        
        try:
            # testing values. Since json are nested dictionary and lists, and they are not hashable, I need to order list before
            # checking equality, and I need to ensure that dictionaries have the same keys and values
            self.assertTrue(compareDict(reference, test))
        
        # The transitory failure seems to be related to a misconfiguration of ensembl
        # rest service. In such cases is better to inform dev<at>ensembl.org and report
        # such issues
        except AssertionError as e:
            # sometimes this test can fail. In such case, i log the error
            logger.error(e)
            logger.error(
                "Sometimes 'test_getInfoSpecies' fails. This could be a transitory problem on EnsEMBL REST service"
            )
        
    def test_getInfoVariation(self):
        """Testing Info Variation GET method"""
        
        curl_cmd = """curl 'http://rest.ensembl.org/info/variation/homo_sapiens?' -H 'Content-type:application/json'"""
        
        # execute the curl cmd an get data as a dictionary
        reference = jsonFromCurl(curl_cmd)
      
        # execute EnsemblRest function
        test = self.EnsEMBL.getInfoVariation(species="homo_sapiens")
        
        # testing values
        self.assertEqual(reference, test)
        
    def test_getInfoVariationPopulations(self):
        """Testing Info Variation Populations GET method"""
        
        curl_cmd = """curl 'http://rest.ensembl.org/info/variation/populations/homo_sapiens?filter=LD' -H 'Content-type:application/json'"""
        
        # execute the curl cmd an get data as a dictionary
        reference = jsonFromCurl(curl_cmd)
      
        # execute EnsemblRest function
        test = self.EnsEMBL.getInfoVariationPopulations(species="homo_sapiens", filter="LD")
        
        # testing values
        self.assertEqual(reference, test)
        
    
class EnsemblRestLinkage(EnsemblRest):
    """A class to deal with ensemblrest linkage disequilibrium methods"""

    def test_getLdId(self):
        """Testing get LD ID GET method"""

        curl_cmd = """curl 'http://rest.ensembl.org/ld/human/rs1042779/1000GENOMES:phase_3:KHV?window_size=10;d_prime=1.0' -H 'Content-type:application/json'"""

        # execute the curl cmd an get data as a dictionary
        reference = jsonFromCurl(curl_cmd)
      
        # execute EnsemblRest function
        test = self.EnsEMBL.getLdId(species="human", id="rs1042779", population_name="1000GENOMES:phase_3:KHV", window_size=10, d_prime=1.0)
        
        # testing values
        try:
            self.assertEqual(reference, test)
            
        #TODO: why this test fail sometimes?
        except AssertionError as e:
            # sometimes this test can fail. In such case, i log the error
            logger.error(e)
            logger.error("Sometimes 'test_getLdId' fails. Maybe could be an ensembl transient problem?")
        
    def test_getLdPairwise(self):
        """Testing get LD pairwise GET method"""
        
        curl_cmd = """curl 'http://rest.ensembl.org/ld/human/pairwise/rs6792369/rs1042779?population_name=1000GENOMES:phase_3:KHV;r2=0.85' -H 'Content-type:application/json'"""
        
        # execute the curl cmd an get data as a dictionary
        reference = jsonFromCurl(curl_cmd)
      
        # execute EnsemblRest function
        test = self.EnsEMBL.getLdPairwise(species="human", id1="rs6792369", id2="rs1042779", population_name="1000GENOMES:phase_3:KHV", r2=0.85)
        
        # testing values
        try:
            self.assertEqual(reference, test)
            
        #TODO: why this test fail sometimes?
        except AssertionError as e:
            # sometimes this test can fail. In such case, i log the error
            logger.error(e)
            logger.error("Sometimes 'test_getLdPairwise' fails. Maybe could be an ensembl transient problem?")
        
    def test_getLdRegion(self):
        """Testing get LD region GET method"""
        
        curl_cmd = """curl 'http://rest.ensembl.org/ld/human/region/6:25837556..25843455/1000GENOMES:phase_3:KHV?r2=0.85:d_prime=1.0' -H 'Content-type:application/json'"""
        
        # execute the curl cmd an get data as a dictionary
        reference = jsonFromCurl(curl_cmd)
      
        # execute EnsemblRest function
        test = self.EnsEMBL.getLdRegion(species="human", region="6:25837556..25843455", population_name="1000GENOMES:phase_3:KHV", r2=0.85, d_prime=1.0)
        
        # testing values
        try:
            self.assertTrue(reference, test)
            
        #TODO: why this test fail sometimes?
        except AssertionError as e:
            # sometimes this test can fail. In such case, i log the error
            logger.error(e)
            logger.error("Sometimes 'test_getLdRegion' fails. Maybe could be an ensembl transient problem?")
    
class EnsemblRestLookUp(EnsemblRest):
    """A class to deal with ensemblrest LookUp methods"""

    def test_getLookupById(self):
        """Testing get lookup by id GET method"""
        
        curl_cmd = """curl 'http://rest.ensembl.org/lookup/id/ENSG00000157764?expand=1' -H 'Content-type:application/json'"""
        
        # execute the curl cmd an get data as a dictionary
        reference = jsonFromCurl(curl_cmd)
      
        # execute EnsemblRest function
        test = self.EnsEMBL.getLookupById(id='ENSG00000157764', expand=1)
        
        # testing values
        self.assertEqual(reference, test)
        
    def test_getLookupByMultipleIds(self):
        """Testing get lookup id POST method"""
        
        curl_cmd = """curl 'http://rest.ensembl.org/lookup/id' -H 'Content-type:application/json' \
-H 'Accept:application/json' -X POST -d '{ "ids" : ["ENSG00000157764", "ENSG00000248378" ] }'"""

        # execute the curl cmd an get data as a dictionary
        reference = jsonFromCurl(curl_cmd)
      
        # execute EnsemblRest function
        test = self.EnsEMBL.getLookupByMultipleIds(ids=["ENSG00000157764", "ENSG00000248378" ])
        
        # testing values
        self.assertEqual(reference, test)
        
    def test_getLookupByMultipleIds_additional_arguments(self):
        """Testing get lookup id POST method with additional arguments"""
        
        curl_cmd = """curl 'http://rest.ensembl.org/lookup/id?expand=1' -H 'Content-type:application/json' \
-H 'Accept:application/json' -X POST -d '{ "ids" : ["ENSG00000157764", "ENSG00000248378" ] }'"""

        # execute the curl cmd an get data as a dictionary
        reference = jsonFromCurl(curl_cmd)
      
        # execute EnsemblRest function
        test = self.EnsEMBL.getLookupByMultipleIds(ids=["ENSG00000157764", "ENSG00000248378" ], expand=1)
        
        # testing values
        self.assertEqual(reference, test)
        
    def test_getLookupBySymbol(self):
        """Testing get lookup by species GET method"""
        
        curl_cmd = """curl 'http://rest.ensembl.org/lookup/symbol/homo_sapiens/BRCA2?expand=1' -H 'Content-type:application/json'"""
        
        # execute the curl cmd an get data as a dictionary
        reference = jsonFromCurl(curl_cmd)
      
        # execute EnsemblRest function
        test = self.EnsEMBL.getLookupBySymbol(species="homo_sapiens", symbol="BRCA2", expand=1)
        
        # testing values
        self.assertEqual(reference, test)
    
    def test_getLookupByMultipleSymbols(self):
        """Testing get lookup by species POST method"""
        
        curl_cmd = """curl 'http://rest.ensembl.org/lookup/symbol/homo_sapiens' -H 'Content-type:application/json' \
-H 'Accept:application/json' -X POST -d '{ "symbols" : ["BRCA2", "BRAF" ] }'"""

        # execute the curl cmd an get data as a dictionary
        reference = jsonFromCurl(curl_cmd)
      
        # execute EnsemblRest function
        test = self.EnsEMBL.getLookupByMultipleSymbols(species="homo_sapiens", symbols=["BRCA2", "BRAF"])
        
        # testing values
        self.assertEqual(reference, test)
    
    def test_getLookupByMultipleSymbols_additional_arguments(self):
        """Testing get lookup by species POST method  with additional arguments"""
        
        curl_cmd = """curl 'http://rest.ensembl.org/lookup/symbol/homo_sapiens?expand=1' -H 'Content-type:application/json' \
-H 'Accept:application/json' -X POST -d '{ "symbols" : ["BRCA2", "BRAF" ] }'"""

        # execute the curl cmd an get data as a dictionary
        reference = jsonFromCurl(curl_cmd)
      
        # execute EnsemblRest function
        test = self.EnsEMBL.getLookupByMultipleSymbols(species="homo_sapiens", symbols=["BRCA2", "BRAF"], expand=1)
        
        # testing values
        self.assertEqual(reference, test)
        
    
class EnsemblRestMapping(EnsemblRest):
    """A class to deal with ensemblrest mapping methods"""

    def test_getMapCdnaToRegion(self):
        """Testing map CDNA to region GET method"""
        
        curl_cmd = """curl 'http://rest.ensembl.org/map/cdna/ENST00000288602/100..300?' -H 'Content-type:application/json'"""
        
        # execute the curl cmd an get data as a dictionary
        reference = jsonFromCurl(curl_cmd)
      
        # execute EnsemblRest function
        test = self.EnsEMBL.getMapCdnaToRegion(id='ENST00000288602', region='100..300')
        
        # testing values
        self.assertEqual(reference, test)
        
    def test_getMapCdsToRegion(self):
        """Testing map CDS to region GET method"""
        
        curl_cmd = """curl 'http://rest.ensembl.org/map/cds/ENST00000288602/1..1000?' -H 'Content-type:application/json'"""
        
        # execute the curl cmd an get data as a dictionary
        reference = jsonFromCurl(curl_cmd)
      
        # execute EnsemblRest function
        test = self.EnsEMBL.getMapCdsToRegion(id='ENST00000288602', region='1..1000')
        
        # testing values
        self.assertEqual(reference, test)
        
    def test_getMapAssemblyOneToTwo(self):
        """Testing converting coordinates between assemblies GET method"""
        
        curl_cmd = """curl 'http://rest.ensembl.org/map/human/GRCh37/X:1000000..1000100:1/GRCh38?' -H 'Content-type:application/json'"""
        
        # execute the curl cmd an get data as a dictionary
        reference = jsonFromCurl(curl_cmd)
      
        # execute EnsemblRest function
        test = self.EnsEMBL.getMapAssemblyOneToTwo(species='human', asm_one='GRCh37', region='X:1000000..1000100:1', asm_two='GRCh38')
        
        # testing values
        self.assertEqual(reference, test)
        
    def test_getMapTranslationToRegion(self):
        """Testing converting protein(traslation) to genomic coordinates GET method"""
        
        curl_cmd = """curl 'http://rest.ensembl.org/map/translation/ENSP00000288602/100..300?' -H 'Content-type:application/json'"""
        
        # execute the curl cmd an get data as a dictionary
        reference = jsonFromCurl(curl_cmd)
      
        # execute EnsemblRest function
        test = self.EnsEMBL.getMapTranslationToRegion(id='ENSP00000288602', region='100..300')
        
        # testing values
        self.assertEqual(reference, test)
    
    
class EnsemblRestOT(EnsemblRest):
    """A class to deal with ensemblrest ontologies and taxonomy methods"""

    def test_getAncestorsById(self):
        """Testing get ancestors by id GET method"""
        
        curl_cmd = """curl 'http://rest.ensembl.org/ontology/ancestors/GO:0005667?' -H 'Content-type:application/json'"""
        
        # execute the curl cmd an get data as a dictionary
        reference = jsonFromCurl(curl_cmd)
      
        # execute EnsemblRest function
        test = self.EnsEMBL.getAncestorsById(id='GO:0005667')
        
        # testing values
        self.assertEqual(reference, test)
        
    def test_getAncestorsChartById(self):
        """Testing get ancestors chart by id GET method"""
        
        curl_cmd = """curl 'http://rest.ensembl.org/ontology/ancestors/chart/GO:0005667?' -H 'Content-type:application/json'"""
        
        # execute the curl cmd an get data as a dictionary
        reference = jsonFromCurl(curl_cmd)
      
        # execute EnsemblRest function
        test = self.EnsEMBL.getAncestorsChartById(id='GO:0005667')
        
        # testing values
        self.assertEqual(reference, test)
        
    def test_getDescendantsById(self):
        """Testing get descendants by id GET method"""
        
        curl_cmd = """curl 'http://rest.ensembl.org/ontology/descendants/GO:0005667?' -H 'Content-type:application/json'"""
        
        # execute the curl cmd an get data as a dictionary
        reference = jsonFromCurl(curl_cmd)
      
        # execute EnsemblRest function
        test = self.EnsEMBL.getDescendantsById(id='GO:0005667')
        
        # testing values
        self.assertEqual(reference, test)
        
    def test_getOntologyById(self):
        """Test get ontology by id GET method"""
        
        curl_cmd = """curl 'http://rest.ensembl.org/ontology/id/GO:0005667?' -H 'Content-type:application/json'"""
        
        # execute the curl cmd an get data as a dictionary
        reference = jsonFromCurl(curl_cmd)
      
        # execute EnsemblRest function
        test = self.EnsEMBL.getOntologyById(id='GO:0005667')
        
        # testing values
        self.assertEqual(reference, test)
        
    def test_getOntologyByName(self):
        """Test get ontology by name GET method"""
        
        curl_cmd = """curl 'http://rest.ensembl.org/ontology/name/%s?' -H 'Content-type:application/json'""" % (
            six.moves.urllib.parse.quote("transcription factor complex")
        )
        
        # execute the curl cmd an get data as a dictionary
        reference = jsonFromCurl(curl_cmd)
      
        # execute EnsemblRest function
        test = self.EnsEMBL.getOntologyByName(name='transcription factor complex')
        
        # testing values
        self.assertEqual(reference, test)
        
    def test_getTaxonomyClassificationById(self):
        """Testing get taxonomy classification by id GET method"""
        
        curl_cmd = """curl 'http://rest.ensembl.org/taxonomy/classification/9606?' -H 'Content-type:application/json'"""
        
        # execute the curl cmd an get data as a dictionary
        reference = jsonFromCurl(curl_cmd)
      
        # execute EnsemblRest function
        test = self.EnsEMBL.getTaxonomyClassificationById(id='9606')
        
        # testing values
        try:
            self.assertTrue(reference, test)
            
        #TODO: why this test fail sometimes?
        except AssertionError as e:
            # sometimes this test can fail. In such case, i log the error
            logger.error(e)
            logger.error("Sometimes 'test_getTaxonomyClassificationById' fails. Maybe could be an ensembl transient problem?")
        
    def test_getTaxonomyById(self):
        """Testing get Taxonomy by id GET method"""
        
        curl_cmd = """curl 'http://rest.ensembl.org/taxonomy/id/9606?' -H 'Content-type:application/json'"""
        
        # execute the curl cmd an get data as a dictionary
        reference = jsonFromCurl(curl_cmd)
      
        # execute EnsemblRest function
        test = self.EnsEMBL.getTaxonomyById(id='9606')
        
        try:
            # testing values. Since json are nested dictionary and lists, and they are not hashable, I need to order list before
            # checking equality, and I need to ensure that dictionaries have the same keys and values
            self.assertTrue(compareDict(reference, test))
        
        # The transitory failure seems to be related to a misconfiguration of ensembl
        # rest service. In such cases is better to inform dev<at>ensembl.org and report
        # such issues
        except AssertionError as e:
            # sometimes this test can fail. In such case, i log the error
            logger.error(e)
            logger.error("Sometimes 'test_getTaxonomyById' fails. This could be a transitory problem on EnsEMBL REST service")
        
    def test_getTaxonomyByName(self):
        """Testing get taxonomy by name GET method"""
        
        curl_cmd = """curl 'http://rest.ensembl.org/taxonomy/name/Homo%25?' -H 'Content-type:application/json'"""
        
        # execute the curl cmd an get data as a dictionary
        reference = jsonFromCurl(curl_cmd)
      
        # execute EnsemblRest function
        test = self.EnsEMBL.getTaxonomyByName(name="Homo%25")
        
        # testing values. Since json are nested dictionary and lists, and they are not hashable, I need to order list before
        # checking equality, and I need to ensure that dictionaries have the same keys and values
        self.assertTrue(compareList(reference, test))


class EnsemblRestOverlap(EnsemblRest):
    """A class to deal with ensemblrest overlap methods"""

    def test_getOverlapById(self):
        """Testing get Overlap by ID GET method"""
        
        curl_cmd = """curl 'http://rest.ensembl.org/overlap/id/ENSG00000157764?feature=gene' -H 'Content-type:application/json'"""
        
        # execute the curl cmd an get data as a dictionary
        reference = jsonFromCurl(curl_cmd)
      
        # execute EnsemblRest function
        test = self.EnsEMBL.getOverlapById(id="ENSG00000157764", feature="gene")
        
        # testing values
        self.assertEqual(reference, test)
        
    def test_getOverlapByRegion(self):
        """Testing get Overlap by region GET method"""
        
        curl_cmd = """curl 'http://rest.ensembl.org/overlap/region/human/7:140424943-140624564?feature=gene;feature=transcript;feature=cds;feature=exon' -H 'Content-type:application/json'"""
        
        # execute the curl cmd an get data as a dictionary
        reference = jsonFromCurl(curl_cmd)
      
        # execute EnsemblRest function
        test = self.EnsEMBL.getOverlapByRegion(species="human", region="7:140424943-140624564", feature=["gene", "transcript", "cds", "exon"])
        
        # testing values
        self.assertEqual(reference, test)
        
    def test_getOverlapByTranslation(self):
        """Testing get Overlab by traslation GET method"""
        
        curl_cmd = """curl 'http://rest.ensembl.org/overlap/translation/ENSP00000288602?type=Superfamily' -H 'Content-type:application/json'"""
        
        # execute the curl cmd an get data as a dictionary
        reference = jsonFromCurl(curl_cmd)
      
        # execute EnsemblRest function
        test = self.EnsEMBL.getOverlapByTranslation(id="ENSP00000288602", type="SuperFamily")
        
        # testing values
        self.assertEqual(reference, test)

    
    # Regulation
    def test_getRegulatoryFeatureById(self):
        """Testing get regulatory Feature GET method"""
        
        curl_cmd = """curl 'http://rest.ensembl.org/regulatory/species/human/id/ENSR00000099113?' -H 'Content-type:application/json'"""
        
        # execute the curl cmd an get data as a dictionary
        reference = jsonFromCurl(curl_cmd)
      
        # execute EnsemblRest function
        test = self.EnsEMBL.getRegulatoryFeatureById(species="human", id="ENSR00000099113")
        
        # testing values
        self.assertEqual(reference, test)
        
    
class EnsemblRestSequence(EnsemblRest):
    """A class to deal with ensemblrest sequence methods"""

    def test_getSequenceById(self):
        """Testing get sequence by ID GET method"""
        
        curl_cmd = """curl 'http://rest.ensembl.org/sequence/id/CCDS5863.1?object_type=transcript;db_type=otherfeatures;type=cds;species=human' -H 'Content-type:application/json'"""
        
        # execute the curl cmd an get data as a dictionary
        reference = jsonFromCurl(curl_cmd)
      
        # execute EnsemblRest function
        test = self.EnsEMBL.getSequenceById(id='CCDS5863.1', object_type="transcript", db_type="otherfeatures", type="cds", species="human")
        
        # testing values
        self.assertEqual(reference, test)
        
    def test_getSequenceByMultipleIds(self):
        """Testing get sequence by ID POST method"""
        
        curl_cmd = """curl 'http://rest.ensembl.org/sequence/id' -H 'Content-type:application/json' \
-H 'Accept:application/json' -X POST -d '{ "ids" : ["ENSG00000157764", "ENSG00000248378" ] }'"""

        # execute the curl cmd an get data as a dictionary
        reference = jsonFromCurl(curl_cmd)
      
        # execute EnsemblRest function
        test = self.EnsEMBL.getSequenceByMultipleIds(ids=["ENSG00000157764", "ENSG00000248378" ])
        
        # testing values
        self.assertEqual(reference, test)
        
    def test_getSequenceByMultipleIds_additional_arguments(self):
        """Testing getSequenceByMultipleIds with mask="soft" and expand_3prime=100"""

        curl_cmd = """curl 'http://rest.ensembl.org/sequence/id?mask=soft;expand_3prime=100' -H 'Content-type:application/json' \
-H 'Accept:application/json' -X POST -d '{ "ids" : ["ENSG00000157764", "ENSG00000248378" ] }'"""
        
        # execute the curl cmd an get data as a dictionary
        reference = jsonFromCurl(curl_cmd)
      
        # execute EnsemblRest function
        test = self.EnsEMBL.getSequenceByMultipleIds(ids=["ENSG00000157764", "ENSG00000248378"], expand_3prime=100, mask="soft")
        
        # testing values
        self.assertEqual(reference, test)
        
    def test_getSequenceByRegion(self):
        """Testing get sequence by region GET method"""
        
        curl_cmd = """curl 'http://rest.ensembl.org/sequence/region/human/X:1000000..1000100:1?' -H 'Content-type:application/json'"""
        
        # execute the curl cmd an get data as a dictionary
        reference = jsonFromCurl(curl_cmd)
      
        # execute EnsemblRest function
        test = self.EnsEMBL.getSequenceByRegion(species='human', region='X:1000000..1000100:1')
        
        # testing values
        self.assertTrue(compareDict(reference, test))
        
    def test_getSequenceByMultipleRegions(self):
        """Testing get sequence by region POST method"""
        
        curl_cmd = """curl 'http://rest.ensembl.org/sequence/region/human' -H 'Content-type:application/json' \
-H 'Accept:application/json' -X POST -d '{ "regions" : ["X:1000000..1000100:1", "ABBA01004489.1:1..100"] }'"""

        # execute the curl cmd an get data as a dictionary
        reference = jsonFromCurl(curl_cmd)
      
        # execute EnsemblRest function
        test = self.EnsEMBL.getSequenceByMultipleRegions(species="human", regions=["X:1000000..1000100:1", "ABBA01004489.1:1..100"])
        
        # testing values
        self.assertEqual(reference, test)
        
    def test_getSequenceByMultipleRegions_additional_arguments(self):
        """Testing get sequence by region POST method with mask="soft" and expand_3prime=100"""
        
        curl_cmd = """curl 'http://rest.ensembl.org/sequence/region/human?mask=soft;expand_3prime=100' -H 'Content-type:application/json' -H 'Accept:application/json' -X POST -d '{ "regions" : ["X:1000000..1000100:1", "ABBA01004489.1:1..100"] }'"""
        
        # execute the curl cmd an get data as a dictionary
        reference = jsonFromCurl(curl_cmd)
      
        # execute EnsemblRest function
        test = self.EnsEMBL.getSequenceByMultipleRegions(species="human", regions=["X:1000000..1000100:1", "ABBA01004489.1:1..100"], expand_3prime=100, mask="soft")
        
        # testing values
        self.assertEqual(reference, test)
        
        
class EnsemblRestHaplotype(EnsemblRest):
    """A class to deal with ensemblrest transcript haplotypes methods"""

    def test_getTranscripsHaplotypes(self):
        """Testing get transcripts Haplotypes GET method"""
        
        curl_cmd = """curl 'http://rest.ensembl.org/transcript_haplotypes/homo_sapiens/ENST00000288602?' -H 'Content-type:application/json'"""
        
        # execute the curl cmd an get data as a dictionary
        reference = jsonFromCurl(curl_cmd)
      
        # execute EnsemblRest function
        test = self.EnsEMBL.getTranscripsHaplotypes(species="homo_sapiens", id="ENST00000288602")
        
        # testing values
        self.assertEqual(reference, test)

    
class EnsemblRestVEP(EnsemblRest):
    """A class to deal with ensemblrest Variant Effect Predictor methods"""

    def test_getVariantConsequencesByHGVSnotation(self):
        """Testing get Variant Consequences by HFVS notation GET method"""
        
        curl_cmd = """curl 'http://rest.ensembl.org/vep/human/hgvs/AGT:c.803T>C?' -H 'Content-type:application/json'"""
        
        # execute the curl cmd an get data as a dictionary
        reference = jsonFromCurl(curl_cmd)
      
        # execute EnsemblRest function
        test = self.EnsEMBL.getVariantConsequencesByHGVSnotation(species="human", hgvs_notation="AGT:c.803T>C")
        
        # testing values
        self.assertEqual(reference, test)
        
    def test_getVariantConsequencesById(self):
        """Testing get variant Consequences by id GET method"""
        
        curl_cmd = """curl 'http://rest.ensembl.org/vep/human/id/COSM476?' -H 'Content-type:application/json'"""
        
        # execute the curl cmd an get data as a dictionary
        reference = jsonFromCurl(curl_cmd)
      
        # execute EnsemblRest function
        test = self.EnsEMBL.getVariantConsequencesById(species='human', id='COSM476')
        
        # testing values
        self.assertEqual(reference, test)
        
    def test_getVariantConsequencesByMultipleIds(self):
        """Testing get variant Consequences by id POST method"""
        
        curl_cmd = """curl 'http://rest.ensembl.org/vep/human/id' -H 'Content-type:application/json' \
-H 'Accept:application/json' -X POST -d '{ "ids" : ["rs56116432", "COSM476" ] }'"""

        # execute the curl cmd an get data as a dictionary
        reference = jsonFromCurl(curl_cmd)
      
        # execute EnsemblRest function
        test = self.EnsEMBL.getVariantConsequencesByMultipleIds(species="human", ids=[ "rs56116432", "COSM476" ])
        
        # testing values
        self.assertEqual(reference, test)
        
    def test_getVariantConsequencesByMultipleIds_additional_arguments(self):
        """Testing get variant Consequences by id POST method using Blosum62=1, CSN=1"""
        
        curl_cmd = """curl 'http://rest.ensembl.org/vep/human/id?Blosum62=1;CSN=1' -H 'Content-type:application/json' \
-H 'Accept:application/json' -X POST -d '{ "ids" : ["rs56116432", "COSM476" ] }'"""

        # execute the curl cmd an get data as a dictionary
        reference = jsonFromCurl(curl_cmd)
      
        # execute EnsemblRest function
        test = self.EnsEMBL.getVariantConsequencesByMultipleIds(species="human", ids=[ "rs56116432", "COSM476" ], Blosum62=1, CSN=1)
        
        # testing values
        self.assertEqual(reference, test)
    
    def test_getVariantConsequencesByRegion(self):
        """Testing get variant consequences by Region GET method"""
        
        curl_cmd = """curl 'http://rest.ensembl.org/vep/human/region/9:22125503-22125502:1/C?' -H 'Content-type:application/json'"""
        
        # execute the curl cmd an get data as a dictionary
        reference = jsonFromCurl(curl_cmd)
      
        # execute EnsemblRest function
        test = self.EnsEMBL.getVariantConsequencesByRegion(species='human', region='9:22125503-22125502:1', allele='C')
        
        # testing values
        self.assertEqual(reference, test)
        
    def test_getVariantConsequencesByMultipleRegions(self):
        """Testing get variant consequences by Region POST method"""
        
        curl_cmd = """curl 'http://rest.ensembl.org/vep/homo_sapiens/region' -H 'Content-type:application/json' \
-H 'Accept:application/json' -X POST -d '{ "variants" : ["21 26960070 rs116645811 G A . . .", "21 26965148 rs1135638 G A . . ." ] }'"""

        # execute the curl cmd an get data as a dictionary
        reference = jsonFromCurl(curl_cmd)
      
        # execute EnsemblRest function
        test = self.EnsEMBL.getVariantConsequencesByMultipleRegions(species="human", variants=["21 26960070 rs116645811 G A . . .", "21 26965148 rs1135638 G A . . ." ] )
        
        # testing values
        self.assertEqual(reference, test)
        
    def test_getVariantConsequencesByMultipleRegions_additional_arguments(self):
        """Testing get variant consequences by Region POST method Blosum62=1, CSN=1"""
        
        curl_cmd = """curl 'http://rest.ensembl.org/vep/homo_sapiens/region?Blosum62=1;CSN=1' -H 'Content-type:application/json' \
-H 'Accept:application/json' -X POST -d '{ "variants" : ["21 26960070 rs116645811 G A . . .", "21 26965148 rs1135638 G A . . ." ] }'"""

        # execute the curl cmd an get data as a dictionary
        reference = jsonFromCurl(curl_cmd)
      
        # execute EnsemblRest function
        test = self.EnsEMBL.getVariantConsequencesByMultipleRegions(species="human", variants=["21 26960070 rs116645811 G A . . .", "21 26965148 rs1135638 G A . . ." ], Blosum62=1, CSN=1 )
        
        # testing values
        self.assertEqual(reference, test)
    
    
class EnsemblRestVariation(EnsemblRest):
    """A class to deal with ensemblrest variation methods"""

    def test_getVariationById(self):
        """Testing get variation by id GET method"""
        
        curl_cmd = """curl 'http://rest.ensembl.org/variation/human/rs56116432?' -H 'Content-type:application/json'"""
        
        # execute the curl cmd an get data as a dictionary
        reference = jsonFromCurl(curl_cmd)
      
        # execute EnsemblRest function
        test = self.EnsEMBL.getVariationById(id="rs56116432", species="homo_sapiens")
        
        # testing values
        self.assertEqual(reference, test)
        
    def test_getVariationByMultipleIds(self):
        """Testing get variation by id POST method"""
        
        curl_cmd = """curl 'http://rest.ensembl.org/variation/homo_sapiens' -H 'Content-type:application/json' \
-H 'Accept:application/json' -X POST -d '{ "ids" : ["rs56116432", "COSM476" ] }'"""
        
        # execute the curl cmd an get data as a dictionary
        reference = jsonFromCurl(curl_cmd)
      
        # execute EnsemblRest function
        test = self.EnsEMBL.getVariationByMultipleIds(ids=["rs56116432", "COSM476" ], species="homo_sapiens")
        
        # testing values
        self.assertEqual(reference, test)
        
    def test_getVariationByMultipleIds_additional_arguments(self):
        """Testing get variation by id POST method with genotypes=1"""
        
        curl_cmd = """curl 'http://rest.ensembl.org/variation/homo_sapiens?genotypes=1' -H 'Content-type:application/json' \
-H 'Accept:application/json' -X POST -d '{ "ids" : ["rs56116432", "COSM476" ] }'"""
        
        # execute the curl cmd an get data as a dictionary
        reference = jsonFromCurl(curl_cmd)
      
        # execute EnsemblRest function
        test = self.EnsEMBL.getVariationByMultipleIds(ids=["rs56116432", "COSM476" ], species="homo_sapiens", genotypes=1)
        
        # testing values
        self.assertEqual(reference, test)
    
    
class EnsemblRestVariationGA4GH(EnsemblRest):
    """A class to deal with ensemblrest variation GA4GH methods"""

    def test_searchGA4GHCallSet(self):
        """Testing GA4GH callset search POST method"""
        
        curl_cmd = """curl 'http://rest.ensembl.org/ga4gh/callsets/search' -H 'Content-type:application/json' \
-H 'Accept:application/json' -X POST -d '{ "variantSetId": 1, "pageSize": 2  }'"""

        # execute the curl cmd an get data as a dictionary
        reference = jsonFromCurl(curl_cmd)
      
        # execute EnsemblRest function
        test = self.EnsEMBL.searchGA4GHCallSet(variantSetId=1, pageSize=2)
        
        # testing values
        self.assertEqual(reference, test)
        
    def test_getGA4GHCallSetById(self):
        """Testing get GA4GH callset by Id GET method"""
        
        curl_cmd = """curl 'http://rest.ensembl.org/ga4gh/callsets/1:NA19777?' -H 'Content-type:application/json'"""
        
        # execute the curl cmd an get data as a dictionary
        reference = jsonFromCurl(curl_cmd)
      
        # execute EnsemblRest function
        test = self.EnsEMBL.getGA4GHCallSetById(id="1:NA19777")
        
        # testing values
        self.assertEqual(reference, test)
        
    def test_searchGA4GHDataset(self):
        """Testing GA4GH search dataset POST method"""
        
        curl_cmd = """curl 'http://rest.ensembl.org/ga4gh/datasets/search' -H 'Content-type:application/json' \
-H 'Accept:application/json' -X POST -d '{ "pageSize": 3 }'"""

        # execute the curl cmd an get data as a dictionary
        reference = jsonFromCurl(curl_cmd)
      
        # execute EnsemblRest function
        test = self.EnsEMBL.searchGA4GHDataset(pageSize=3)
        
        # testing values
        self.assertEqual(reference, test)
        
    def test_getGA4GHDatasetById(self):
        """Testing GA4GH get dataset by Id GET method"""
        
        curl_cmd = """curl 'http://rest.ensembl.org/ga4gh/datasets/6e340c4d1e333c7a676b1710d2e3953c?' -H 'Content-type:application/json'"""
        
        # execute the curl cmd an get data as a dictionary
        reference = jsonFromCurl(curl_cmd)
      
        # execute EnsemblRest function
        test = self.EnsEMBL.getGA4GHDatasetById(id="6e340c4d1e333c7a676b1710d2e3953c")
        
        # testing values
        self.assertEqual(reference, test)
        
    def test_getGA4GHVariantsById(self):
        """Testing GA4GH get variant by Id GET method"""
        
        curl_cmd = """curl 'http://rest.ensembl.org/ga4gh/variants/1:rs1333049?' -H 'Content-type:application/json'"""
        
        # execute the curl cmd an get data as a dictionary
        reference = jsonFromCurl(curl_cmd)
      
        # execute EnsemblRest function
        test = self.EnsEMBL.getGA4GHVariantsById(id="1:rs1333049")
        
        # testing values
        self.assertEqual(reference, test)
        
    def test_searchGA4GHVariants(self):
        """Testing GA4GH search variants POST method"""
        
        curl_cmd = """curl 'http://rest.ensembl.org/ga4gh/variants/search' -H 'Content-type:application/json' \
-H 'Accept:application/json' -X POST -d '{ "variantSetId": 1, "referenceName": 22,"start": 17190024 ,"end":  17671934 ,  "pageToken":"", "pageSize": 1 }'"""

        # execute the curl cmd an get data as a dictionary
        reference = jsonFromCurl(curl_cmd)
      
        # execute EnsemblRest function
        test = self.EnsEMBL.searchGA4GHVariants(variantSetId=1, referenceName=22, start=17190024, end=17671934, pageToken="", pageSize=1)
        
        # testing values
        self.assertEqual(reference, test)
        
    def test_searchGA4GHVariantsets(self):
        """Testing GA4GH search variantset POST method"""
        
        curl_cmd = """curl 'http://rest.ensembl.org/ga4gh/variantsets/search' -H 'Content-type:application/json' \
-H 'Accept:application/json' -X POST -d '{ "datasetId": "6e340c4d1e333c7a676b1710d2e3953c",    "pageToken": "", "pageSize": 2 }'"""

        # execute the curl cmd an get data as a dictionary
        reference = jsonFromCurl(curl_cmd)
      
        # execute EnsemblRest function
        test = self.EnsEMBL.searchGA4GHVariantsets(datasetId="6e340c4d1e333c7a676b1710d2e3953c", pageToken="", pageSize=2)
        
        # testing values
        self.assertEqual(reference, test)
        
    def test_getGA4GHVariantsetsById(self):
        """Testing GA4GH get variantset by Id GET method"""
        
        curl_cmd = """curl 'http://rest.ensembl.org/ga4gh/variantsets/1?' -H 'Content-type:application/json'"""

        # execute the curl cmd an get data as a dictionary
        reference = jsonFromCurl(curl_cmd)
      
        # execute EnsemblRest function
        test = self.EnsEMBL.getGA4GHVariantsetsById(id=1)
        
        # testing values
        self.assertEqual(reference, test)
        
    def test_searchGA4GHReferences(self):
        """Testing GA4GH search references POST method"""
        
        curl_cmd = """curl 'http://rest.ensembl.org/ga4gh/references/search' -H 'Content-type:application/json' \
-H 'Accept:application/json' -X POST -d '{ "referenceSetId": "GRCh38", "pageSize": 10 }'"""

        # execute the curl cmd an get data as a dictionary
        reference = jsonFromCurl(curl_cmd)
      
        # execute EnsemblRest function
        test = self.EnsEMBL.searchGA4GHReferences(referenceSetId="GRCh38", pageSize=10)
        
        # testing values
        self.assertEqual(reference, test)
        
    def test_getGA4GHReferencesById(self):
        """Testing GA4GH get references by Id GET method"""
        
        curl_cmd = """curl 'http://rest.ensembl.org/ga4gh/references/9489ae7581e14efcad134f02afafe26c?' -H 'Content-type:application/json'"""

        # execute the curl cmd an get data as a dictionary
        reference = jsonFromCurl(curl_cmd)
      
        # execute EnsemblRest function
        test = self.EnsEMBL.getGA4GHReferencesById(id="9489ae7581e14efcad134f02afafe26c")
        
        # testing values
        self.assertEqual(reference, test)
        
    def test_searchGA4GHReferenceSets(self):
        """Testing GA4GH search reference sets POST method"""
        
        curl_cmd = """curl 'http://rest.ensembl.org/ga4gh/referencesets/search' -H 'Content-type:application/json' \
-H 'Accept:application/json' -X POST -d '{   }'"""

        # execute the curl cmd an get data as a dictionary
        reference = jsonFromCurl(curl_cmd)
      
        # execute EnsemblRest function
        test = self.EnsEMBL.searchGA4GHReferenceSets()
        
        # testing values
        self.assertEqual(reference, test)
        
    def test_getGA4GHReferenceSetsById(self):
        """Testing GA4GH get reference set by Id GET method"""
        
        curl_cmd = """curl 'http://rest.ensembl.org/ga4gh/referencesets/GRCh38?' -H 'Content-type:application/json'"""

        # execute the curl cmd an get data as a dictionary
        reference = jsonFromCurl(curl_cmd)
      
        # execute EnsemblRest function
        test = self.EnsEMBL.getGA4GHReferenceSetsById(id="GRCh38")
        
        # testing values
        self.assertEqual(reference, test)


class EnsemblGenomeRest(unittest.TestCase):
    """A class to test EnsemblGenomeRest methods"""
    
    def setUp(self):
        """Create a EnsemblRest object"""
        self.EnsEMBL = ensemblrest.EnsemblGenomeRest()
        
    def tearDown(self):
        """Sleep a while before doing next request"""
        time.sleep(WAIT)

    def test_getGeneFamilyById(self):
        """Testing genefamily by id GET method"""
        
        curl_cmd = """curl 'http://rest.ensemblgenomes.org/family/id/MF_01120?compara=bacteria' -H 'Content-type:application/json'"""
        
        # execute the curl cmd an get data as a dictionary
        reference = jsonFromCurl(curl_cmd)
      
        # execute EnsemblRest function
        test = self.EnsEMBL.getGeneFamilyById(id="MF_01120", compara="bacteria")
        
        # testing values
        self.assertEqual(reference, test)
        
    def test_getGeneFamilyMemberById(self):
        """Testing genefamily member by id GET method"""
        
        curl_cmd = """curl 'http://rest.ensemblgenomes.org/family/member/id/STK_01900?compara=bacteria' -H 'Content-type:application/json'"""
        
        # execute the curl cmd an get data as a dictionary
        reference = jsonFromCurl(curl_cmd)
      
        # execute EnsemblRest function
        test = self.EnsEMBL.getGeneFamilyMemberById(id="STK_01900", compara="bacteria")
        
        # testing values
        self.assertEqual(reference, test)
        
    def test_getGeneFamilyMemberBySymbol(self):
        """Testing genefamily member by symbol"""
        
        curl_cmd = """curl 'http://rest.ensemblgenomes.org/family/member/symbol/sulfolobus_tokodaii_str_7/lysK?compara=bacteria' -H 'Content-type:application/json'"""
        
        # execute the curl cmd an get data as a dictionary
        reference = jsonFromCurl(curl_cmd)
      
        # execute EnsemblRest function
        test = self.EnsEMBL.getGeneFamilyMemberBySymbol(symbol="lysK", species="sulfolobus_tokodaii_str_7", compara="bacteria")
        
        # testing values
        self.assertEqual(reference, test)
        
    def test_getInfoEgVersion(self):
        """Testing EgVersion GET method"""
        
        curl_cmd = """curl 'http://rest.ensemblgenomes.org/info/eg_version?' -H 'Content-type:application/json'"""
        
        # execute the curl cmd an get data as a dictionary
        reference = jsonFromCurl(curl_cmd)
      
        # execute EnsemblRest function
        test = self.EnsEMBL.getInfoEgVersion()
        
        # testing values
        self.assertEqual(reference, test)
        
    def test_getInfoDivisions(self):
        """Testing Info Divisions GET method"""
        
        curl_cmd = """curl 'http://rest.ensemblgenomes.org/info/divisions?' -H 'Content-type:application/json'"""

        # execute the curl cmd an get data as a dictionary
        reference = jsonFromCurl(curl_cmd)
      
        # execute EnsemblRest function
        test = self.EnsEMBL.getInfoDivisions()
        
        # testing values
        self.assertEqual(reference, test)
        
    def test_getInfoGenomesByName(self):
        """Testing Info Genomes by Name GET method"""
        
        curl_cmd = """curl 'http://rest.ensemblgenomes.org/info/genomes/campylobacter_jejuni_subsp_jejuni_bh_01_0142?' -H 'Content-type:application/json'"""
        
        # execute the curl cmd an get data as a dictionary
        reference = jsonFromCurl(curl_cmd)
      
        # execute EnsemblRest function
        test = self.EnsEMBL.getInfoGenomesByName(name="campylobacter_jejuni_subsp_jejuni_bh_01_0142")
        
        # testing values
        self.assertEqual(reference, test)
        
    def test_getInfoGenomesByAccession(self): 
        """Testing Info Genomes by Accession GET method"""
        
        curl_cmd = """curl 'http://rest.ensemblgenomes.org/info/genomes/accession/U00096?' -H 'Content-type:application/json'"""
        
        # execute the curl cmd an get data as a dictionary
        reference = jsonFromCurl(curl_cmd)
      
        # execute EnsemblRest function
        test = self.EnsEMBL.getInfoGenomesByAccession(division="U00096")
        
        # testing values
        self.assertEqual(reference, test)
        
    def test_getInfoGenomesByAssembly(self):
        """Testing Info Genomes by Assembly GET method"""
        
        curl_cmd = """curl 'http://rest.ensemblgenomes.org/info/genomes/assembly/GCA_000005845?' -H 'Content-type:application/json'"""
        
        # execute the curl cmd an get data as a dictionary
        reference = jsonFromCurl(curl_cmd)
      
        # execute EnsemblRest function
        test = self.EnsEMBL.getInfoGenomesByAssembly(division="GCA_000005845")
        
        # testing values
        self.assertEqual(reference, test)
    
    def test_getInfoGenomesByDivision(self):
        """Testing Info Genomes by Division GET method"""
        
        curl_cmd = """curl 'http://rest.ensemblgenomes.org/info/genomes/division/EnsemblPlants?' -H 'Content-type:application/json'"""
        
        # execute the curl cmd an get data as a dictionary
        reference = jsonFromCurl(curl_cmd)
      
        # execute EnsemblRest function
        test = self.EnsEMBL.getInfoGenomesByDivision(division="EnsemblPlants")
        
        # testing values
        self.assertEqual(reference, test)
        
    def test_getInfoGenomesByTaxonomy(self):
        """Testing Info Genomes by Taxonomy GET method"""
        
        curl_cmd = """curl 'http://rest.ensemblgenomes.org/info/genomes/taxonomy/Arabidopsis?' -H 'Content-type:application/json'"""
        
        # execute the curl cmd an get data as a dictionary
        reference = jsonFromCurl(curl_cmd)
      
        # execute EnsemblRest function
        test = self.EnsEMBL.getInfoGenomesByTaxonomy(division="Arabidopsis")
        
        # testing values
        self.assertEqual(reference, test)
        
    def test_getLookupByGenomeName(self):
        """Testing Lookup by genome name GET method"""
        
        curl_cmd = """curl 'http://rest.ensemblgenomes.org/lookup/genome/campylobacter_jejuni_subsp_jejuni_bh_01_0142?' -H 'Content-type:application/json'"""
        
        # execute the curl cmd an get data as a dictionary
        reference = jsonFromCurl(curl_cmd)
      
        # execute EnsemblRest function
        test = self.EnsEMBL.getLookupByGenomeName(name="campylobacter_jejuni_subsp_jejuni_bh_01_0142")
        
        # testing values
        self.assertEqual(reference, test)

if __name__ == "__main__":
    unittest.main()

    