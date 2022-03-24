# -*- coding: utf-8 -*-
"""
Created on Thu Mar 24 14:53:33 2022

@author: mathieu
"""
from randomwalk import WalkingDot
import unittest

class Testrandomwalk(unittest.TestCase):
    
    def setUp(self):
        
        self.walk = WalkingDot()
    
    def test_doTheWalkTypeErrors(self):

        with self.assertRaises(Exception):
            self.walk.doTheWalk(100.1, 100.1, 101)

    def test_doTheWalkOddNumberLength(self):

        with self.assertRaises(ValueError):
            self.walk.doTheWalk(100, 100, 100)
    
    
    



if __name__ == '__main__':
    unittest.main(verbosity=0)