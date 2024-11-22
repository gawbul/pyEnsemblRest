import json
import logging
import re
import shlex
import subprocess
import time
import unittest
import urllib.parse
from typing import Any

import pytest
from requests import Response

import pyensemblrest
from pyensemblrest.ensemblrest import FakeResponse, ensembl_user_agent

# logger instance
logger = logging.getLogger(__name__)

# create console handler and set level to debug. NullHandler to put all into /dev/null
# ch = logging.NullHandler()

# This console handle write all logging to and opened strem. sys.stderr is the default
ch = logging.StreamHandler()

# Set the level for this handler
ch.setLevel(logging.DEBUG)

# create formatter
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

# add formatter to ch
ch.setFormatter(formatter)

# add ch to logger
logger.addHandler(ch)

# Wait some time before next request
WAIT = 1

# Sometimes curl fails
MAX_RETRIES = 5

# curl timeouts
TIMEOUT = 60


def launch(cmd: str) -> str:
    """Calling a cmd with subprocess"""

    # setting curl timeouts
    pattern = re.compile("curl")
    repl = "curl --connect-timeout %s --max-time %s" % (TIMEOUT, TIMEOUT * 2)

    # Setting curl options
    cmd = re.sub(pattern, repl, cmd)

    logger.debug("Executing: %s" % (cmd))

    args = shlex.split(cmd)
    p = subprocess.Popen(
        args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True
    )
    stdout, stderr = p.communicate()

    if len(stderr) > 0:
        logger.debug(stderr)

    # debug
    # logger.debug("Got: %s" % (stdout))

    return stdout


def jsonFromCurl(curl_cmd: str) -> dict[Any, Any] | None:
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
            time.sleep(WAIT * 10)

            # next request
            continue

        if isinstance(data, dict):
            if "error" in data:
                logger.warning("Curl command failed: %s" % (data["error"]))
                time.sleep(WAIT * 10)

                # next request
                continue

        # If I arrive here, I assume that curl went well
        break

    return data


def _genericCMP(v1: Any, v2: Any) -> bool:
    """Check ensembl complex elements"""

    logger.debug("Check %s == %s" % (v1, v2))

    # check that types are the same
    if type(v1) is not type(v2):
        return False
    elif isinstance(v1, dict):
        # call comparedict
        if compareDict(v1, v2) is False:
            return False
    elif isinstance(v1, list):
        # call comparedict
        if compareList(v1, v2) is False:
            return False
    elif isinstance(v1, (str, float, int)):
        if v1 != v2:
            return False
    else:
        logger.error("%s <> %s" % (v1, v2))
        logger.critical("Case not implemented: type: %s" % (type(v1)))

    # default value
    return True


# A function to evaluate if two python complex dictionaries are the same
def compareDict(d1: dict[Any, Any], d2: dict[Any, Any]) -> bool:
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

    # now I have to check values for each key value
    for k in k1:
        # get values
        v1 = d1[k]
        v2 = d2[k]

        if v1 == v2:
            continue

        # the species key may differ in some cases: ex: Tgut-Mgal-Ggal[3] <> Ggal-Mgal-Tgut[3]
        if k in ["species", "tree"] and isinstance(v1, str) and isinstance(v2, str):
            pattern = re.compile(r"([\w]+)-?(?:\[\d\])?")

            # override values
            v1 = re.findall(pattern, v1)
            v2 = re.findall(pattern, v2)

        # check if elements are the same
        if _genericCMP(v1, v2) is False:
            return False

    # if I arrive here:
    return True


def compareList(l1: list[Any], l2: list[Any]) -> bool:
    """A function to evaluate if two python complex lists are the same"""

    # check if lists are equal
    if l1 == l2:
        return True

    # check if lengths are equal
    if len(l1) != len(l2):
        return False

    # I cannot use set nor collections.Count, since elements could't be hashable
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

            # If I found en equal element, i can stop
            if flag_found is True:
                break

        # After cycling amoung l2, if I can't find an equal element
        if flag_found is False:
            return False

    # if I arrive here
    return True


def compareNested(obj1: Any, obj2: Any) -> bool:
    """Compare complex nested objects."""
    if isinstance(obj1, dict) and isinstance(obj2, dict):
        return compareDict(obj1, obj2)
    if isinstance(obj1, list) and isinstance(obj2, list):
        return compareList(obj1, obj2)
    else:
        return obj1 == obj2


class EnsemblRest(unittest.TestCase):
    """A class to test EnsemblRest methods"""

    def setUp(self) -> None:
        """Create a EnsemblRest object"""
        self.EnsEMBL = pyensemblrest.EnsemblRest()

    def tearDown(self) -> None:
        """Sleep a while before doing next request"""
        time.sleep(WAIT)


class EnsemblRestHelper(EnsemblRest):
    """A class to deal with ensemblrest helper methods"""

    def test_compareNestedDict(self) -> None:
        reference = {
            "one": ["bar", "foo"],
            "two": ["test", "this"],
            "three": ["foo", "bar"],
            "four": ["this", "test"],
        }

        test = {
            "two": ["test", "this"],
            "four": ["this", "test"],
            "three": ["foo", "bar"],
            "one": ["bar", "foo"],
        }

        self.assertTrue(compareNested(reference, test))

    def test_compareNestedList(self) -> None:
        reference = [
            {
                "one": ["bar", "foo"],
                "two": ["test", "this"],
                "three": ["foo", "bar"],
                "four": ["this", "test"],
            },
            {
                "one": ["bar", "foo"],
                "two": ["test", "this"],
                "three": ["foo", "bar"],
                "four": ["this", "test"],
            },
        ]

        test = [
            {
                "two": ["test", "this"],
                "four": ["this", "test"],
                "three": ["foo", "bar"],
                "one": ["bar", "foo"],
            },
            {
                "two": ["test", "this"],
                "four": ["this", "test"],
                "three": ["foo", "bar"],
                "one": ["bar", "foo"],
            },
        ]

        self.assertTrue(compareNested(reference, test))


class EnsemblRestBase(EnsemblRest):
    """A class to deal with ensemblrest base methods"""

    @pytest.mark.live
    def test_setHeaders(self) -> None:
        """Testing EnsemblRest with no headers provided"""

        user_agent = ensembl_user_agent
        self.EnsEMBL = pyensemblrest.EnsemblRest(headers={})
        self.assertEqual(self.EnsEMBL.session.headers.get("User-Agent"), user_agent)

    @pytest.mark.live
    def test_mandatoryParameters(self) -> None:
        """Testing EnsemblRest with no mandatory parameters"""

        self.assertRaisesRegex(
            Exception,
            "mandatory param .* not specified",
            self.EnsEMBL.getArchiveById,
        )

    @pytest.mark.live
    def test_wait4request(self) -> None:
        """Simulating max request per second"""

        self.EnsEMBL.getArchiveById(id="ENSG00000157764")
        self.EnsEMBL.req_count = 15
        self.EnsEMBL.last_req += 2
        self.EnsEMBL.getArchiveById(id="ENSG00000157764")

        # check request count has reset to zero
        self.assertEqual(self.EnsEMBL.req_count, 0)

    @pytest.mark.live
    def test_methodNotImplemented(self) -> None:
        """Testing a not implemented method"""

        # Add a non supported method
        pyensemblrest.ensemblrest.ensembl_api_table["notImplemented"] = {
            "doc": "Uses the given identifier to return the archived sequence",
            "url": "/archive/id/{{id}}",
            "method": "HEAD",
            "content_type": "application/json",
        }

        # register this method
        self.EnsEMBL.__dict__["notImplemented"] = self.EnsEMBL.register_api_func(
            "notImplemented", pyensemblrest.ensembl_config.ensembl_api_table
        )

        # Set __doc__ for generic class method
        self.EnsEMBL.__dict__[
            "notImplemented"
        ].__doc__ = pyensemblrest.ensemblrest.ensembl_api_table["notImplemented"]["doc"]

        # add function name to the class methods
        self.EnsEMBL.__dict__["notImplemented"].__name__ = "notImplemented"

        # call the new function and deal with the exception
        self.assertRaises(
            NotImplementedError, self.EnsEMBL.notImplemented, id="ENSG00000157764"
        )

    def __something_bad(self, curl_cmd: str, last_response: Response) -> None:
        """A function to test 'something bad' message"""

        # execute the curl cmd and get data as a dictionary
        reference = jsonFromCurl(curl_cmd)

        # instantiate a fake response
        fakeResponse = FakeResponse(
            headers=last_response.headers,
            status_code=400,
            text="""{"error":"something bad has happened"}""",
        )
        test = self.EnsEMBL.parseResponse(fakeResponse)

        # testing values
        self.assertDictEqual(reference, test)
        self.assertGreaterEqual(self.EnsEMBL.last_attempt, 1)

    @pytest.mark.live
    def test_SomethingBad(self) -> None:
        """Deal with the {"error":"something bad has happened"} message"""

        # get the curl cmd from ensembl site:
        curl_cmd = "curl 'https://rest.ensembl.org/archive/id/ENSG00000157764?' -H 'Content-type:application/json'"

        # get a request
        self.EnsEMBL.getArchiveById(id="ENSG00000157764")

        # retrieve last_reponse
        last_response = self.EnsEMBL.last_response

        # call generic function
        self.__something_bad(curl_cmd, last_response)

    @pytest.mark.live
    def test_SomethingBadPOST(self) -> None:
        """Deal with the {"error":"something bad has happened"} message using a POST method"""

        curl_cmd = (
            """curl 'https://rest.ensembl.org/lookup/id' -H 'Content-type:application/json' """
            """-H 'Accept:application/json' -X POST -d '{ "ids" : ["ENSG00000157764", "ENSG00000248378"] }'"""
        )

        # execute EnsemblRest function
        self.EnsEMBL.getLookupByMultipleIds(ids=["ENSG00000157764", "ENSG00000248378"])

        # retrieve last_reponse
        last_response = self.EnsEMBL.last_response

        # call generic function
        self.__something_bad(curl_cmd, last_response)

    @pytest.mark.live
    def test_LDFeatureContainerAdaptor(self) -> None:
        """Deal with the {"error":"Something went wrong while fetching from LDFeatureContainerAdaptor"} message"""

        curl_cmd = (
            """curl 'https://rest.ensembl.org/ld/human/pairwise/rs6792369/"""
            """rs1042779?population_name=1000GENOMES:phase_3:KHV;r2=0.85' -H 'Content-type:application/json'"""
        )

        # execute the curl cmd an get data as a dictionary
        reference = jsonFromCurl(curl_cmd)

        # get a request
        self.EnsEMBL.getLdPairwise(
            species="human",
            id1="rs6792369",
            id2="rs1042779",
            population_name="1000GENOMES:phase_3:KHV",
            r2=0.85,
        )

        # retrieve last_reponse
        response = self.EnsEMBL.last_response

        # instantiate a fake response
        fakeResponse = FakeResponse(
            headers=response.headers,
            status_code=400,
            text="""{"error":"Something went wrong while fetching from LDFeatureContainerAdaptor"}""",
        )
        test = self.EnsEMBL.parseResponse(fakeResponse)

        # testing values
        self.assertEqual(reference, test)
        self.assertGreaterEqual(self.EnsEMBL.last_attempt, 1)


