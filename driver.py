# -*- coding: utf-8 -*-
"""
Created on Tue Mar  8 17:29:53 2022

Author: Sam Taxay

WHAT IS NEEDED:
    Read in gps data to txt file/finding a way to import terminal output
    Read in magnetometer data
"""

import gps_snr as gp
import quest as qt
import numpy as np
import test_data

def main():
    body_0 = np.array([[1,0,0],[0,1,0]])
    body = np.array([[0.8660254,-0.5,0],[0.5,0.8660254,0]])
    body_90 = np.array([[0,1,0],[-1,0,0]])
    body_180z = np.array([[-1,0,0],[0,-1,0]])
    body_180y = np.array([[-1,0,0],[0,1,0]])
    body_180x = np.array([[1,0,0],[0,-1,0]])
    gain = 1
    boresight = gp.snr2boresight(test_data.txt,gain);
    
    inertial = np.array([boresight,[0,1,0]])
    
    body_raw = np.array([[0.7814,0.3751,0.4987],[0.6163,0.7075,-0.3459]])
    inertial_raw = np.array([[0.2673,0.5345,0.8018],[-0.3124,0.9370,0.1562]])
    
    weight = np.array([[1],[1]])

    b_x_180 = np.array([[1,0,0],[0,-1,0]])
    b_x_correct = np.array([0,1,0,0])
    b_y_180 = np.array([[-1,0,0],[0,1,0]])
    b_y_correct = np.array([0,0,1,0])
    b_z_180 = np.array([[-1,0,0],[0,-1,0]])
    b_z_correct = np.array([0,0,0,1])
    w = np.array([[1],[1]])
    i = np.array([[1,0,0],[0,1,0]])
    #tic = time.perf_counter()

    print("original\n",b_x_180)
    out = quest(b_x_180,w,i)
    print("output=\n",out)
    print("actual=\n",b_x_correct)

    print("original\n",b_y_180)
    out = quest(b_y_180,w,i)
    print("output=\n",out)
    print("actual=\n",b_y_correct)

    print("original\n",b_z_180)
    out = quest(b_z_180,w,i)
    print("output=\n",out)
    print("actual=\n",b_z_correct)