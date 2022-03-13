# -*- coding: utf-8 -*-
"""
Created on Mon Feb  7 23:34:08 2022

@author: samta
"""

#Written by Brian Leung

###PURPOSE:
#This file just runs some unit tests on quest.
import numpy as np
import quest as q
import unittest

#Runs quest and checks against the correct quaternion.
def q_match(correct,b,w,i):
    return(np.sum(abs(correct-(q.quest(b,w,i)).T))<0.001)

class quest_test(unittest.TestCase):

    def test_0(self):
        b_0 = np.array([[1,0,0],[0,1,0]])
        b_0_correct = np.array([1,0,0,0])
        w = np.array([[1],[1]])
        i = np.array([[1,0,0],[0,1,0]])
        self.assertTrue(q_match(b_0_correct,b_0,w,i))

    def test_90(self):
        b_90neg_z = np.array([[0,1,0],[-1,0,0]])
        b_90neg_z_correct = np.array([0.7071068,0,0,-0.7071068])
        w = np.array([[1],[1]])
        i = np.array([[1,0,0],[0,1,0]])
        self.assertTrue(q_match(b_90neg_z_correct,b_90neg_z,w,i))

    def test_180(self):
        b_x_180 = np.array([[1,0,0],[0,-1,0]])
        b_x_correct = np.array([0,1,0,0])
        b_y_180 = np.array([[-1,0,0],[0,1,0]])
        b_y_correct = np.array([0,0,1,0])
        b_z_180 = np.array([[-1,0,0],[0,-1,0]])
        b_z_correct = np.array([0,0,0,1])
        w = np.array([[1],[1]])
        i = np.array([[1,0,0],[0,1,0]])
        self.assertTrue(q_match(b_z_correct,b_z_180,w,i))
        self.assertTrue(q_match(b_x_correct,b_x_180,w,i))
        self.assertTrue(q_match(b_y_correct,b_y_180,w,i))

    def test_aoe_vt(self):
        b = np.array([[0.7814,0.3751,0.4987],[0.6163,0.7075,-0.3459]])
        i = np.array([[0.2673,0.5345,0.8018],[-0.3124,0.9370,0.1562]])
        w = np.array([[1],[1]])
        correct = np.array([0.8418,0.2643,-0.0051,0.4706])
        self.assertTrue(q_match(correct,b,w,i))


if __name__ == "__main__":
    unittest.main()
