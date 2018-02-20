# -*- coding: utf-8 -*-
"""
Created on Wed May 18 14:25:55 2016

@author: Paolo Cozzi <paolo.cozzi@ptp.it>
"""

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

# importing modules
import time

# import my module
import ensemblrest

# import my exceptions
from ensemblrest.exceptions import EnsemblRestError, EnsemblRestRateLimitError, EnsemblRestServiceUnavailable

# import other modules
import unittest

import six

#TODO: test maximum POST input size
class EnsemblRest(unittest.TestCase):
    """A class to test EnsemblRest methods"""
    
    def setUp(self):
        """Create a EnsemblRest object"""
        self.EnsEMBL = ensemblrest.EnsemblRest()
        
    def tearDown(self):
        """Sleep a while before doing next request"""
        time.sleep(0.2)
        
    def test_BadRequest(self):
        """Do an ensembl bad request"""
        
        six.assertRaisesRegex(self, EnsemblRestError, "EnsEMBL REST API returned a 400 (Bad Request)*", self.EnsEMBL.getArchiveById, id="meow")
        
    def test_BadUrl(self):
        """Do a Not found request"""
        
        # record old uri value
        old_uri = self.EnsEMBL.getArchiveById.__globals__["ensembl_api_table"]["getArchiveById"]["url"]
        
        # set a new uri. This change a global value
        self.EnsEMBL.getArchiveById.__globals__["ensembl_api_table"]["getArchiveById"]["url"] = '/archive/meow/{{id}}'
        
        # do a request
        try:
            six.assertRaisesRegex(self, EnsemblRestError, "EnsEMBL REST API returned a 404 (Not Found)*", self.EnsEMBL.getArchiveById, id="ENSG00000157764")
            
        except AssertionError as e:
            # fix the global value
            self.EnsEMBL.getArchiveById.__globals__["ensembl_api_table"]["getArchiveById"]["url"] = old_uri
            # then raise exception
            raise Exception(e)
            
        # fix the global value
        self.EnsEMBL.getArchiveById.__globals__["ensembl_api_table"]["getArchiveById"]["url"] = old_uri
        
    def test_getMsg(self):
        """Do a bad request and get message"""

        msg = None
        try:
            self.EnsEMBL.getArchiveById(id="miao")
        except EnsemblRestError as e:
            msg = e.msg
        
        self.assertRegexpMatches(msg, "EnsEMBL REST API returned a 400 (Bad Request)*")
        
    def test_rateLimit(self):
        """Simulating a rate limiting environment"""
        
        # get a request
        self.EnsEMBL.getArchiveById(id="ENSG00000157764")
        
        # retrieve last_reponse
        response = self.EnsEMBL.last_response
        
        # get headers
        headers = response.headers
        
        # simulating a rate limiting
        # https://github.com/Ensembl/ensembl-rest/wiki/Rate-Limits#a-maxed-out-rate-limit-response
        headers["Retry-After"] = '40.0'
        headers["X-RateLimit-Limit"] = '55000'
        headers["X-RateLimit-Reset"] = '40'
        headers["X-RateLimit-Period"] = '3600'
        headers["X-RateLimit-Remaining"] = '0'
        
        # set a different status code
        response.status_code = 429
        
        # now parse request. headers is a reference to response.headers
        six.assertRaisesRegex(self, EnsemblRestRateLimitError, "EnsEMBL REST API returned a 429 (Too Many Requests)*", self.EnsEMBL.parseResponse, response)
        
        # try to read exception message
        msg = None
        try:
            self.EnsEMBL.parseResponse(response)
        
        except EnsemblRestError as e:
            msg = e.msg
        
        self.assertRegexpMatches(msg, "EnsEMBL REST API returned a 429 (Too Many Requests)*")
        
    def test_RestUnavailable(self):
        """Querying a not available REST server"""
        
        # get an ensembl rest service (sopposing that we have no local REST service)
        EnsEMBL = ensemblrest.EnsemblRest(base_url='http://localhost:3000')
        
        # get a request (GET)
        self.assertRaises(EnsemblRestServiceUnavailable, EnsEMBL.getArchiveById, id="ENSG00000157764")
        self.assertRaises(EnsemblRestServiceUnavailable, EnsEMBL.getArchiveByMultipleIds, id=["ENSG00000157764", "ENSG00000248378"])
        
    def test_SomethingBad(self):
        """raise exception when n of attempts exceeds"""
        
        # get a request
        self.EnsEMBL.getArchiveById(id="ENSG00000157764")
        
        # retrieve last_reponse
        response = self.EnsEMBL.last_response
        
        # raise last_attempt number
        self.EnsEMBL.last_attempt = self.EnsEMBL.max_attempts
        
        # create a fake request.Response class
        class FakeResponse():
            def __init__(self, resp):
                self.headers = resp.headers
                self.status_code = 400
                self.text = """{"error":"something bad has happened"}"""
                
        #instantiate a fake response
        fakeResponse = FakeResponse(response)
        
        # verify exception
        six.assertRaisesRegex(self, EnsemblRestError, "Max number of retries attempts reached.*", self.EnsEMBL.parseResponse, fakeResponse)
        
    def test_RequestTimeout(self):
        """Deal with connections timeout"""
        
        # get a new ensemblrest object
        ensGenomeRest = ensemblrest.EnsemblGenomeRest()
        
        # Ovverride max_attempts
        ensGenomeRest.max_attempts = 1
        ensGenomeRest.timeout = 1
        
        # verify exception
        six.assertRaisesRegex(self, EnsemblRestError, "Max number of retries attempts reached.* timeout", ensGenomeRest.getGeneFamilyById, id="MF_01687", compara="bacteria")


if __name__ == "__main__":
    unittest.main()