class EnsemblRestArchive(EnsemblRest):
    """A class to deal with ensemblrest archive methods"""

    @pytest.mark.live
    def test_getArchiveById(self) -> None:
        """Test archive GET endpoint"""

        # get the curl cmd from ensembl site:
        curl_cmd = "curl 'https://rest.ensembl.org/archive/id/ENSG00000157764?' -H 'Content-type:application/json'"

        # execute the curl cmd an get data as a dictionary
        reference = jsonFromCurl(curl_cmd)

        # execute EnsemblRest function
        test = self.EnsEMBL.getArchiveById(id="ENSG00000157764")

        # testing values
        self.assertDictEqual(reference, test)

    @pytest.mark.live
    def test_getXMLArchiveById(self) -> None:
        """text archive GET endpoint returning XML"""

        # get the curl cmd from ensembl site:
        curl_cmd = "curl 'https://rest.ensembl.org/archive/id/ENSG00000157764?' -H 'Content-type:text/xml'"

        # execute the curl cmd an get data as a dictionary
        reference = launch(curl_cmd)

        # execute EnsemblRest function
        test = self.EnsEMBL.getArchiveById(
            id="ENSG00000157764", content_type="text/xml"
        )

        # testing values
        self.assertEqual(reference, test)

    @pytest.mark.live
    def test_getArchiveByMultipleIds(self) -> None:
        """Test archive POST endpoint"""

        curl_cmd = (
            """curl 'https://rest.ensembl.org/archive/id' -H 'Content-type:application/json' """
            """-H 'Accept:application/json' -X POST -d '{ "id" : ["ENSG00000157764", "ENSG00000248378"] }'"""
        )

        # execute the curl cmd an get data as a dictionary
        reference = jsonFromCurl(curl_cmd)

        # execute EnsemblRest function
        test = self.EnsEMBL.getArchiveByMultipleIds(
            id=["ENSG00000157764", "ENSG00000248378"]
        )

        # testing values
        self.assertListEqual(reference, test)


class EnsemblRestComparative(EnsemblRest):
    """A class to deal with ensemblrest comparative genomics methods"""

    @pytest.mark.live
    def test_getCafeGeneTreeById(self) -> None:
        """Test genetree by id GET method"""

        curl_cmd = (
            """curl 'https://rest.ensembl.org/cafe/genetree/id/ENSGT00390000003602?' """
            """-H 'Content-type:application/json'"""
        )

        # execute the curl cmd an get data as a dictionary
        reference = jsonFromCurl(curl_cmd)

        # execute EnsemblRest function. Dealing with application/json is simpler,
        # since text/x-phyloxml+xml may change elements order
        test = self.EnsEMBL.getCafeGeneTreeById(
            id="ENSGT00390000003602", content_type="application/json"
        )

        # testing values
        self.assertTrue(compareNested(reference, test))

    @pytest.mark.live
    def test_getCafeGeneTreeMemberBySymbol(self) -> None:
        """Test genetree by symbol GET method"""

        curl_cmd = (
            """curl 'https://rest.ensembl.org/cafe/genetree/member/symbol/homo_sapiens/"""
            """BRCA2?prune_species=cow;prune_taxon=9526' -H 'Content-type:application/json'"""
        )

        # execute the curl cmd an get data as a dictionary
        reference = jsonFromCurl(curl_cmd)

        # execute EnsemblRest function. Dealing with application/json is simpler,
        # since text/x-phyloxml+xml may change elements order
        test = self.EnsEMBL.getCafeGeneTreeMemberBySymbol(
            species="human",
            symbol="BRCA2",
            prune_species="cow",
            prune_taxon=9526,
            content_type="application/json",
        )

        # testing values
        self.assertTrue(compareNested(reference, test))

    @pytest.mark.live
    def test_getCafeGeneTreeMemberById(self) -> None:
        """Test genetree by member id GET method"""

        curl_cmd = (
            """curl 'https://rest.ensembl.org/cafe/genetree/member/id/"""
            """homo_sapiens/ENSG00000157764?' -H 'Content-type:application/json'"""
        )

        # execute the curl cmd an get data as a dictionary
        reference = jsonFromCurl(curl_cmd)

        # Execute EnsemblRest function. Dealing with application/json is simpler,
        # since text/x-phyloxml+xml may change elements order
        test = self.EnsEMBL.getCafeGeneTreeMemberById(
            id="ENSG00000157764",
            species="homo_sapiens",
            content_type="application/json",
        )

        # Set self.maxDiff to None to see differences
        # self.maxDiff = None

        # testing values. Since json are nested dictionary and lists,
        # and they are not hashable, I need to order list before checking equality,
        # and I need to ensure that dictionaries have the same keys and values
        self.assertTrue(compareNested(reference, test))

    @pytest.mark.live
    def test_getGeneTreeById(self) -> None:
        """Test genetree by id GET method"""

        curl_cmd = (
            """curl 'https://rest.ensembl.org/genetree/id/ENSGT00390000003602?' """
            """-H 'Content-type:application/json'"""
        )

        # execute the curl cmd an get data as a dictionary
        reference = jsonFromCurl(curl_cmd)

        # execute EnsemblRest function. Dealing with application/json is simpler,
        # since text/x-phyloxml+xml may change elements order
        test = self.EnsEMBL.getGeneTreeById(
            id="ENSGT00390000003602", content_type="application/json"
        )

        # testing values
        self.assertTrue(compareNested(reference, test))

    @pytest.mark.live
    def test_getGeneTreeMemberBySymbol(self) -> None:
        """Test genetree by symbol GET method"""

        curl_cmd = (
            """curl 'https://rest.ensembl.org/genetree/member/symbol/homo_sapiens/"""
            """BRCA2?prune_species=cow;prune_taxon=9526' -H 'Content-type:application/json'"""
        )

        # execute the curl cmd an get data as a dictionary
        reference = jsonFromCurl(curl_cmd)

        # execute EnsemblRest function. Dealing with application/json is simpler,
        # since text/x-phyloxml+xml may change elements order
        test = self.EnsEMBL.getGeneTreeMemberBySymbol(
            species="human",
            symbol="BRCA2",
            prune_species="cow",
            prune_taxon=9526,
            content_type="application/json",
        )

        # testing values
        self.assertTrue(compareNested(reference, test))

    @pytest.mark.live
    def test_getGeneTreeMemberById(self) -> None:
        """Test genetree by member id GET method"""

        curl_cmd = (
            """curl 'https://rest.ensembl.org/genetree/member/id/"""
            """homo_sapiens/ENSG00000157764?' -H 'Content-type:application/json'"""
        )

        # execute the curl cmd an get data as a dictionary
        reference = jsonFromCurl(curl_cmd)

        # Execute EnsemblRest function. Dealing with application/json is simpler,
        # since text/x-phyloxml+xml may change elements order
        test = self.EnsEMBL.getGeneTreeMemberById(
            id="ENSG00000157764",
            species="homo_sapiens",
            content_type="application/json",
        )

        # Set self.maxDiff to None to see differences
        # self.maxDiff = None

        # testing values. Since json are nested dictionary and lists,
        # and they are not hashable, I need to order list before checking equality,
        # and I need to ensure that dictionaries have the same keys and values
        self.assertTrue(compareNested(reference, test))

    @pytest.mark.live
    def test_getAlignmentByRegion(self) -> None:
        """Test get genomic alignment region GET method"""

        curl_cmd = (
            """curl 'https://rest.ensembl.org/alignment/region/homo_sapiens/"""
            """X:1000000..1000100:1?species_set_group=mammals' -H 'Content-type:application/json'"""
        )

        # execute the curl cmd an get data as a dictionary
        reference = jsonFromCurl(curl_cmd)

        # execute EnsemblRest function. Dealing with application/json is simpler
        test = self.EnsEMBL.getAlignmentByRegion(
            species="homo_sapiens",
            region="X:1000000..1000100:1",
            species_set_group="mammals",
        )

        # testing values. Values in list can have different order
        self.assertTrue(compareNested(reference, test))

    @pytest.mark.live
    def test_getHomologyById(self) -> None:
        """test get homology by Id GET method"""

        curl_cmd = (
            """curl 'https://rest.ensembl.org/homology/id/homo_sapiens/ENSG00000157764?' """
            """-H 'Content-type:application/json'"""
        )

        # execute the curl cmd an get data as a dictionary
        reference = jsonFromCurl(curl_cmd)

        # execute EnsemblRest function. Dealing with application/json is simpler,
        #  since text/x-phyloxml+xml may change elements order
        test = self.EnsEMBL.getHomologyById(
            id="ENSG00000157764", species="homo_sapiens"
        )

        # testing values. Since json are nested dictionary and lists,
        # and they are not hashable, I need to order list before checking equality,
        # and I need to ensure that dictionaries have the same keys and values
        self.assertTrue(compareNested(reference, test))

    @pytest.mark.live
    def test_getHomologyBySymbol(self) -> None:
        """test get homology by symbol"""

        curl_cmd = """curl 'https://rest.ensembl.org/homology/symbol/human/BRCA2?' -H 'Content-type:application/json'"""

        # execute the curl cmd an get data as a dictionary
        reference = jsonFromCurl(curl_cmd)

        # execute EnsemblRest function. Dealing with application/json is simpler,
        # since text/x-phyloxml+xml may change elements order
        test = self.EnsEMBL.getHomologyBySymbol(species="human", symbol="BRCA2")

        # testing values. Since json are nested dictionary and lists, and they are not hashable,
        # I need to order list before checking equality,
        # and I need to ensure that dictionaries have the same keys and values
        self.assertTrue(compareNested(reference, test))


class EnsemblRestXref(EnsemblRest):
    """A class to deal with ensemblrest cross references methods"""

    @pytest.mark.live
    def test_getXrefsBySymbol(self) -> None:
        """Testing get XRef by Id GET method"""

        curl_cmd = (
            """curl 'https://rest.ensembl.org/xrefs/symbol/homo_sapiens/BRCA2?' """
            """-H 'Content-type:application/json'"""
        )

        # execute the curl cmd an get data as a dictionary
        reference = jsonFromCurl(curl_cmd)

        # execute EnsemblRest function
        test = self.EnsEMBL.getXrefsBySymbol(species="human", symbol="BRCA2")

        # testing values
        self.assertTrue(compareNested(reference, test))

    @pytest.mark.live
    def test_getXrefsById(self) -> None:
        """Testing get XRef by Id GET method"""

        curl_cmd = """curl 'https://rest.ensembl.org/xrefs/id/ENSG00000157764?' -H 'Content-type:application/json'"""

        # execute the curl cmd an get data as a dictionary
        reference = jsonFromCurl(curl_cmd)

        # execute EnsemblRest function
        test = self.EnsEMBL.getXrefsById(id="ENSG00000157764")

        # testing values
        self.assertTrue(compareNested(reference, test))

    @pytest.mark.live
    def test_getXrefsByName(self) -> None:
        """Testing get XRef by Id GET method"""

        curl_cmd = """curl 'https://rest.ensembl.org/xrefs/name/human/BRCA2?' -H 'Content-type:application/json'"""

        # execute the curl cmd an get data as a dictionary
        reference = jsonFromCurl(curl_cmd)

        # execute EnsemblRest function
        test = self.EnsEMBL.getXrefsByName(species="human", name="BRCA2")

        # testing values
        self.assertTrue(compareNested(reference, test))


