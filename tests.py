import googleplaystore    
import json
import os
import json
import unittest
import collections


__author__ = 'Javier Chavez'
__email__ = 'javierc@cs.unm.edu'



class GooglePlayStoreAPITestCase(unittest.TestCase):

    def setUp(self):
        default_value = ''
        # get the vars defined in bashrc
        cookie = {
            "PLAY_PREFS": os.getenv('PLAY_PREFS', default_value),
            "NID":        os.getenv('NID', default_value),
            "_gat":       os.getenv('GAT', default_value),
            "_ga":        os.getenv('_GA', default_value)
        }


        # init google play store api
        self.ps = googleplaystore.PlayStore(cookie=cookie)

    def test_search_return(self):
        searchcls = self.ps.search('google', 1)

        #self.assertGreater(len(apps), 0)
        self.assertTrue(isinstance(searchcls, googleplaystore.Search))


    def test_app_return(self):
        appcls = self.ps.get_app('com.twitter.android')
        self.assertTrue(isinstance(appcls, googleplaystore.App))
        
        
    def test_app_feilds(self):
        app = self.ps.get_app('com.twitter.android')
        app.populate_fields()

        _feilds = ['url',
                   'name',
                   'developer',
                   'package',
                   'description',
                   'icon',
                   'price',
                   'pub_date',
                   'category'
               ]

        for field in _feilds:
            self.assertTrue(app[field])
        

        
if __name__ == '__main__':
    unittest.main()
        
