#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 21 10:17:06 2020

@author: samueljon
"""

import pandas as pd
import numpy as np

# CL - The system cooling load
# RT - capacity of the ith chiller
# COP - Ratio of the chiller cooling load to the chiller power consumption
# PLR - chiller cooling load divided by its design capacity
# L - Lambda multiplier
# time - hourly time from 0-24. 0 is 12AM, 24 is 11PM


class PLR_Calc(object):
    
    def __init__(self,  regression_filepath = 0, 
                 CL_filepath = 0, 
                 RT_filepath = '/Users/samueljon/Desktop/Desktop Folder/University of Arizona/Spring 2020/CHEE 443/CHRP-AI/DataAcquisition/Equipment Specs/ChillerCapacity.csv', 
                 time = 0):
        self.a = 0 #regression_filepath - parse this for each constant
        self.b = 0 #regression_filepath
        self.c = 0 #regression_filepath
        self.CL = pd.read_csv(CL_filepath)[time]
        self.CL_Archive = pd.read_csv(CL_filepath)[time]
        self.RT = pd.read_csv(RT_filepath)['Tons'].values
        self.RT_Archive = pd.read_csv(RT_filepath)['Tons'].values
        self.min = 0.2
        self.lag = 0
    
    def lagrange(self):
        #Returns a single value given the nominal chiller tonage, RT, and coefficients from the regression, a,b,c
        self.lag = (2*self.CL+np.sum((self.b/self.c)*self.RT))/np.sum((self.RT**2)/self.c)
        return self.lag
    
    def PLR(self): 
        #Returns Numpy Array of PLR for each chiller
        PLR_ = (self.lagrange()*self.RT-self.b)/(2*self.c)
        return PLR_
    
    def PLR_corr(self):
        #PLR_Corrected: Array of all PLR's calculated fixing/removing any terms that violate the min/max constraint
        PLR_Corrected = self.PLR()    
        
        #Runs loop while PLR<Min or PLR>Max
        while np.count_nonzero((PLR_Corrected > 1) | ((PLR_Corrected < self.min) & (PLR_Corrected != 0))) > 0: 
        
            for i in len(PLR_Corrected):
                #### Minimum ####
                if PLR_Corrected[i] <=  self.min: #Minumum Value
                    PLR_Corrected[i] = 0 #Minumum Value                
                
                #### Maximum  ####  
                elif self.PLR_Corrected[i] >= 1: #Maximum Value
                    PLR_Corrected[i] = 1 #Maxiumum Value
                
            
            #RT_new: Returns an updated RT, elimniting the RT values of the chillers that violate the Max/Min threshold
            self.RT = self.RT_Archive[(PLR_Corrected >= self.min ) & (PLR_Corrected <= 1)]
            
            #### Assumes Method 2 for min b/c of how RT is summed ####
            #CL_new: Subtracts CL predicted from the updated PLR's RT value
            self.CL = self.CL_Archive - np.sum(self.RT_Archive[(PLR_Corrected >=1)])
            
            #lagrange_new: Returns new lagrange based off RT_new & CL_new
            lagrange_new = self.lagrange()
            
            #PLR_new: Returns new values of PLR using RT_new & lagrange_new
            PLR_new = self.PLR()
            
            #PLR_Corrected: Returns all PLR's correcting the values that did not violate the constrain with their new PLR (PLR_new)
            # and keeping chillers that were fixed to either 0 or 1
            PLR_Corrected[(PLR_Corrected >= self.min) & (PLR_Corrected <= 1)] = PLR_new
        
            
        return PLR_Corrected


if __name__ == '__main__':
   test = PLR_Calc(regression_filepath = 0, 
                 CL_filepath = 0, 
                 RT_filepath = '/Users/samueljon/Desktop/Desktop Folder/University of Arizona/Spring 2020/CHEE 443/CHRP-AI/DataAcquisition/Equipment Specs/ChillerCapacity.csv', 
                 time = 0)
   PLR_test = test.PLR_corr()
    
        

