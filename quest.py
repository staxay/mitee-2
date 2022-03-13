# -*- coding: utf-8 -*-
"""
Created on Mon Feb  7 22:50:37 2022

@author: samta
"""

#Originally written by Brian Leung, reworked by Sam Taxay

"""
PURPOSE:
    Implementation of the quest algorithm.
PARAMETERS:
    body_vecs: Nx3 numpy array of unit length body measurement vectors, where N>=2
    weights: Nx1 numpy array of weights, corresponding to each of the unit body vectors 
    inertial_vecs: Nx3 numpy array corresponding inertial vectors
OUTPUT:
    Quaternion of current attitude <q0 q1 q2 q3>, where q0 is the scalar term
    (It'll just be a 1x4 numpy array, since numpy doesnt support quaternions natively.)
"""

import numpy as np
import eig_helper as eh
import sun_vector_approx as sv
import gps_snr as gp
import test_data
from math import sqrt
from math import degrees
import time

def quest(body_vecs,weights,inertial_vecs,precision=0.000001):

    #Ensuring proper vector lengths of all inputs
    if (body_vecs.shape[1] != 3 or inertial_vecs.shape[1] != 3 or weights.shape[1] != 1):
        raise ValueError("Check the dimensions on your arrays.")
    #Ensuring same number of inertial and body vectors
    if (body_vecs.shape != inertial_vecs.shape):
        raise ValueError("Unequal numbers of inertial and body vectors.")
    #Ensuring same number of weights and body vectors
    if (body_vecs.shape[0] != weights.shape[0]):
        raise ValueError("Unequal numbers of weights and body vectors.")
    vec_count = body_vecs.shape[0]

    #Just ensures the vectors aren't stuck as ints.
    body_vecs = body_vecs*1.0
    inertial_vecs = inertial_vecs*1.0

    ##DETERMINING APPROXIMATE EIGENVALUE
    eig_guess = weights.sum()
    
    #Calculating K matrix:
    B = np.zeros((3,3))
    for i in range(vec_count):
        B += weights[i]*body_vecs[i,:].reshape(3,1).dot(inertial_vecs[i,:].reshape(1,3))

    Z = np.array([[B[1,2]-B[2,1]],[B[2,0]-B[0,2]],[B[0,1]-B[1,0]]])
    sigma = B[0,0] + B[1,1] + B[2,2] #trace of B
    S = B+B.T
    K = np.zeros((4,4))
    K[0,0]=sigma
    K[1:,0]=Z.reshape(3)
    K[0,1:]=Z.reshape(3)
    K[1:,1:]=S-sigma*np.identity(3)
    
    ##NEWTON RAPHSON TO FIND ACTUAL EIGENVALUE
    c_l3 = eh.l3_coeff(K)
    c_l2 = eh.l2_coeff(K)
    c_l1 = eh.l1_coeff(K)
    c_l0 = eh.l0_coeff(K)
    while (abs(eh.chr_eq(eig_guess,c_l0,c_l1,c_l2,c_l3)) >= precision): #arbitrary precision
        eig_guess -= eh.chr_eq(eig_guess,c_l0,c_l1,c_l2,c_l3)/eh.diff_chr_eq(eig_guess,c_l1,c_l2,c_l3)

    ##SINGULARITY HANDLING
    #Will only trigger if the pre_crp_mat is singular. Should only recurse once.
    #Could this check be done somewhat earlier in the program, 
    #so we don't have to redo everything?
    pre_crp_mat = (eig_guess+sigma)*np.identity(3)-S
    if np.linalg.det(pre_crp_mat) == 0:
        #This alternate body frame is completely arbitrary.
        rot_mat = np.array([
            [0,0,1],
            [1,0,0],
            [0,1,0]])
        rot_quat = np.array([0.5,0.5,0.5,0.5])

        for i in range(vec_count):
            body_vecs[i,:] = (rot_mat.dot(body_vecs[i,:].reshape(3,1))).reshape(3,)

        alt_quat = quest(body_vecs,weights,inertial_vecs)

        ##Rotates the alternate quaternion back to original
        rot_quat_mat = np.array([
            [rot_quat[0],-rot_quat[1],-rot_quat[2],-rot_quat[3]],
            [rot_quat[1], rot_quat[0], rot_quat[3],-rot_quat[2]],
            [rot_quat[2],-rot_quat[3], rot_quat[0], rot_quat[1]],
            [rot_quat[3], rot_quat[2],-rot_quat[1], rot_quat[0]]
        ])
        ##Rounding takes care of any minor precision issues
        return np.around(rot_quat_mat.dot(alt_quat),8)
    
    ##CALCULATE OUTPUT IN CRPs
    crp = np.linalg.inv(pre_crp_mat).dot(Z)
    
    ##CONVERT TO QUATERNIONS
    temp_quat = np.array([[1.0],[0.0],[0.0],[0.0]])
    temp_quat[1:,0] = crp.reshape(3)
    quat = 1/sqrt(1+(crp.T).dot(crp))*temp_quat

    return(quat)