class EnsemblRestInfo(EnsemblRest):
    """A class to deal with ensemblrest information methods"""

    @pytest.mark.live
    def test_getInfoAnalysis(self) -> None:
        """Testing Info analysis GET method"""

        curl_cmd = """curl 'https://rest.ensembl.org/info/analysis/homo_sapiens?' -H 'Content-type:application/json'"""

        # execute the curl cmd an get data as a dictionary
        reference = jsonFromCurl(curl_cmd)

        # execute EnsemblRest function
        test = self.EnsEMBL.getInfoAnalysis(species="homo_sapiens")

        # testing values
        self.assertTrue(compareNested(reference, test))

    @pytest.mark.live
    def test_getInfoAssembly(self) -> None:
        """Testing Info assembly GET method"""

        curl_cmd = """curl 'https://rest.ensembl.org/info/assembly/homo_sapiens?' -H 'Content-type:application/json'"""

        # execute the curl cmd an get data as a dictionary
        reference = jsonFromCurl(curl_cmd)

        # execute EnsemblRest function
        test = self.EnsEMBL.getInfoAssembly(species="homo_sapiens")

        # testing values
        self.assertTrue(compareNested(reference, test))

    @pytest.mark.live
    def test_getInfoAssemblyRegion(self) -> None:
        """Testing Info Assembly by region GET method"""

        curl_cmd = """curl 'https://rest.ensembl.org/info/assembly/homo_sapiens/X?' -H 'Content-type:application/json'"""

        # execute the curl cmd an get data as a dictionary
        reference = jsonFromCurl(curl_cmd)

        # execute EnsemblRest function
        test = self.EnsEMBL.getInfoAssemblyRegion(
            species="homo_sapiens", region_name="X"
        )

        # testing values
        self.assertTrue(compareNested(reference, test))

    # @pytest.mark.skip(reason="Keeps timing out - check if working here https://rest.ensembl.org/info/biotypes/homo_sapiens")
    @pytest.mark.live
    def test_getInfoBiotypes(self) -> None:
        """Testing Info BioTypes GET method"""

        curl_cmd = """curl 'https://rest.ensembl.org/info/biotypes/homo_sapiens?' -H 'Content-type:application/json'"""

        # execute the curl cmd an get data as a dictionary
        reference = jsonFromCurl(curl_cmd)

        # execute EnsemblRest function
        test = self.EnsEMBL.getInfoBiotypes(species="homo_sapiens")

        # testing values
        self.assertTrue(compareNested(reference, test))

    @pytest.mark.live
    def test_getInfoBiotypesByGroup(self) -> None:
        """Testing Info BioTypes by Group GET method"""

        curl_cmd = """curl 'https://rest.ensembl.org/info/biotypes/groups/coding/gene?' -H 'Content-type:application/json'"""

        # execute the curl cmd an get data as a dictionary
        reference = jsonFromCurl(curl_cmd)

        # execute EnsemblRest function
        test = self.EnsEMBL.getInfoBiotypesByGroup(group="coding", object_type="gene")

        # testing values
        self.assertTrue(compareNested(reference, test))

    @pytest.mark.live
    def test_getInfoBiotypesByName(self) -> None:
        """Testing Info BioTypes by Name GET method"""

        curl_cmd = """curl 'https://rest.ensembl.org/info/biotypes/name/protein_coding/gene?' -H 'Content-type:application/json'"""

        # execute the curl cmd an get data as a dictionary
        reference = jsonFromCurl(curl_cmd)

        # execute EnsemblRest function
        test = self.EnsEMBL.getInfoBiotypesByName(
            name="protein_coding", object_type="gene"
        )

        # testing values
        self.assertTrue(compareNested(reference, test))

    @pytest.mark.live
    def test_getInfoComparaMethods(self) -> None:
        """Testing Info Compara Methods GET method"""

        curl_cmd = """curl 'https://rest.ensembl.org/info/compara/methods/?' -H 'Content-type:application/json'"""

        # execute the curl cmd an get data as a dictionary
        reference = jsonFromCurl(curl_cmd)

        # execute EnsemblRest function
        test = self.EnsEMBL.getInfoComparaMethods()

        # testing values
        self.assertTrue(compareNested(reference, test))

    @pytest.mark.live
    def test_getInfoComparaSpeciesSets(self) -> None:
        """Testing Info Compara Species Sets GET method"""

        curl_cmd = (
            """curl 'https://rest.ensembl.org/info/compara/species_sets/EPO?' """
            """-H 'Content-type:application/json'"""
        )

        # execute the curl cmd an get data as a dictionary
        reference = jsonFromCurl(curl_cmd)

        # execute EnsemblRest function
        test = self.EnsEMBL.getInfoComparaSpeciesSets(methods="EPO")

        # testing values
        self.assertTrue(compareNested(reference, test))

    @pytest.mark.live
    def test_getInfoComparas(self) -> None:
        """Testing Info Compara GET method"""

        curl_cmd = """curl 'https://rest.ensembl.org/info/comparas?' -H 'Content-type:application/json'"""

        # execute the curl cmd an get data as a dictionary
        reference = jsonFromCurl(curl_cmd)

        # execute EnsemblRest function
        test = self.EnsEMBL.getInfoComparas()

        # testing values
        self.assertTrue(compareNested(reference, test))

    @pytest.mark.live
    def test_getInfoData(self) -> None:
        """Testing Info Data GET method"""

        curl_cmd = """curl 'https://rest.ensembl.org/info/data/?' -H 'Content-type:application/json'"""

        # execute the curl cmd an get data as a dictionary
        reference = jsonFromCurl(curl_cmd)

        # execute EnsemblRest function
        test = self.EnsEMBL.getInfoData()

        # testing values
        self.assertTrue(compareNested(reference, test))

    @pytest.mark.live
    def test_getInfoEgVersion(self) -> None:
        """Testing EgVersion GET method"""

        curl_cmd = """curl 'https://rest.ensembl.org/info/eg_version?' -H 'Content-type:application/json'"""

        # execute the curl cmd an get data as a dictionary
        reference = jsonFromCurl(curl_cmd)

        # execute EnsemblRest function
        test = self.EnsEMBL.getInfoEgVersion()

        # testing values
        self.assertTrue(compareNested(reference, test))

    @pytest.mark.live
    def test_getInfoExternalDbs(self) -> None:
        """Testing Info External Dbs GET method"""

        curl_cmd = (
            """curl 'https://rest.ensembl.org/info/external_dbs/homo_sapiens?' """
            """-H 'Content-type:application/json'"""
        )

        # execute the curl cmd an get data as a dictionary
        reference = jsonFromCurl(curl_cmd)

        # execute EnsemblRest function
        test = self.EnsEMBL.getInfoExternalDbs(species="homo_sapiens")

        # testing values
        self.assertTrue(compareNested(reference, test))

    @pytest.mark.live
    def test_getInfoDivisions(self) -> None:
        """Testing Info Divisions GET method"""

        curl_cmd = """curl 'https://rest.ensembl.org/info/divisions?' -H 'Content-type:application/json'"""

        # execute the curl cmd an get data as a dictionary
        reference = jsonFromCurl(curl_cmd)

        # execute EnsemblRest function
        test = self.EnsEMBL.getInfoDivisions()

        # testing values
        self.assertTrue(compareNested(reference, test))

    @pytest.mark.live
    def test_getInfoGenomesByName(self) -> None:
        """Testing Info Genomes by Name GET method"""

        curl_cmd = (
            """curl 'https://rest.ensembl.org/info/genomes/"""
            """homo_sapiens?' -H 'Content-type:application/json'"""
        )

        # execute the curl cmd an get data as a dictionary
        reference = jsonFromCurl(curl_cmd)

        # execute EnsemblRest function
        test = self.EnsEMBL.getInfoGenomesByName(name="homo_sapiens")

        # testing values
        self.assertTrue(compareNested(reference, test))

    @pytest.mark.live
    def test_getInfoGenomesByAccession(self) -> None:
        """Testing Info Genomes by Accession GET method"""

        curl_cmd = (
            """curl 'https://rest.ensembl.org/info/genomes/accession/U00096?' """
            """-H 'Content-type:application/json'"""
        )

        # execute the curl cmd an get data as a dictionary
        reference = jsonFromCurl(curl_cmd)

        # execute EnsemblRest function
        test = self.EnsEMBL.getInfoGenomesByAccession(accession="U00096")

        # testing values
        self.assertTrue(compareNested(reference, test))

    @pytest.mark.live
    def test_getInfoGenomesByAssembly(self) -> None:
        """Testing Info Genomes by Assembly GET method"""

        curl_cmd = (
            """curl 'https://rest.ensembl.org/info/genomes/assembly/GCA_902167145.1?' """
            """-H 'Content-type:application/json'"""
        )

        # execute the curl cmd an get data as a dictionary
        reference = jsonFromCurl(curl_cmd)

        # execute EnsemblRest function
        test = self.EnsEMBL.getInfoGenomesByAssembly(assembly_id="GCA_902167145.1")

        # testing values
        self.assertTrue(compareNested(reference, test))

    @pytest.mark.live
    def test_getInfoGenomesByDivision(self) -> None:
        """Testing Info Genomes by Division GET method"""

        curl_cmd = (
            """curl 'https://rest.ensembl.org/info/genomes/division/EnsemblPlants?' """
            """-H 'Content-type:application/json'"""
        )

        # execute the curl cmd an get data as a dictionary
        reference = jsonFromCurl(curl_cmd)

        # execute EnsemblRest function
        test = self.EnsEMBL.getInfoGenomesByDivision(division="EnsemblPlants")

        # testing values
        self.assertTrue(compareNested(reference, test))

    @pytest.mark.live
    def test_getInfoGenomesByTaxonomy(self) -> None:
        """Testing Info Genomes by Taxonomy GET method"""

        curl_cmd = (
            """curl 'https://rest.ensembl.org/info/genomes/taxonomy/Arabidopsis?' """
            """-H 'Content-type:application/json'"""
        )

        # execute the curl cmd an get data as a dictionary
        reference = jsonFromCurl(curl_cmd)

        # execute EnsemblRest function
        test = self.EnsEMBL.getInfoGenomesByTaxonomy(taxon_name="Arabidopsis")

        # testing values
        self.assertTrue(compareNested(reference, test))

    @pytest.mark.live
    def test_getInfoPing(self) -> None:
        """Testing Info Ping GET method"""

        curl_cmd = """curl 'https://rest.ensembl.org/info/ping?' -H 'Content-type:application/json'"""

        # execute the curl cmd an get data as a dictionary
        reference = jsonFromCurl(curl_cmd)

        # execute EnsemblRest function
        test = self.EnsEMBL.getInfoPing()

        # testing values
        self.assertTrue(compareNested(reference, test))

    @pytest.mark.live
    def test_getInfoRest(self) -> None:
        """Testing Info REST GET method"""

        curl_cmd = """curl 'https://rest.ensembl.org/info/rest?' -H 'Content-type:application/json'"""

        # execute the curl cmd an get data as a dictionary
        reference = jsonFromCurl(curl_cmd)

        # execute EnsemblRest function
        test = self.EnsEMBL.getInfoRest()

        # testing values
        self.assertEqual(reference, test)

    @pytest.mark.live
    def test_getInfoSoftware(self) -> None:
        """Testing Info Software GET method"""

        curl_cmd = """curl 'https://rest.ensembl.org/info/software?' -H 'Content-type:application/json'"""

        # execute the curl cmd an get data as a dictionary
        reference = jsonFromCurl(curl_cmd)

        # execute EnsemblRest function
        test = self.EnsEMBL.getInfoSoftware()

        # testing values
        self.assertTrue(compareNested(reference, test))

    @pytest.mark.live
    def test_getInfoSpecies(self) -> None:
        """Testing Info Species GET method"""

        curl_cmd = """curl 'https://rest.ensembl.org/info/species?division=ensembl' -H 'Content-type:application/json'"""

        # execute the curl cmd an get data as a dictionary
        reference = jsonFromCurl(curl_cmd)

        # execute EnsemblRest function
        test = self.EnsEMBL.getInfoSpecies(division="ensembl")

        self.assertTrue(compareNested(reference, test))

    @pytest.mark.live
    def test_getInfoVariationBySpecies(self) -> None:
        """Testing Info Variation by species GET method"""

        curl_cmd = """curl 'https://rest.ensembl.org/info/variation/homo_sapiens?' -H 'Content-type:application/json'"""

        # execute the curl cmd an get data as a dictionary
        reference = jsonFromCurl(curl_cmd)

        # execute EnsemblRest function
        test = self.EnsEMBL.getInfoVariationBySpecies(species="homo_sapiens")

        # testing values
        self.assertTrue(compareNested(reference, test))

    @pytest.mark.live
    def test_getInfoVariationConsequenceTypes(self) -> None:
        """Testing Info Variation Consequence Types GET method"""

        curl_cmd = """curl 'https://rest.ensembl.org/info/variation/consequence_types?' -H 'Content-type:application/json'"""

        # execute the curl cmd an get data as a dictionary
        reference = jsonFromCurl(curl_cmd)

        # execute EnsemblRest function
        test = self.EnsEMBL.getInfoVariationConsequenceTypes()

        # testing values
        self.assertTrue(compareNested(reference, test))

    @pytest.mark.live
    def test_getInfoVariationPopulationIndividuals(self) -> None:
        """Testing Info Variation Population Individuals GET method"""

        curl_cmd = (
            """curl 'https://rest.ensembl.org/info/variation/populations/human/1000GENOMES:phase_3:ASW?' """
            """-H 'Content-type:application/json'"""
        )

        # execute the curl cmd an get data as a dictionary
        reference = jsonFromCurl(curl_cmd)

        # execute EnsemblRest function
        test = self.EnsEMBL.getInfoVariationPopulationIndividuals(
            species="human",
            population_name="1000GENOMES:phase_3:ASW",
        )

        # testing values
        self.assertTrue(compareNested(reference, test))

    @pytest.mark.live
    def test_getInfoVariationPopulations(self) -> None:
        """Testing Info Variation Populations GET method"""

        curl_cmd = (
            """curl 'https://rest.ensembl.org/info/variation/populations/homo_sapiens?filter=LD' """
            """-H 'Content-type:application/json'"""
        )

        # execute the curl cmd an get data as a dictionary
        reference = jsonFromCurl(curl_cmd)

        # execute EnsemblRest function
        test = self.EnsEMBL.getInfoVariationPopulations(
            species="homo_sapiens", filter="LD"
        )

        # testing values
        self.assertTrue(compareNested(reference, test))


