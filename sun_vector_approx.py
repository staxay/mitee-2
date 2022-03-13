# -*- coding: utf-8 -*-
"""
Created on Mon Feb  7 23:34:34 2022

@author: samta
"""

#Written by Brian Leung

"""
PURPOSE:
    This function roughly estimates a sun vector, given the photodiode measurements for the antennas. 
PARAMETERS:
    pd_volts: 4x1 numpy array consisting of the photodiode voltages. Will be <Top,Left,Bottom,Right>
OUTPUT:
    1x3 numpy array <x,y,z> of the approximated unit length sun vector, with respect to body frame
"""
import numpy as np

def estimate_sun_vec(pd_volts):
    ### IMPORTANT VALUES ###
    #True: throw errors, False: return <0,0,1>
    throw_error = True
    error_vector = np.array([0,0,1])

    #True: try its best with both sides being bright, False: resort to error
    handle_opposite_sides = True

    max_voltage = 9
    min_voltage = 0.339
    ### END IMPORTANT VALUES ###

    #Scale the pd voltage according to the minimum and maximum voltages. (ideally taken across all days)
    pd_volts = (pd_volts-min_voltage)/(max_voltage-min_voltage)
    #Determines which sensors we should be paying attention to.
    #Find largest pd voltage value.

    primary_sensor = np.argmax(pd_volts)

    #Find second largest pd voltage value.
    temp = np.copy(pd_volts)
    temp[primary_sensor] = 0
    secondary_sensor = np.argmax(temp)
    #If it is way too dark, you can't resolve a vector.

    ### ERROR HANDLING ###

    #If the brightness is 5% of the max brightness, return an error vector. It's too dark to resolve a vector.
    if (np.sum(pd_volts) <= 0.05*4):
        return error_vector

    #If both sensors are on opposite sides of the craft, something doesn't seem right. This will handle it.
    if (secondary_sensor == (primary_sensor+2)%4):
        #Change the secondary sensor to one of the sides next to the primary side, trying to make a best guess.
        if (handle_opposite_sides):
            temp[secondary_sensor] = 0
            secondary_sensor = np.argmax(pd_volts)
        else:
            if (throw_error):
                raise ValueError("Brightness is high on opposite sides of the craft.")
            else:
                return error_vector
    #print("primary",primary_sensor)
    #print("secondary",secondary_sensor)

    ### END ERROR HANDLING ###

    #We can now process this data using arccos.
    pd_angles = np.arccos(pd_volts)
    #pd_angles now has the angles of incidence of the 4 sensors in radians.

    if (primary_sensor==0): #TOP
        primary_vec = np.array([np.tan(pd_angles[0]),1])
    if (primary_sensor==1): #LEFT
        primary_vec = np.array([-1,np.tan(pd_angles[1])])
    if (primary_sensor==2): #BOTTOM
        primary_vec = np.array([np.tan(pd_angles[2]),-1])
    if (primary_sensor==3): #RIGHT
        primary_vec = np.array([1,np.tan(pd_angles[3])])
    if (secondary_sensor==0): #TOP
        secondary_vec = np.array([np.tan(pd_angles[0]),1])
    if (secondary_sensor==1): #LEFT
        secondary_vec = np.array([-1,np.tan(pd_angles[1])])
    if (secondary_sensor==2): #BOTTOM
        secondary_vec = np.array([np.tan(pd_angles[2]),-1])
    if (secondary_sensor==3): #RIGHT
        secondary_vec = np.array([1,np.tan(pd_angles[3])])

    if (primary_sensor%2==0): #if the primary vector is top/bottom and secondary vector is left/right
        primary_vec[0] = primary_vec[0]*secondary_vec[0]
        secondary_vec[1] = secondary_vec[1]*primary_vec[1]
    else: #if the secondary vector is top/bottom and primary vector is left/right
        primary_vec[1] = primary_vec[1]*secondary_vec[1]
        secondary_vec[0] = secondary_vec[0]*primary_vec[0]

    primary_unit_vec = primary_vec / ((primary_vec**2).sum()**0.5)
    secondary_unit_vec = secondary_vec / ((secondary_vec**2).sum()**0.5)
    approx = primary_unit_vec+secondary_unit_vec
    approx = approx / ((approx**2).sum()**0.5)
    return np.array([approx[0],approx[1],0])

def main():
    #pudding = np.array([0.56,0.34,0.2,0.1])
    pudding45 = np.array([0.7071,0.7071,0,0])
    pudding90 = np.array([1,0,0,0])
    pudding_dark = np.array([0.07,0.01,0.01,0.01])
    print(estimate_sun_vec(pudding_dark))

if __name__ == "__main__":
    main()