"""
PURPOSE:
    Translates quaternion to roll, pitch, and yaw angles for simplicity
PARAMETERS:
    Quaternion of current attitude <q0 q1 q2 q3>, where q0 is the scalar term
    (It'll just be a 1x4 numpy array, since numpy doesnt support quaternions natively.)
OUTPUT:
    1x3 array of roll, pitch, and yaw angles respectively
"""
def quat2rpy(quat):
    
    #Pulls out each quaterion value from array for ease of use
    q0 = quat[0]
    q1 = quat[1]
    q2 = quat[2]
    q3 = quat[3]
    
    roll = np.arctan((2*(q2*q3 + q0*q1))/(2*q0**2 + 2*q3**2 - 1))
    pitch = np.arcsin(-2*q1*q3 - 2*q0*q2)
    yaw =  np.arctan((2*(q1*q2 + q0*q3))/(2*q0**2 + 2*q1**2 - 1))
    
    rpy = np.array([roll,pitch,yaw])
    
    return(rpy)

"""
PURPOSE:
    Translates roll, pitch, and yaw angles to degrees for simplicity
PARAMETERS:
    1x3 numpy array Roll, Pitch, and Yaw angles in radians
OUTPUT:
    1x3 numpy array of roll, pitch, and yaw angles in degrees respectively
"""
def rpy_degrees(rpy):
    
    for i in range(0,2):
        rpy[i] = degrees(rpy[i])
        
    return rpy

def main():
    body_0 = np.array([[1,0,0],[0,1,0]])
    body = np.array([[0.8660254,-0.5,0],[0.5,0.8660254,0]])
    body_90 = np.array([[0,1,0],[-1,0,0]])
    body_180z = np.array([[-1,0,0],[0,-1,0]])
    body_180y = np.array([[-1,0,0],[0,1,0]])
    body_180x = np.array([[1,0,0],[0,-1,0]])
    pd_volts = np.array([1,2,3,4])
    volts = sv.estimate_sun_vec(pd_volts)
    
    gain = 1
    boresight = gp.snr2boresight(test_data.txt,gain);
    inertial = np.array([volts,boresight])
    
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

    print("original\n",body_raw)
    out = quest(body_raw,w,inertial)
    nout = quat2rpy(out)
    print("output=\n",nout)
    nout = rpy_degrees(nout)
    print("output=\n",nout)
    print("actual=\n",b_x_correct)

    print("original\n",b_y_180)
    out = quest(b_y_180,w,i)
    out = quat2rpy(out)
    print("output=\n",out)
    print("actual=\n",b_y_correct)

    print("original\n",b_z_180)
    out = quest(b_z_180,w,i)
    out = quat2rpy(out)
    print("output=\n",out)
    print("actual=\n",b_z_correct)

if __name__ == "__main__":
    main()

    #---Testing block for characteristic equation---
    '''
    M = np.array([
        [4,1,3,4],
        [5,6,7,8],
        [9,10,11,12],
        [13,14,15,13]])
    c_l3 = eh.l3_coeff(M)
    c_l2 = eh.l2_coeff(M)
    c_l1 = eh.l1_coeff(M)
    c_l0 = eh.l0_coeff(M)
    print(c_l0)
    print(c_l1)
    print(c_l2)
    print(c_l3)
    print(eh.chr_eq(1,c_l0,c_l1,c_l2,c_l3))
    print(eh.diff_chr_eq(1,c_l1,c_l2,c_l3))
    '''
    #---End testing block---

    '''
    #Various debug statements
    print("B = \n",B)
    print("Z = \n",Z)
    print("sigma = \n",sigma)
    print("S = \n",S)
    print("K = \n",K)
    print("Actual eigenvalue is = ",eig_guess)
    print("CRP =\n",crp)
    '''