class EnsemblRestLinkage(EnsemblRest):
    """A class to deal with ensemblrest linkage disequilibrium methods"""

    @pytest.mark.live
    def test_getLdId(self) -> None:
        """Testing get LD ID GET method"""

        curl_cmd = (
            """curl 'https://rest.ensembl.org/ld/human/rs1042779/1000GENOMES:phase_3:KHV?"""
            """window_size=10;d_prime=1.0' -H 'Content-type:application/json'"""
        )

        # execute the curl cmd an get data as a dictionary
        reference = jsonFromCurl(curl_cmd)

        # execute EnsemblRest function
        test = self.EnsEMBL.getLdId(
            species="human",
            id="rs1042779",
            population_name="1000GENOMES:phase_3:KHV",
            window_size=10,
            d_prime=1.0,
        )

        # testing values
        self.assertTrue(compareNested(reference, test))

    @pytest.mark.live
    def test_getLdPairwise(self) -> None:
        """Testing get LD pairwise GET method"""

        curl_cmd = (
            """curl 'https://rest.ensembl.org/ld/human/pairwise/rs6792369/rs1042779?"""
            """population_name=1000GENOMES:phase_3:KHV;r2=0.85' -H 'Content-type:application/json'"""
        )

        # execute the curl cmd an get data as a dictionary
        reference = jsonFromCurl(curl_cmd)

        # execute EnsemblRest function
        test = self.EnsEMBL.getLdPairwise(
            species="human",
            id1="rs6792369",
            id2="rs1042779",
            population_name="1000GENOMES:phase_3:KHV",
            r2=0.85,
        )

        # testing values
        self.assertTrue(compareNested(reference, test))

    @pytest.mark.live
    def test_getLdRegion(self) -> None:
        """Testing get LD region GET method"""

        curl_cmd = (
            """curl 'https://rest.ensembl.org/ld/human/region/6:25837556..25843455/"""
            """1000GENOMES:phase_3:KHV?r2=0.85:d_prime=1.0' -H 'Content-type:application/json'"""
        )

        # execute the curl cmd an get data as a dictionary
        reference = jsonFromCurl(curl_cmd)

        # execute EnsemblRest function
        test = self.EnsEMBL.getLdRegion(
            species="human",
            region="6:25837556..25843455",
            population_name="1000GENOMES:phase_3:KHV",
            r2=0.85,
            d_prime=1.0,
        )

        self.assertTrue(compareNested(reference, test))


class EnsemblRestLookUp(EnsemblRest):
    """A class to deal with ensemblrest LookUp methods"""

    @pytest.mark.live
    def test_getLookupById(self) -> None:
        """Testing get lookup by id GET method"""

        curl_cmd = (
            """curl 'https://rest.ensembl.org/lookup/id/ENSG00000157764?expand=1' """
            """-H 'Content-type:application/json'"""
        )

        # execute the curl cmd an get data as a dictionary
        reference = jsonFromCurl(curl_cmd)

        # execute EnsemblRest function
        test = self.EnsEMBL.getLookupById(id="ENSG00000157764", expand=1)

        # testing values
        self.assertTrue(compareNested(reference, test))

    @pytest.mark.live
    def test_getLookupByMultipleIds(self) -> None:
        """Testing get lookup id POST method"""

        curl_cmd = (
            """curl 'https://rest.ensembl.org/lookup/id' -H 'Content-type:application/json' """
            """-H 'Accept:application/json' -X POST -d '{ "ids" : ["ENSG00000157764", "ENSG00000248378" ] }'"""
        )

        # execute the curl cmd an get data as a dictionary
        reference = jsonFromCurl(curl_cmd)

        # execute EnsemblRest function
        test = self.EnsEMBL.getLookupByMultipleIds(
            ids=["ENSG00000157764", "ENSG00000248378"]
        )

        # testing values
        self.assertTrue(compareNested(reference, test))

    @pytest.mark.live
    def test_getLookupByMultipleIds_additional_arguments(self) -> None:
        """Testing get lookup id POST method with additional arguments"""

        curl_cmd = (
            """curl 'https://rest.ensembl.org/lookup/id?expand=1' -H 'Content-type:application/json' """
            """-H 'Accept:application/json' -X POST -d '{ "ids" : ["ENSG00000157764", "ENSG00000248378"] }'"""
        )

        # execute the curl cmd an get data as a dictionary
        reference = jsonFromCurl(curl_cmd)

        # execute EnsemblRest function
        test = self.EnsEMBL.getLookupByMultipleIds(
            ids=["ENSG00000157764", "ENSG00000248378"], expand=1
        )

        # testing values
        self.assertTrue(compareNested(reference, test))

    @pytest.mark.live
    def test_getLookupBySymbol(self) -> None:
        """Testing get lookup by species GET method"""

        curl_cmd = (
            """curl 'https://rest.ensembl.org/lookup/symbol/homo_sapiens/BRCA2?expand=1' """
            """-H 'Content-type:application/json'"""
        )

        # execute the curl cmd an get data as a dictionary
        reference = jsonFromCurl(curl_cmd)

        # execute EnsemblRest function
        test = self.EnsEMBL.getLookupBySymbol(
            species="homo_sapiens", symbol="BRCA2", expand=1
        )

        # testing values
        self.assertTrue(compareNested(reference, test))

    @pytest.mark.live
    def test_getLookupByMultipleSymbols(self) -> None:
        """Testing get lookup by species POST method"""

        curl_cmd = (
            """curl 'https://rest.ensembl.org/lookup/symbol/homo_sapiens' -H 'Content-type:application/json' """
            """-H 'Accept:application/json' -X POST -d '{ "symbols" : ["BRCA2", "BRAF" ] }'"""
        )

        # execute the curl cmd an get data as a dictionary
        reference = jsonFromCurl(curl_cmd)

        # execute EnsemblRest function
        test = self.EnsEMBL.getLookupByMultipleSymbols(
            species="homo_sapiens", symbols=["BRCA2", "BRAF"]
        )

        # testing values
        self.assertTrue(compareNested(reference, test))

    @pytest.mark.live
    def test_getLookupByMultipleSymbols_additional_arguments(self) -> None:
        """Testing get lookup by species POST method  with additional arguments"""

        curl_cmd = (
            """curl 'https://rest.ensembl.org/lookup/symbol/homo_sapiens?expand=1' """
            """-H 'Content-type:application/json' -H 'Accept:application/json' """
            """-X POST -d '{ "symbols" : ["BRCA2", "BRAF" ] }'"""
        )

        # execute the curl cmd an get data as a dictionary
        reference = jsonFromCurl(curl_cmd)

        # execute EnsemblRest function
        test = self.EnsEMBL.getLookupByMultipleSymbols(
            species="homo_sapiens", symbols=["BRCA2", "BRAF"], expand=1
        )

        # testing values
        self.assertTrue(compareNested(reference, test))


