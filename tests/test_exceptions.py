import time
import unittest

import pytest

import pyensemblrest
from pyensemblrest.ensemblrest import FakeResponse
from pyensemblrest.exceptions import (
    EnsemblRestError,
    EnsemblRestRateLimitError,
    EnsemblRestServiceUnavailable,
)


class EnsemblRest(unittest.TestCase):
    """A class to test EnsemblRest methods"""

    def setUp(self) -> None:
        """Create a EnsemblRest object"""
        self.EnsEMBL = pyensemblrest.EnsemblRest()

    def tearDown(self) -> None:
        """Sleep a while before doing next request"""
        time.sleep(0.2)

    @pytest.mark.live
    def test_BadRequest(self) -> None:
        """Do an ensembl bad request"""

        self.assertRaisesRegex(
            EnsemblRestError,
            "EnsEMBL REST API returned a 400 (Bad Request)*",
            self.EnsEMBL.getArchiveById,
            id="meow",
        )

    @pytest.mark.live
    def test_BadUrl(self) -> None:
        """Do a Not found request"""

        # record old uri value
        old_uri = self.EnsEMBL.getArchiveById.__globals__["ensembl_api_table"][
            "getArchiveById"
        ]["url"]

        # set a new uri. This change a global value
        self.EnsEMBL.getArchiveById.__globals__["ensembl_api_table"]["getArchiveById"][
            "url"
        ] = "/archive/meow/{{id}}"

        # do a request
        try:
            self.assertRaisesRegex(
                EnsemblRestError,
                "EnsEMBL REST API returned a 404 (Not Found)*",
                self.EnsEMBL.getArchiveById,
                id="ENSG00000157764",
            )

        except AssertionError as e:
            # fix the global value
            self.EnsEMBL.getArchiveById.__globals__["ensembl_api_table"][
                "getArchiveById"
            ]["url"] = old_uri
            # then raise exception
            raise Exception(e)

        # fix the global value
        self.EnsEMBL.getArchiveById.__globals__["ensembl_api_table"]["getArchiveById"][
            "url"
        ] = old_uri

    @pytest.mark.live
    def test_getMsg(self) -> None:
        """Do a bad request and get message"""

        msg = None
        try:
            self.EnsEMBL.getArchiveById(id="miao")
        except EnsemblRestError as e:
            msg = e.msg

        self.assertRegex(msg, "EnsEMBL REST API returned a 400 (Bad Request)*")

    @pytest.mark.live
    def test_rateLimit(self) -> None:
        """Simulating a rate limiting environment"""

        # get a request
        self.EnsEMBL.getArchiveById(id="ENSG00000157764")

        # retrieve last_reponse
        response = self.EnsEMBL.last_response

        # get headers
        headers = response.headers

        # simulating a rate limiting
        # https://github.com/Ensembl/ensembl-rest/wiki/Rate-Limits#a-maxed-out-rate-limit-response
        headers["Retry-After"] = "40.0"
        headers["X-RateLimit-Limit"] = "55000"
        headers["X-RateLimit-Reset"] = "40"
        headers["X-RateLimit-Period"] = "3600"
        headers["X-RateLimit-Remaining"] = "0"

        # set a different status code
        response.status_code = 429

        # now parse request. headers is a reference to response.headers
        self.assertRaisesRegex(
            EnsemblRestRateLimitError,
            "EnsEMBL REST API returned a 429 (Too Many Requests)*",
            self.EnsEMBL.parseResponse,
            response,
        )

        # try to read exception message
        msg = None
        try:
            self.EnsEMBL.parseResponse(response)

        except EnsemblRestError as e:
            msg = e.msg

        self.assertRegex(msg, "EnsEMBL REST API returned a 429 (Too Many Requests)*")

    @pytest.mark.live
    def test_RestUnavailable(self) -> None:
        """Querying a not available REST server"""

        # get an ensembl rest service (supposing that we have no local REST service)
        EnsEMBL = pyensemblrest.EnsemblRest(base_url="http://localhost:3000")

        # get a request (GET)
        self.assertRaises(
            EnsemblRestServiceUnavailable, EnsEMBL.getArchiveById, id="ENSG00000157764"
        )
        self.assertRaises(
            EnsemblRestServiceUnavailable,
            EnsEMBL.getArchiveByMultipleIds,
            id=["ENSG00000157764", "ENSG00000248378"],
        )

    @pytest.mark.live
    def test_SomethingBad(self) -> None:
        """raise exception when n of attempts exceeds"""

        # get a request
        self.EnsEMBL.getArchiveById(id="ENSG00000157764")

        # retrieve last_reponse
        response = self.EnsEMBL.last_response

        # raise last_attempt number
        self.EnsEMBL.last_attempt = self.EnsEMBL.max_attempts

        # instantiate a fake response
        fakeResponse = FakeResponse(
            headers=response.headers,
            status_code=400,
            text="""{"error":"something bad has happened"}""",
        )

        # verify exception
        self.assertRaisesRegex(
            EnsemblRestError,
            "Max number of retries attempts reached.*",
            self.EnsEMBL.parseResponse,
            fakeResponse,
        )

    @pytest.mark.live
    def test_RequestTimeout(self) -> None:
        """Deal with connections timeout"""

        # Ovverride max_attempts
        self.EnsEMBL.max_attempts = 1
        self.EnsEMBL.timeout = 1

        # verify exception
        self.assertRaisesRegex(
            EnsemblRestError,
            "Max number of retries attempts reached.* timeout",
            self.EnsEMBL.searchGA4GHFeatures,
            parentId="ENST00000408937.7",
            featureSetId="",
            featureTypes=["cds"],
            end=220023,
            referenceName="X",
            start=197859,
            pageSize=1,
        )

    @pytest.mark.live
    def test_MaximumPOSTSize(self) -> None:
        """Deal with maximum post size errors"""

        # verify exception
        self.assertRaisesRegex(
            EnsemblRestError,
            "POST message too large.*",
            self.EnsEMBL.getSequenceByMultipleIds,
            ids=[
                "ENSG00000157764",
                "ENSG00000248378",
                "ENSG00000157764",
                "ENSG00000248378",
                "ENSG00000157764",
                "ENSG00000248378",
                "ENSG00000157764",
                "ENSG00000248378",
                "ENSG00000157764",
                "ENSG00000248378",
                "ENSG00000157764",
                "ENSG00000248378",
                "ENSG00000157764",
                "ENSG00000248378",
                "ENSG00000157764",
                "ENSG00000248378",
                "ENSG00000157764",
                "ENSG00000248378",
                "ENSG00000157764",
                "ENSG00000248378",
                "ENSG00000157764",
                "ENSG00000248378",
                "ENSG00000157764",
                "ENSG00000248378",
                "ENSG00000157764",
                "ENSG00000248378",
                "ENSG00000157764",
                "ENSG00000248378",
                "ENSG00000157764",
                "ENSG00000248378",
                "ENSG00000157764",
                "ENSG00000248378",
                "ENSG00000157764",
                "ENSG00000248378",
                "ENSG00000157764",
                "ENSG00000248378",
                "ENSG00000157764",
                "ENSG00000248378",
                "ENSG00000157764",
                "ENSG00000248378",
                "ENSG00000157764",
                "ENSG00000248378",
                "ENSG00000157764",
                "ENSG00000248378",
                "ENSG00000157764",
                "ENSG00000248378",
                "ENSG00000157764",
                "ENSG00000248378",
                "ENSG00000157764",
                "ENSG00000248378",
                "ENSG00000157764",
                "ENSG00000248378",
                "ENSG00000157764",
                "ENSG00000248378",
                "ENSG00000157764",
                "ENSG00000248378",
                "ENSG00000157764",
                "ENSG00000248378",
                "ENSG00000157764",
                "ENSG00000248378",
            ],
        )


if __name__ == "__main__":
    unittest.main()
