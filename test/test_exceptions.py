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
        
        self.assertRaisesRegexp(EnsemblRestError, "EnsEMBL REST API returned a 400 (Bad Request)*", self.EnsEMBL.getArchiveById, id="miao")
        
    def test_BadUrl(self):
        """Do a Not found request"""
        
        # record old uri value
        old_uri = self.EnsEMBL.getArchiveById.func_globals["ensembl_api_table"]["getArchiveById"]["url"]
        
        # set a new uri. This change a global value
        self.EnsEMBL.getArchiveById.func_globals["ensembl_api_table"]["getArchiveById"]["url"] = '/archive/miao/{{id}}'
        
        # do a request
        try:
            self.assertRaisesRegexp(EnsemblRestError, "EnsEMBL REST API returned a 404 (Not Found)*", self.EnsEMBL.getArchiveById, id="ENSG00000157764")
            
        except AssertionError, message:
            # fix the global value
            self.EnsEMBL.getArchiveById.func_globals["ensembl_api_table"]["getArchiveById"]["url"] = old_uri
            # then raise exception
            raise Exception, message
            
        # fix the global value
        self.EnsEMBL.getArchiveById.func_globals["ensembl_api_table"]["getArchiveById"]["url"] = old_uri
        
    def test_getMsg(self):
        """Do a bad request and get message"""
        
        try:
            self.EnsEMBL.getArchiveById(id="miao")
        
        except EnsemblRestError as e:
            pass
        
        self.assertRegexpMatches(e.msg, "EnsEMBL REST API returned a 400 (Bad Request)*")
    

if __name__ == "__main__":
    unittest.main()