class EnsemblRestMapping(EnsemblRest):
    """A class to deal with ensemblrest mapping methods"""

    @pytest.mark.live
    def test_getMapCdnaToRegion(self) -> None:
        """Testing map CDNA to region GET method"""

        curl_cmd = (
            """curl 'https://rest.ensembl.org/map/cdna/ENST00000288602/100..300?' """
            """-H 'Content-type:application/json'"""
        )

        # execute the curl cmd an get data as a dictionary
        reference = jsonFromCurl(curl_cmd)

        # execute EnsemblRest function
        test = self.EnsEMBL.getMapCdnaToRegion(id="ENST00000288602", region="100..300")

        # testing values
        self.assertTrue(compareNested(reference, test))

    @pytest.mark.live
    def test_getMapCdsToRegion(self) -> None:
        """Testing map CDS to region GET method"""

        curl_cmd = (
            """curl 'https://rest.ensembl.org/map/cds/ENST00000288602/1..1000?' """
            """-H 'Content-type:application/json'"""
        )

        # execute the curl cmd an get data as a dictionary
        reference = jsonFromCurl(curl_cmd)

        # execute EnsemblRest function
        test = self.EnsEMBL.getMapCdsToRegion(id="ENST00000288602", region="1..1000")

        # testing values
        self.assertTrue(compareNested(reference, test))

    @pytest.mark.live
    def test_getMapAssemblyOneToTwo(self) -> None:
        """Testing converting coordinates between assemblies GET method"""

        curl_cmd = (
            """curl 'https://rest.ensembl.org/map/human/GRCh37/X:1000000..1000100:1/GRCh38?' """
            """-H 'Content-type:application/json'"""
        )

        # execute the curl cmd an get data as a dictionary
        reference = jsonFromCurl(curl_cmd)

        # execute EnsemblRest function
        test = self.EnsEMBL.getMapAssemblyOneToTwo(
            species="human",
            asm_one="GRCh37",
            region="X:1000000..1000100:1",
            asm_two="GRCh38",
        )

        # testing values
        self.assertTrue(compareNested(reference, test))

    @pytest.mark.live
    def test_getMapTranslationToRegion(self) -> None:
        """Testing converting protein(traslation) to genomic coordinates GET method"""

        curl_cmd = (
            """curl 'https://rest.ensembl.org/map/translation/ENSP00000288602/100..300?' """
            """-H 'Content-type:application/json'"""
        )

        # execute the curl cmd an get data as a dictionary
        reference = jsonFromCurl(curl_cmd)

        # execute EnsemblRest function
        test = self.EnsEMBL.getMapTranslationToRegion(
            id="ENSP00000288602", region="100..300"
        )

        # testing values
        self.assertTrue(compareNested(reference, test))


class EnsemblRestOT(EnsemblRest):
    """A class to deal with ensemblrest ontologies and taxonomy methods"""

    @pytest.mark.live
    def test_getAncestorsById(self) -> None:
        """Testing get ancestors by id GET method"""

        curl_cmd = (
            """curl 'https://rest.ensembl.org/ontology/ancestors/GO:0005667?' """
            """-H 'Content-type:application/json'"""
        )

        # execute the curl cmd an get data as a dictionary
        reference = jsonFromCurl(curl_cmd)

        # execute EnsemblRest function
        test = self.EnsEMBL.getAncestorsById(id="GO:0005667")

        # testing values
        self.assertTrue(compareNested(reference, test))

    @pytest.mark.live
    def test_getAncestorsChartById(self) -> None:
        """Testing get ancestors chart by id GET method"""

        curl_cmd = (
            """curl 'https://rest.ensembl.org/ontology/ancestors/chart/GO:0005667?' """
            """-H 'Content-type:application/json'"""
        )

        # execute the curl cmd an get data as a dictionary
        reference = jsonFromCurl(curl_cmd)

        # execute EnsemblRest function
        test = self.EnsEMBL.getAncestorsChartById(id="GO:0005667")

        # testing values
        self.assertTrue(compareNested(reference, test))

    @pytest.mark.live
    def test_getDescendantsById(self) -> None:
        """Testing get descendants by id GET method"""

        curl_cmd = (
            """curl 'https://rest.ensembl.org/ontology/descendants/GO:0005667?' """
            """-H 'Content-type:application/json'"""
        )

        # execute the curl cmd an get data as a dictionary
        reference = jsonFromCurl(curl_cmd)

        # execute EnsemblRest function
        test = self.EnsEMBL.getDescendantsById(id="GO:0005667")

        # testing values
        self.assertTrue(compareNested(reference, test))

    @pytest.mark.live
    def test_getOntologyById(self) -> None:
        """Test get ontology by id GET method"""

        curl_cmd = """curl 'https://rest.ensembl.org/ontology/id/GO:0005667?' -H 'Content-type:application/json'"""

        # execute the curl cmd an get data as a dictionary
        reference = jsonFromCurl(curl_cmd)

        # execute EnsemblRest function
        test = self.EnsEMBL.getOntologyById(id="GO:0005667")

        # testing values
        self.assertTrue(compareNested(reference, test))

    @pytest.mark.live
    def test_getOntologyByName(self) -> None:
        """Test get ontology by name GET method"""

        curl_cmd = (
            """curl 'https://rest.ensembl.org/ontology/name/%s?' -H 'Content-type:application/json'"""
            % (urllib.parse.quote("transcription factor complex"))
        )

        # execute the curl cmd an get data as a dictionary
        reference = jsonFromCurl(curl_cmd)

        # execute EnsemblRest function
        test = self.EnsEMBL.getOntologyByName(name="transcription factor complex")

        # testing values
        self.assertTrue(compareNested(reference, test))

    @pytest.mark.live
    def test_getTaxonomyClassificationById(self) -> None:
        """Testing get taxonomy classification by id GET method"""

        curl_cmd = """curl 'https://rest.ensembl.org/taxonomy/classification/9606?' -H 'Content-type:application/json'"""

        # execute the curl cmd an get data as a dictionary
        reference = jsonFromCurl(curl_cmd)

        # execute EnsemblRest function
        test = self.EnsEMBL.getTaxonomyClassificationById(id="9606")

        # testing values
        self.assertTrue(compareNested(reference, test))

    @pytest.mark.live
    def test_getTaxonomyById(self) -> None:
        """Testing get Taxonomy by id GET method"""

        curl_cmd = """curl 'https://rest.ensembl.org/taxonomy/id/9606?' -H 'Content-type:application/json'"""

        # execute the curl cmd an get data as a dictionary
        reference = jsonFromCurl(curl_cmd)

        # execute EnsemblRest function
        test = self.EnsEMBL.getTaxonomyById(id="9606")

        # testing values. Since json are nested dictionary and lists, and they are not hashable,
        # I need to order list before checking equality,
        # and I need to ensure that dictionaries have the same keys and values
        self.assertTrue(compareNested(reference, test))

    @pytest.mark.live
    def test_getTaxonomyByName(self) -> None:
        """Testing get taxonomy by name GET method"""

        curl_cmd = """curl 'https://rest.ensembl.org/taxonomy/name/human?' -H 'Content-type:application/json'"""

        # execute the curl cmd an get data as a dictionary
        reference = jsonFromCurl(curl_cmd)

        # execute EnsemblRest function
        test = self.EnsEMBL.getTaxonomyByName(name="human")

        # testing values. Since json are nested dictionary and lists, and they are not hashable,
        # I need to order list before checking equality,
        # and I need to ensure that dictionaries have the same keys and values
        self.assertTrue(compareNested(reference, test))


class EnsemblRestOverlap(EnsemblRest):
    """A class to deal with ensemblrest overlap methods"""

    @pytest.mark.live
    def test_getOverlapById(self) -> None:
        """Testing get Overlap by ID GET method"""

        curl_cmd = (
            """curl 'https://rest.ensembl.org/overlap/id/ENSG00000157764?feature=gene' """
            """-H 'Content-type:application/json'"""
        )

        # execute the curl cmd an get data as a dictionary
        reference = jsonFromCurl(curl_cmd)

        # execute EnsemblRest function
        test = self.EnsEMBL.getOverlapById(id="ENSG00000157764", feature="gene")

        # testing values
        self.assertTrue(compareNested(reference, test))

    @pytest.mark.live
    def test_getOverlapByRegion(self) -> None:
        """Testing get Overlap by region GET method"""

        curl_cmd = (
            """curl 'https://rest.ensembl.org/overlap/region/human/7:140424943-140624564?feature=gene;"""
            """feature=transcript;feature=cds;feature=exon' -H 'Content-type:application/json'"""
        )

        # execute the curl cmd an get data as a dictionary
        reference = jsonFromCurl(curl_cmd)

        # execute EnsemblRest function
        test = self.EnsEMBL.getOverlapByRegion(
            species="human",
            region="7:140424943-140624564",
            feature=["gene", "transcript", "cds", "exon"],
        )

        # testing values
        self.assertTrue(compareNested(reference, test))

    @pytest.mark.live
    def test_getOverlapByTranslation(self) -> None:
        """Testing get Overlab by traslation GET method"""

        curl_cmd = (
            """curl 'https://rest.ensembl.org/overlap/translation/ENSP00000288602?type=Superfamily' """
            """-H 'Content-type:application/json'"""
        )

        # execute the curl cmd an get data as a dictionary
        reference = jsonFromCurl(curl_cmd)

        # execute EnsemblRest function
        test = self.EnsEMBL.getOverlapByTranslation(
            id="ENSP00000288602", type="SuperFamily"
        )

        # testing values
        self.assertTrue(compareNested(reference, test))


class EnsemblRestPhenotypeAnnotations(EnsemblRest):
    """A class to deal with ensemblrest phenotype annotations methods"""

    @pytest.mark.live
    def test_getPhenotypeByAccession(self) -> None:
        """Testing get phenotype by accession GET method"""

        curl_cmd = (
            """curl 'https://rest.ensembl.org/phenotype/accession/human/EFO:0003900?' """
            """-H 'Content-type:application/json'"""
        )

        # execute the curl cmd an get data as a dictionary
        reference = jsonFromCurl(curl_cmd)

        # execute EnsemblRest function
        test = self.EnsEMBL.getPhenotypeByAccession(
            species="human", accession="EFO:0003900"
        )

        # testing values
        self.assertTrue(compareNested(reference, test))

    @pytest.mark.live
    def test_getPhenotypeByGene(self) -> None:
        """Testing get phenotype by gene GET method"""

        curl_cmd = (
            """curl 'https://rest.ensembl.org/phenotype/gene/human/ENSG00000157764?' """
            """-H 'Content-type:application/json'"""
        )

        # execute the curl cmd an get data as a dictionary
        reference = jsonFromCurl(curl_cmd)

        # execute EnsemblRest function
        test = self.EnsEMBL.getPhenotypeByGene(species="human", gene="ENSG00000157764")

        # testing values
        self.assertTrue(compareNested(reference, test))

    @pytest.mark.live
    def test_getPhenotypeByRegion(self) -> None:
        """Testing get phenotype by region GET method"""

        curl_cmd = (
            """curl 'https://rest.ensembl.org/phenotype/region/human/9:22125500-22136000:1?' """
            """-H 'Content-type:application/json'"""
        )

        # execute the curl cmd an get data as a dictionary
        reference = jsonFromCurl(curl_cmd)

        # execute EnsemblRest function
        test = self.EnsEMBL.getPhenotypeByRegion(
            species="human", region="9:22125500-22136000:1"
        )

        # testing values
        self.assertTrue(compareNested(reference, test))

    @pytest.mark.live
    def test_getPhenotypeByTerm(self) -> None:
        """Testing get phenotype by term GET method"""

        curl_cmd = (
            """curl 'https://rest.ensembl.org/phenotype/term/human/coffee%20consumption?' """
            """-H 'Content-type:application/json'"""
        )

        # execute the curl cmd an get data as a dictionary
        reference = jsonFromCurl(curl_cmd)

        # execute EnsemblRest function
        test = self.EnsEMBL.getPhenotypeByTerm(
            species="human", term="coffee consumption"
        )

        # testing values
        self.assertTrue(compareNested(reference, test))


