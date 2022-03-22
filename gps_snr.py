"""
Originally created on Mon Mar 7 22:31:31 2022

Author: Sam Taxay
"""
import numpy as np

"""
PURPOSE:
    Translates GPS data to an antenna boresight vector for use in QUEST
PARAMETERS:
    filename: txt file containing GPS reciever terminal outputs
    gain: Antenna gain (determined by product)
OUTPUT:
    3x1 Antenna boresight vector for use in QUEST algorithm
"""

def snr2boresight(filename,gain):

    #Opens the txt file containing raw GPS data
    #But, opens the txt file in reverse to read most recent data
    df = reversed(open(filename).readlines())

    #GPS parser to pull out Elevation, Azimuth, and Signal-To-Noise Ratio

    for line in df:
        if not line.startswith('$GPGSV') :
            continue
        else:
            pieces = line.split(',')
            EL = int(pieces[5])
            AZ = int(pieces[6])
            SNR = int(pieces[7])
            break

    print('Satellite Information')
    print('Elevation angle:', EL)
    print('Azimuth angle:', AZ)
    print('Signal-to-Noise Ratio (dB):', SNR)
    print('')

    #Determines off-angle between LOS and Boresight vector
    cos_alf = SNR/(100*gain)-1
    alpha = np.arccos(SNR/(100*gain)-1)


    #Determines line of sight vector
    sat_1 = np.sin(np.deg2rad(AZ)) * np.cos(np.deg2rad(EL))
    sat_2 = np.cos(np.deg2rad(AZ)) * np.cos(np.deg2rad(EL))
    sat_3 = np.sin(np.deg2rad(EL))

    #boresight is A, where A dot L (line of sight) = cos(a)

    #Setting up boresight solver
    LOS = np.array([sat_1,sat_2,sat_3])
    LOS_t = np.transpose(LOS)
    LOS_tr = LOS_t*LOS

    #Solving system of equations
    LOS_full = np.eye(3)*np.transpose(LOS_tr)
    alf_full = LOS_t*cos_alf

    #Finding boresight vector
    boresight = np.linalg.solve(LOS_full,alf_full)

    #LOS_mag = np.sqrt(sat_1**2 + sat_2**2 + sat_3**2)
    #LOS_norm = LOS/LOS_mag
    return boresight

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

    #Calculates roll, pitch, and yaw from quaternion
    roll = np.arctan((2*(q2*q3 + q0*q1))/(2*q0**2 + 2*q3**2 - 1))
    pitch = np.arcsin(-2*q1*q3 - 2*q0*q2)
    yaw =  np.arctan((2*(q1*q2 + q0*q3))/(2*q0**2 + 2*q1**2 - 1))

    rpy = np.array([roll,pitch,yaw])

    return rpy



