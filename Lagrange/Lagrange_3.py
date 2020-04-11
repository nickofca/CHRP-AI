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
    
    def __init__(self, regression_filepath = '/Users/samueljon/Desktop/Desktop Folder/University of Arizona/Spring 2020/CHEE 443/CHRP-AI/Lagrange/cop_plr_regression2.csv', 
                 CL_filepath = 0, 
                 RT_filepath = '/Users/samueljon/Desktop/Desktop Folder/University of Arizona/Spring 2020/CHEE 443/CHRP-AI/DataAcquisition/Equipment Specs/ChillerCapacity.csv',
                 Ice_filepath = '/Users/samueljon/Desktop/Desktop Folder/University of Arizona/Spring 2020/CHEE 443/CHRP-AI/DataAcquisition/Equipment Specs/IceChillerCapacity.csv',
                 time = 0):
        self.a = pd.read_csv(regression_filepath).loc[:,'a']
        self.b = pd.read_csv(regression_filepath).loc[:,'b']
        self.c = pd.read_csv(regression_filepath).loc[:,'c']
        self.a_Archive = pd.read_csv(regression_filepath).loc[:,'a']
        self.b_Archive = pd.read_csv(regression_filepath).loc[:,'b']
        self.c_Archive = pd.read_csv(regression_filepath).loc[:,'c']
        #self.CL = pd.read_csv(CL_filepath)[time]
        #self.CL_Archive = pd.read_csv(CL_filepath)[time]
        self.CL = 5000 #Delete these, just for test purposes
        self.CL_Archive = 5000 #Delete these, just for test purposes
        self.Plant = pd.read_csv(RT_filepath)['Plant']
        self.ChillerNum = pd.read_csv(RT_filepath)['Chiller']
        self.RT = pd.read_csv(RT_filepath)['Tons'].values
        self.RT_Archive = pd.read_csv(RT_filepath)['Tons'].values
        self.Ice = pd.read_csv(Ice_filepath)['Tons'].values
        self.min = 0.2
        self.lag = 0
    
    def lagrange(self):
        #Returns a single value given the nominal chiller tonage, RT, and coefficients from the regression, a,b,c
        self.lag = (2*self.CL+np.sum((self.b/self.c)*self.RT))/np.sum((self.RT**2)/self.c)
        return self.lag
    
    def PLR(self): 
        #Returns Numpy Array of PLR for each chiller
        self.PLR_ = (self.lagrange()*self.RT-self.b)/(2*self.c)
        return self.PLR_
    
    def PLR_corr(self, ice = False):
        #PLR_Corrected: Array of all PLR's calculated fixing/removing any terms that violate the min/max constraint
                    
        self.PLR_Corrected = self.PLR()
       
        
        #Runs loop while PLR<Min or PLR>Max
        while np.count_nonzero( (np.isnan(self.PLR_Corrected)) | (self.PLR_Corrected > 1) | ((self.PLR_Corrected < self.min) & (self.PLR_Corrected != 0))) > 0:
        
            for i in range(len(self.PLR_Corrected)):
                #### Minimum ####
                if self.PLR_Corrected[i] <=  self.min: #Minumum Value
                   self.PLR_Corrected[i] = 0 #Minumum Value                
                
                #### Maximum  ####  
                elif self.PLR_Corrected[i] >= 1: #Maximum Value
                   self.PLR_Corrected[i] = 1 #Maxiumum Value
                   
                #### NaN #####
                elif np.isnan(self.PLR_Corrected[i]) == True: #If any NaN values replace these with 0
                    self.PLR_Corrected[i] = 0 
                
            
            #RT_new: Returns an updated RT, elimniting the RT values of the chillers that violate the Max/Min threshold
            self.RT = self.RT_Archive[(self.PLR_Corrected >= self.min ) & (self.PLR_Corrected <= 1)]
            
            #Regression Constants indexed to match RT_new
            self.a = self.a_Archive[(self.PLR_Corrected >= self.min ) & (self.PLR_Corrected <= 1)]
            self.b = self.b_Archive[(self.PLR_Corrected >= self.min ) & (self.PLR_Corrected <= 1)]
            self.c = self.c_Archive[(self.PLR_Corrected >= self.min ) & (self.PLR_Corrected <= 1)]
            
            
            #CL_new: Subtracts CL predicted from the updated PLR's RT value
            #Temporary: If Ice is being used subtract predicted CL from sum of Ice capacity along with sum of chiller at max capacity
            if ice:
                self.CL = self.CL_Archive - np.sum(self.RT_Archive[(self.PLR_Corrected >=1)]) - np.sum(self.Ice)
            else:
                self.CL = self.CL_Archive - np.sum(self.RT_Archive[(self.PLR_Corrected >=1)])
            
            #lagrange_new: Returns new lagrange based off RT_new & CL_new
            lagrange_new = self.lagrange()
            
            #PLR_new: Returns new values of PLR using RT_new & lagrange_new
            PLR_new = self.PLR()
            
            #PLR_Corrected: Returns all PLR's correcting the values that did not violate the constrain with their new PLR (PLR_new)
            # and keeping chillers that were fixed to either 0 or 1
            self.PLR_Corrected[(self.PLR_Corrected >= self.min) & (self.PLR_Corrected <= 1)] = PLR_new
        
        
        FinalRes = pd.concat([self.Plant, self.ChillerNum, self.PLR_Corrected], keys = ['Plant', 'Chiller', 'PLR Value'], axis =1)
        print(FinalRes.to_string(index = False))
        #print(pd.concat([self.Plant, self.ChillerNum, self.PLR_Corrected], axis =1).to_string(index = False))
        return self.PLR_Corrected 
        
        
        


if __name__ == '__main__':
   test = PLR_Calc(regression_filepath = '/Users/samueljon/Desktop/Desktop Folder/University of Arizona/Spring 2020/CHEE 443/CHRP-AI/Lagrange/cop_plr_regression2.csv', 
                 CL_filepath = 5000, 
                 RT_filepath = '/Users/samueljon/Desktop/Desktop Folder/University of Arizona/Spring 2020/CHEE 443/CHRP-AI/DataAcquisition/Equipment Specs/ChillerCapacity.csv', 
                 time = 0)
   PLR_test = test.PLR_corr()
    
        