class EnsemblRestRegulation(EnsemblRest):
    """A class to deal with ensemblrest regulation methods"""

    @pytest.mark.live
    def test_getRegulationBindingMatrix(self) -> None:
        """Testing get regulation binding matrix GET method"""

        curl_cmd = (
            """curl 'https://rest.ensembl.org/species/human/binding_matrix/ENSPFM0001?' """
            """-H 'Content-type:application/json'"""
        )

        # execute the curl cmd an get data as a dictionary
        reference = jsonFromCurl(curl_cmd)

        # execute EnsemblRest function
        test = self.EnsEMBL.getRegulationBindingMatrix(
            species="human", binding_matrix="ENSPFM0001"
        )

        # testing values
        self.assertTrue(compareNested(reference, test))


class EnsemblRestSequence(EnsemblRest):
    """A class to deal with ensemblrest sequence methods"""

    @pytest.mark.live
    def test_getSequenceById(self) -> None:
        """Testing get sequence by ID GET method"""

        curl_cmd = (
            """curl 'https://rest.ensembl.org/sequence/id/CCDS5863.1?object_type=transcript;"""
            """db_type=otherfeatures;type=cds;species=human' -H 'Content-type:application/json'"""
        )

        # execute the curl cmd an get data as a dictionary
        reference = jsonFromCurl(curl_cmd)

        # execute EnsemblRest function
        test = self.EnsEMBL.getSequenceById(
            id="CCDS5863.1",
            object_type="transcript",
            db_type="otherfeatures",
            type="cds",
            species="human",
        )

        # testing values
        self.assertTrue(compareNested(reference, test))

    @pytest.mark.live
    def test_getSequenceByMultipleIds(self) -> None:
        """Testing get sequence by ID POST method"""

        curl_cmd = (
            """curl 'https://rest.ensembl.org/sequence/id' -H 'Content-type:application/json' """
            """-H 'Accept:application/json' -X POST -d '{ "ids" : ["ENSG00000157764", "ENSG00000248378"]}'"""
        )

        # execute the curl cmd an get data as a dictionary
        reference = jsonFromCurl(curl_cmd)

        # execute EnsemblRest function
        test = self.EnsEMBL.getSequenceByMultipleIds(
            ids=["ENSG00000157764", "ENSG00000248378"]
        )

        # testing values
        self.assertTrue(compareNested(reference, test))

    @pytest.mark.live
    def test_getSequenceByMultipleIds_additional_arguments(self) -> None:
        """Testing getSequenceByMultipleIds with mask="soft" and expand_3prime=100"""

        curl_cmd = (
            """curl 'https://rest.ensembl.org/sequence/id?mask=soft;expand_3prime=100' """
            """-H 'Content-type:application/json' -H 'Accept:application/json' """
            """-X POST -d '{ "ids" : ["ENSG00000157764", "ENSG00000248378" ] }'"""
        )

        # execute the curl cmd an get data as a dictionary
        reference = jsonFromCurl(curl_cmd)

        # execute EnsemblRest function
        test = self.EnsEMBL.getSequenceByMultipleIds(
            ids=["ENSG00000157764", "ENSG00000248378"], expand_3prime=100, mask="soft"
        )

        # testing values
        self.assertTrue(compareNested(reference, test))

    @pytest.mark.live
    def test_getSequenceByRegion(self) -> None:
        """Testing get sequence by region GET method"""

        curl_cmd = (
            """curl 'https://rest.ensembl.org/sequence/region/human/X:1000000..1000100:1?' """
            """-H 'Content-type:application/json'"""
        )

        # execute the curl cmd an get data as a dictionary
        reference = jsonFromCurl(curl_cmd)

        # execute EnsemblRest function
        test = self.EnsEMBL.getSequenceByRegion(
            species="human", region="X:1000000..1000100:1"
        )

        # testing values
        self.assertTrue(compareNested(reference, test))

    @pytest.mark.live
    def test_getSequenceByMultipleRegions(self) -> None:
        """Testing get sequence by region POST method"""

        curl_cmd = (
            """curl 'https://rest.ensembl.org/sequence/region/human' -H 'Content-type:application/json' """
            """-H 'Accept:application/json' -X POST """
            """-d '{ "regions" : ["X:1000000..1000100:1", "ABBA01004489.1:1..100"] }'"""
        )

        # execute the curl cmd an get data as a dictionary
        reference = jsonFromCurl(curl_cmd)

        # execute EnsemblRest function
        test = self.EnsEMBL.getSequenceByMultipleRegions(
            species="human", regions=["X:1000000..1000100:1", "ABBA01004489.1:1..100"]
        )

        # testing values
        self.assertTrue(compareNested(reference, test))

    @pytest.mark.live
    def test_getSequenceByMultipleRegions_additional_arguments(self) -> None:
        """Testing get sequence by region POST method with mask="soft" and expand_3prime=100"""

        curl_cmd = (
            """curl 'https://rest.ensembl.org/sequence/region/human?mask=soft;expand_3prime=100' """
            """-H 'Content-type:application/json' -H 'Accept:application/json' -X POST """
            """-d '{ "regions" : ["X:1000000..1000100:1", "ABBA01004489.1:1..100"] }'"""
        )

        # execute the curl cmd an get data as a dictionary
        reference = jsonFromCurl(curl_cmd)

        # execute EnsemblRest function
        test = self.EnsEMBL.getSequenceByMultipleRegions(
            species="human",
            regions=["X:1000000..1000100:1", "ABBA01004489.1:1..100"],
            expand_3prime=100,
            mask="soft",
        )

        # testing values
        self.assertTrue(compareNested(reference, test))


class EnsemblRestHaplotype(EnsemblRest):
    """A class to deal with ensemblrest transcript haplotypes methods"""

    @pytest.mark.live
    def test_getTranscripsHaplotypes(self) -> None:
        """Testing get transcripts Haplotypes GET method"""

        curl_cmd = (
            """curl 'https://rest.ensembl.org/transcript_haplotypes/homo_sapiens/ENST00000288602?' """
            """-H 'Content-type:application/json'"""
        )

        # execute the curl cmd an get data as a dictionary
        reference = jsonFromCurl(curl_cmd)

        # execute EnsemblRest function
        test = self.EnsEMBL.getTranscriptHaplotypes(
            species="homo_sapiens", id="ENST00000288602"
        )

        # testing values
        self.assertTrue(compareNested(reference, test))


class EnsemblRestVEP(EnsemblRest):
    """A class to deal with ensemblrest Variant Effect Predictor methods"""

    @pytest.mark.live
    def test_getVariantConsequencesByHGVSNotation(self) -> None:
        """Testing get Variant Consequences by HFVS notation GET method"""

        curl_cmd = """curl 'https://rest.ensembl.org/vep/human/hgvs/ENST00000366667:c.803C>T?' -H 'Content-type:application/json'"""

        # execute the curl cmd an get data as a dictionary
        reference = jsonFromCurl(curl_cmd)

        # execute EnsemblRest function
        test = self.EnsEMBL.getVariantConsequencesByHGVSNotation(
            species="human", hgvs_notation="ENST00000366667:c.803C>T"
        )

        # testing values
        self.assertTrue(compareNested(reference, test))

    @pytest.mark.live
    def test_getVariantConsequencesByMultipleHGVSnotations(self) -> None:
        """Testing get variant consequences by multiple HFVS notations POST method"""

        curl_cmd = (
            """curl -X POST 'https://rest.ensembl.org/vep/human/hgvs' """
            """-d '{ "hgvs_notations" : ["ENST00000366667:c.803C>T", "9:g.22125504G>C"] }' """
            """-H 'Content-type:application/json' -H 'Accept:application/json'"""
        )

        # execute the curl cmd an get data as a dictionary
        reference = jsonFromCurl(curl_cmd)

        # execute EnsemblRest function
        test = self.EnsEMBL.getVariantConsequencesByMultipleHGVSNotations(
            species="human",
            hgvs_notations=["ENST00000366667:c.803C>T", "9:g.22125504G>C"],
        )

        # testing values
        self.assertTrue(compareNested(reference, test))

    @pytest.mark.live
    def test_getVariantConsequencesById(self) -> None:
        """Testing get variant Consequences by id GET method"""

        curl_cmd = """curl 'https://rest.ensembl.org/vep/human/id/COSM476?' -H 'Content-type:application/json'"""

        # execute the curl cmd an get data as a dictionary
        reference = jsonFromCurl(curl_cmd)

        # execute EnsemblRest function
        test = self.EnsEMBL.getVariantConsequencesById(species="human", id="COSM476")

        # testing values
        self.assertTrue(compareNested(reference, test))

    @pytest.mark.live
    def test_getVariantConsequencesByMultipleIds(self) -> None:
        """Testing get variant Consequences by id POST method"""

        curl_cmd = (
            """curl 'https://rest.ensembl.org/vep/human/id' -H 'Content-type:application/json' """
            """-H 'Accept:application/json' -X POST -d '{ "ids" : ["rs56116432", "COSM476" ] }'"""
        )

        # execute the curl cmd an get data as a dictionary
        reference = jsonFromCurl(curl_cmd)

        # execute EnsemblRest function
        test = self.EnsEMBL.getVariantConsequencesByMultipleIds(
            species="human", ids=["rs56116432", "COSM476"]
        )

        # testing values
        self.assertTrue(compareNested(reference, test))

    @pytest.mark.live
    def test_getVariantConsequencesByMultipleIds_additional_arguments(self) -> None:
        """Testing get variant Consequences by id POST method using Blosum62=1, CSN=1"""

        curl_cmd = (
            """curl 'https://rest.ensembl.org/vep/human/id?Blosum62=1;CSN=1' """
            """-H 'Content-type:application/json' -H 'Accept:application/json' """
            """-X POST -d '{ "ids" : ["rs56116432", "COSM476" ] }'"""
        )

        # execute the curl cmd an get data as a dictionary
        reference = jsonFromCurl(curl_cmd)

        # execute EnsemblRest function
        test = self.EnsEMBL.getVariantConsequencesByMultipleIds(
            species="human", ids=["rs56116432", "COSM476"], Blosum62=1, CSN=1
        )

        # testing values
        self.assertTrue(compareNested(reference, test))

    @pytest.mark.live
    def test_getVariantConsequencesByRegion(self) -> None:
        """Testing get variant consequences by Region GET method"""

        curl_cmd = (
            """curl 'https://rest.ensembl.org/vep/human/region/9:22125503-22125502:1/C?' """
            """-H 'Content-type:application/json'"""
        )

        # execute the curl cmd an get data as a dictionary
        reference = jsonFromCurl(curl_cmd)

        # execute EnsemblRest function
        test = self.EnsEMBL.getVariantConsequencesByRegion(
            species="human", region="9:22125503-22125502:1", allele="C"
        )

        # testing values
        self.assertTrue(compareNested(reference, test))

    @pytest.mark.live
    def test_getVariantConsequencesByMultipleRegions(self) -> None:
        """Testing get variant consequences by Region POST method"""

        curl_cmd = (
            """curl 'https://rest.ensembl.org/vep/homo_sapiens/region' -H 'Content-type:application/json' """
            """-H 'Accept:application/json' -X POST -d '{ "variants" : """
            """["21 26960070 rs116645811 G A . . .", "21 26965148 rs1135638 G A . . ." ] }'"""
        )

        # execute the curl cmd an get data as a dictionary
        reference = jsonFromCurl(curl_cmd)

        # execute EnsemblRest function
        test = self.EnsEMBL.getVariantConsequencesByMultipleRegions(
            species="human",
            variants=[
                "21 26960070 rs116645811 G A . . .",
                "21 26965148 rs1135638 G A . . .",
            ],
        )

        # testing values
        self.assertTrue(compareNested(reference, test))

    @pytest.mark.live
    def test_getVariantConsequencesByMultipleRegions_additional_arguments(self) -> None:
        """Testing get variant consequences by Region POST method Blosum62=1, CSN=1"""

        curl_cmd = (
            """curl 'https://rest.ensembl.org/vep/homo_sapiens/region?Blosum62=1;CSN=1' """
            """-H 'Content-type:application/json' -H 'Accept:application/json' -X POST -d """
            """'{ "variants" : ["21 26960070 rs116645811 G A . . .", "21 26965148 rs1135638 G A . . ." ] }'"""
        )

        # execute the curl cmd an get data as a dictionary
        reference = jsonFromCurl(curl_cmd)

        # execute EnsemblRest function
        test = self.EnsEMBL.getVariantConsequencesByMultipleRegions(
            species="human",
            variants=[
                "21 26960070 rs116645811 G A . . .",
                "21 26965148 rs1135638 G A . . .",
            ],
            Blosum62=1,
            CSN=1,
        )

        # testing values
        self.assertTrue(compareNested(reference, test))


class EnsemblRestVariation(EnsemblRest):
    """A class to deal with ensemblrest variation methods"""

    @pytest.mark.live
    def test_getVariantRecoderById(self) -> None:
        """Testing get variant recoder by id GET method"""

        curl_cmd = """curl 'https://rest.ensembl.org/variant_recoder/human/rs56116432?' -H 'Content-type:application/json'"""

        # execute the curl cmd an get data as a dictionary
        reference = jsonFromCurl(curl_cmd)

        # execute EnsemblRest function
        test = self.EnsEMBL.getVariationRecoderById(id="rs56116432", species="human")

        # testing values
        self.assertTrue(compareNested(reference, test))

    @pytest.mark.live
    def test_getVariantRecoderByMultipleIds(self) -> None:
        """Testing get variant recoder by multiple ids POST method"""

        curl_cmd = (
            """curl -X POST 'https://rest.ensembl.org/variant_recoder/human' """
            """-d '{ "ids" : ["rs56116432", "rs1042779" ] }' """
            """-H 'Content-type:application/json' -H 'Accept:application/json' """
        )

        # execute the curl cmd an get data as a dictionary
        reference = jsonFromCurl(curl_cmd)

        # execute EnsemblRest function
        test = self.EnsEMBL.getVariationRecoderByMultipleIds(
            ids=["rs56116432", "rs1042779"], species="human"
        )

        # testing values
        self.assertTrue(compareNested(reference, test))

    @pytest.mark.live
    def test_getVariationById(self) -> None:
        """Testing get variation by id GET method"""

        curl_cmd = """curl 'https://rest.ensembl.org/variation/human/rs56116432?' -H 'Content-type:application/json'"""

        # execute the curl cmd an get data as a dictionary
        reference = jsonFromCurl(curl_cmd)

        # execute EnsemblRest function
        test = self.EnsEMBL.getVariationById(id="rs56116432", species="homo_sapiens")

        # testing values
        self.assertTrue(compareNested(reference, test))

    @pytest.mark.live
    def test_getVariationByPMCID(self) -> None:
        """Testing get variation by pmcid GET method"""

        curl_cmd = """curl 'https://rest.ensembl.org/variation/human/pmcid/PMC5002951?' -H 'Content-type:application/json'"""

        # execute the curl cmd an get data as a dictionary
        reference = jsonFromCurl(curl_cmd)

        # execute EnsemblRest function
        test = self.EnsEMBL.getVariationByPMCID(pmcid="PMC5002951", species="human")

        # testing values
        self.assertTrue(compareNested(reference, test))

    @pytest.mark.live
    def test_getVariationByPMID(self) -> None:
        """Testing get variation by pmid GET method"""

        curl_cmd = """curl 'https://rest.ensembl.org/variation/human/pmid/26318936?' -H 'Content-type:application/json'"""

        # execute the curl cmd an get data as a dictionary
        reference = jsonFromCurl(curl_cmd)

        # execute EnsemblRest function
        test = self.EnsEMBL.getVariationByPMID(pmid="26318936", species="human")

        # testing values
        self.assertTrue(compareNested(reference, test))

    @pytest.mark.live
    def test_getVariationByMultipleIds(self) -> None:
        """Testing get variation by id POST method"""

        curl_cmd = (
            """curl 'https://rest.ensembl.org/variation/homo_sapiens' -H 'Content-type:application/json' """
            """-H 'Accept:application/json' -X POST -d '{ "ids" : ["rs56116432", "COSM476" ] }'"""
        )

        # execute the curl cmd an get data as a dictionary
        reference = jsonFromCurl(curl_cmd)

        # execute EnsemblRest function
        test = self.EnsEMBL.getVariationByMultipleIds(
            ids=["rs56116432", "COSM476"], species="homo_sapiens"
        )

        # testing values
        self.assertTrue(compareNested(reference, test))

    @pytest.mark.live
    def test_getVariationByMultipleIds_additional_arguments(self) -> None:
        """Testing get variation by id POST method with genotypes=1"""

        curl_cmd = (
            """curl 'https://rest.ensembl.org/variation/homo_sapiens?genotypes=1' """
            """-H 'Content-type:application/json' -H 'Accept:application/json' """
            """-X POST -d '{ "ids" : ["rs56116432", "COSM476" ] }'"""
        )

        # execute the curl cmd an get data as a dictionary
        reference = jsonFromCurl(curl_cmd)

        # execute EnsemblRest function
        test = self.EnsEMBL.getVariationByMultipleIds(
            ids=["rs56116432", "COSM476"], species="homo_sapiens", genotypes=1
        )

        # testing values
        self.assertTrue(compareNested(reference, test))


class EnsemblRestVariationGA4GH(EnsemblRest):
    """A class to deal with ensemblrest variation GA4GH methods"""

    @pytest.mark.live
    def test_getGA4GHBeacon(self) -> None:
        """Testing get GA4GH beacon GET method"""

        curl_cmd = """curl 'https://rest.ensembl.org/ga4gh/beacon?' -H 'Content-type:application/json' """

        # execute the curl cmd an get data as a dictionary
        reference = jsonFromCurl(curl_cmd)

        # execute EnsemblRest function
        test = self.EnsEMBL.getGA4GHBeacon()

        # testing values
        self.assertTrue(compareNested(reference, test))

    @pytest.mark.live
    def test_getGA4GHBeaconQuery(self) -> None:
        """Testing get GA4GH beacon query GET method"""

        curl_cmd = (
            """curl 'http://rest.ensembl.org/ga4gh/beacon/query?referenceBases=G;"""
            """alternateBases=C;referenceName=9;assemblyId=GRCh38;start=22125503' """
            """-H 'Content-type:application/json' """
        )

        # execute the curl cmd an get data as a dictionary
        reference = jsonFromCurl(curl_cmd)

        # execute EnsemblRest function
        test = self.EnsEMBL.getGA4GHBeaconQuery(
            referenceBases="G",
            alternateBases="C",
            referenceName=9,
            assemblyId="GRCh38",
            start=22125503,
        )

        # testing values
        self.assertTrue(compareNested(reference, test))

    @pytest.mark.live
    def test_postGA4GHBeaconQuery(self) -> None:
        """Testing get GA4GH beacon query POST method"""

        curl_cmd = (
            """curl -X POST 'http://rest.ensembl.org/ga4gh/beacon/query' """
            """-H 'Content-type:application/json' -H 'Accept:application/json' """
            """-d '{ "referenceName": "9", "start": 22125503, "referenceBases": "G", """
            """"alternateBases": "C", "assemblyId": "GRCh38"}'"""
        )

        # execute the curl cmd an get data as a dictionary
        reference = jsonFromCurl(curl_cmd)

        # execute EnsemblRest function
        test = self.EnsEMBL.postGA4GHBeaconQuery(
            referenceBases="G",
            alternateBases="C",
            referenceName=9,
            assemblyId="GRCh38",
            start=22125503,
        )

        # testing values
        self.assertTrue(compareNested(reference, test))

    @pytest.mark.live
    def test_getGA4GHFeatures(self) -> None:
        """Testing get GA4GH features GET method"""

        curl_cmd = """curl 'https://rest.ensembl.org/ga4gh/features/ENST00000408937.7?' -H 'Content-type:application/json' """

        # execute the curl cmd an get data as a dictionary
        reference = jsonFromCurl(curl_cmd)

        # execute EnsemblRest function
        test = self.EnsEMBL.getGA4GHFeaturesById(id="ENST00000408937.7")

        # testing values
        self.assertTrue(compareNested(reference, test))

    @pytest.mark.live
    def test_searchGA4GHFeatures(self) -> None:
        """Testing GA4GH features search POST method"""

        curl_cmd = (
            """curl 'https://rest.ensembl.org/ga4gh/features/search' -H 'Content-type:application/json' """
            """-H 'Accept:application/json' -X POST -d '{ "start":39657458, "end": 39753127, """
            """"referenceName":"20", "featureSetId": "", "parentId": "ENSG00000176515.1" }'"""
        )

        # execute the curl cmd an get data as a dictionary
        reference = jsonFromCurl(curl_cmd)

        # execute EnsemblRest function
        test = self.EnsEMBL.searchGA4GHFeatures(
            referenceName="20",
            start=39657458,
            end=39753127,
            featureSetId="",
            parentId="ENSG00000176515.1",
        )

        # testing values
        self.assertTrue(compareNested(reference, test))

    @pytest.mark.live
    def test_searchGA4GHCallset(self) -> None:
        """Testing GA4GH callset search POST method"""

        curl_cmd = (
            """curl 'https://rest.ensembl.org/ga4gh/callsets/search' -H 'Content-type:application/json' """
            """-H 'Accept:application/json' -X POST -d '{ "variantSetId": 1, "pageSize": 2  }'"""
        )

        # execute the curl cmd an get data as a dictionary
        reference = jsonFromCurl(curl_cmd)

        # execute EnsemblRest function
        test = self.EnsEMBL.searchGA4GHCallset(variantSetId=1, pageSize=2)

        # testing values
        self.assertTrue(compareNested(reference, test))

    @pytest.mark.live
    def test_getGA4GHCallsetById(self) -> None:
        """Testing get GA4GH callset by Id GET method"""

        curl_cmd = """curl 'https://rest.ensembl.org/ga4gh/callsets/1:NA19777?' -H 'Content-type:application/json'"""

        # execute the curl cmd an get data as a dictionary
        reference = jsonFromCurl(curl_cmd)

        # execute EnsemblRest function
        test = self.EnsEMBL.getGA4GHCallsetById(id="1:NA19777")

        # testing values
        self.assertTrue(compareNested(reference, test))

    @pytest.mark.live
    def test_searchGA4GHDatasets(self) -> None:
        """Testing GA4GH search dataset POST method"""

        curl_cmd = (
            """curl 'https://rest.ensembl.org/ga4gh/datasets/search' -H 'Content-type:application/json' """
            """-H 'Accept:application/json' -X POST -d '{ "pageSize": 3 }'"""
        )

        # execute the curl cmd an get data as a dictionary
        reference = jsonFromCurl(curl_cmd)

        # execute EnsemblRest function
        test = self.EnsEMBL.searchGA4GHDatasets(pageSize=3)

        # testing values
        self.assertTrue(compareNested(reference, test))

    @pytest.mark.live
    def test_getGA4GHDatasetsById(self) -> None:
        """Testing GA4GH get dataset by Id GET method"""

        curl_cmd = (
            """curl 'https://rest.ensembl.org/ga4gh/datasets/6e340c4d1e333c7a676b1710d2e3953c?' """
            """-H 'Content-type:application/json'"""
        )

        # execute the curl cmd an get data as a dictionary
        reference = jsonFromCurl(curl_cmd)

        # execute EnsemblRest function
        test = self.EnsEMBL.getGA4GHDatasetsById(id="6e340c4d1e333c7a676b1710d2e3953c")

        # testing values
        self.assertTrue(compareNested(reference, test))

    @pytest.mark.live
    def test_searchGA4GHFeatureset(self) -> None:
        """Testing GA4GH featureset search POST method"""

        curl_cmd = (
            """curl 'https://rest.ensembl.org/ga4gh/featuresets/search' -H 'Content-type:application/json' """
            """-H 'Accept:application/json' -X POST -d '{ "datasetId": "Ensembl" }'"""
        )

        # execute the curl cmd an get data as a dictionary
        reference = jsonFromCurl(curl_cmd)

        # execute EnsemblRest function
        test = self.EnsEMBL.searchGA4GHFeaturesets(
            datasetId="Ensembl",
        )

        # testing values
        self.assertTrue(compareNested(reference, test))

    @pytest.mark.live
    def test_getGA4GHFeaturesetById(self) -> None:
        """Testing get GA4GH featureset GET method"""

        curl_cmd = """curl 'https://rest.ensembl.org/ga4gh/featuresets/Ensembl?' -H 'Content-type:application/json' """

        # execute the curl cmd an get data as a dictionary
        reference = jsonFromCurl(curl_cmd)

        # execute EnsemblRest function
        test = self.EnsEMBL.getGA4GHFeaturesetsById(id="Ensembl")

        # testing values
        self.assertTrue(compareNested(reference, test))

    @pytest.mark.live
    def test_getGA4GHVariantsById(self) -> None:
        """Testing GA4GH get variant by Id GET method"""

        curl_cmd = """curl 'https://rest.ensembl.org/ga4gh/variants/1:rs61752113?' -H 'Content-type:application/json'"""

        # execute the curl cmd an get data as a dictionary
        reference = jsonFromCurl(curl_cmd)

        # execute EnsemblRest function
        test = self.EnsEMBL.getGA4GHVariantsById(id="1:rs61752113")

        # testing values
        self.assertTrue(compareNested(reference, test))

    @pytest.mark.live
    def test_searchGA4GHVariantAnnotations(self) -> None:
        """Testing GA4GH variant annotations search POST method"""

        curl_cmd = (
            """curl 'https://rest.ensembl.org/ga4gh/variantannotations/search' -H 'Content-type:application/json' """
            """-H 'Accept:application/json' -X POST -d '{ "variantAnnotationSetId": "Ensembl", "referenceName": "22", """
            """"start": 25000000 , "end": 25194457, "pageSize": 2}'"""
        )

        # execute the curl cmd an get data as a dictionary
        reference = jsonFromCurl(curl_cmd)

        # execute EnsemblRest function
        test = self.EnsEMBL.searchGA4GHVariantAnnotations(
            variantAnnotationSetId="Ensembl",
            referenceName=22,
            start=25000000,
            end=25194457,
            pageSize=2,
        )

        # testing values
        self.assertTrue(compareNested(reference, test))

    @pytest.mark.live
    def test_searchGA4GHVariants(self) -> None:
        """Testing GA4GH search variants POST method"""

        curl_cmd = (
            """curl 'https://rest.ensembl.org/ga4gh/variants/search' -H 'Content-type:application/json' """
            """-H 'Accept:application/json' -X POST -d '{ "variantSetId": 1, "referenceName": 22,"""
            """"start": 17190024, "end": 17671934, "callSetIds":["1:NA19777", "1:HG01242", "1:HG01142"],"""
            """"pageToken":"", "pageSize": 1 }'"""
        )

        # execute the curl cmd an get data as a dictionary
        reference = jsonFromCurl(curl_cmd)

        # execute EnsemblRest function
        test = self.EnsEMBL.searchGA4GHVariants(
            variantSetId=1,
            referenceName=22,
            start=17190024,
            end=17671934,
            callSetIds=["1:NA19777", "1:HG01242", "1:HG01142"],
            pageToken="",
            pageSize=1,
        )

        # testing values
        self.assertTrue(compareNested(reference, test))

    @pytest.mark.live
    def test_searchGA4GHVariantsets(self) -> None:
        """Testing GA4GH search variantset POST method"""

        curl_cmd = (
            """curl 'https://rest.ensembl.org/ga4gh/variantsets/search' -H 'Content-type:application/json' """
            """-H 'Accept:application/json' -X POST -d """
            """'{ "datasetId": "6e340c4d1e333c7a676b1710d2e3953c","pageToken": "", "pageSize": 2 }'"""
        )

        # execute the curl cmd an get data as a dictionary
        reference = jsonFromCurl(curl_cmd)

        # execute EnsemblRest function
        test = self.EnsEMBL.searchGA4GHVariantsets(
            datasetId="6e340c4d1e333c7a676b1710d2e3953c", pageToken="", pageSize=2
        )

        # testing values
        self.assertTrue(compareNested(reference, test))

    @pytest.mark.live
    def test_getGA4GHVariantsetsById(self) -> None:
        """Testing GA4GH get variantset by Id GET method"""

        curl_cmd = """curl 'https://rest.ensembl.org/ga4gh/variantsets/1?' -H 'Content-type:application/json'"""

        # execute the curl cmd an get data as a dictionary
        reference = jsonFromCurl(curl_cmd)

        # execute EnsemblRest function
        test = self.EnsEMBL.getGA4GHVariantsetsById(id=1)

        # testing values
        self.assertTrue(compareNested(reference, test))

    @pytest.mark.live
    def test_searchGA4GHReferences(self) -> None:
        """Testing GA4GH search references POST method"""

        curl_cmd = (
            """curl 'https://rest.ensembl.org/ga4gh/references/search' """
            """-H 'Content-type:application/json' -H 'Accept:application/json' """
            """-X POST -d '{ "referenceSetId": "GRCh38", "pageSize": 10 }'"""
        )

        # execute the curl cmd an get data as a dictionary
        reference = jsonFromCurl(curl_cmd)

        # execute EnsemblRest function
        test = self.EnsEMBL.searchGA4GHReferences(referenceSetId="GRCh38", pageSize=10)

        # testing values
        self.assertTrue(compareNested(reference, test))

    @pytest.mark.live
    def test_getGA4GHReferencesById(self) -> None:
        """Testing GA4GH get references by Id GET method"""

        curl_cmd = (
            """curl 'https://rest.ensembl.org/ga4gh/references/9489ae7581e14efcad134f02afafe26c?' """
            """-H 'Content-type:application/json'"""
        )

        # execute the curl cmd an get data as a dictionary
        reference = jsonFromCurl(curl_cmd)

        # execute EnsemblRest function
        test = self.EnsEMBL.getGA4GHReferencesById(
            id="9489ae7581e14efcad134f02afafe26c"
        )

        # testing values
        self.assertTrue(compareNested(reference, test))

    @pytest.mark.live
    def test_searchGA4GHReferencesets(self) -> None:
        """Testing GA4GH search reference sets POST method"""

        curl_cmd = (
            """curl 'https://rest.ensembl.org/ga4gh/referencesets/search' """
            """-H 'Content-type:application/json' -H 'Accept:application/json' """
            """-X POST -d '{   }'"""
        )

        # execute the curl cmd an get data as a dictionary
        reference = jsonFromCurl(curl_cmd)

        # execute EnsemblRest function
        test = self.EnsEMBL.searchGA4GHReferencesets()

        # testing values
        self.assertTrue(compareNested(reference, test))

    @pytest.mark.live
    def test_getGA4GHReferenceSetsById(self) -> None:
        """Testing GA4GH get reference set by Id GET method"""

        curl_cmd = """curl 'https://rest.ensembl.org/ga4gh/referencesets/GRCh38?' -H 'Content-type:application/json'"""

        # execute the curl cmd an get data as a dictionary
        reference = jsonFromCurl(curl_cmd)

        # execute EnsemblRest function
        test = self.EnsEMBL.getGA4GHReferencesetsById(id="GRCh38")

        # testing values
        self.assertTrue(compareNested(reference, test))

    @pytest.mark.live
    def test_searchGA4GHVariantAnnotationsets(self) -> None:
        """Testing GA4GH variant annotation sets search POST method"""

        curl_cmd = (
            """curl 'https://rest.ensembl.org/ga4gh/variantannotationsets/search' -H 'Content-type:application/json' """
            """-H 'Accept:application/json' -X POST -d '{ "variantSetId": "Ensembl"}'"""
        )

        # execute the curl cmd an get data as a dictionary
        reference = jsonFromCurl(curl_cmd)

        # execute EnsemblRest function
        test = self.EnsEMBL.searchGA4GHVariantAnnotationsets(
            variantSetId="Ensembl",
        )

        # testing values
        self.assertTrue(compareNested(reference, test))

    @pytest.mark.live
    def test_getGA4GHVariantAnnotationsets(self) -> None:
        """Testing get GA4GH variant annotation sets GET method"""

        curl_cmd = """curl 'https://rest.ensembl.org/ga4gh/variantannotationsets/Ensembl' -H 'Content-type:application/json'"""

        # execute the curl cmd an get data as a dictionary
        reference = jsonFromCurl(curl_cmd)

        # execute EnsemblRest function
        test = self.EnsEMBL.getGA4GHVariantAnnotationsetsById(
            id="Ensembl",
        )

        # testing values
        self.assertTrue(compareNested(reference, test))


if __name__ == "__main__":
    unittest.main()
