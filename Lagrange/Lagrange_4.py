#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 21 10:17:06 2020

@author: samueljon
"""
import pandas as pd
import numpy as np


# =============================================================================
#
#           CL : Predicted cooling load
#           RT : Capacity of  ith chiller
#           Ice : Capacity of ith ice chiller
#           COP : Coefficient of Performance (chiller cooling load to power consumption)
#           PLR : Part Load Ratio (chiller cooling load to nominal capacity)
#           time : hourly time from 0-24. 0 is 12AM, 12 is 12PM, 24 is 11PM
#           a,b,c : regression coefficients of second degree polynomial (a+bx+cx^2)
#           dT : temperature differential in Fahrenheit
#           GPMmin : Minimum GPM for each chiller set by UA Facilities & chiller limitation
#           
# =============================================================================


class PLR_Calc(object):
    '''
    CL : Predicted cooling load
    RT : Capacity of  ith chiller
    Ice : Capacity of ith ice chiller
    COP : Coefficient of Performance (chiller cooling load to power consumption)
    PLR : Part Load Ratio (chiller cooling load to nominal capacity)
    time : hourly time from 0-24. 0 is 12AM, 12 is 12PM, 24 is 11PM
    a,b,c : regression coefficients of third degree polynomial (a+bx+cx^2)
    dT : AvgTemp per hour in Fahrenheit 
    GPMmin : Minimum GPM for each chiller set by UA Facilities & chiller limitation
    '''
    def __init__(self, dT_ahsc = 7,
                 dT_crb = 5,
                 dT_chrp = 6,
                 regression_filepath = '/Users/samueljon/Desktop/Desktop Folder/University of Arizona/Spring 2020/CHEE 443/CHRP-AI/Lagrange/regression_coefficients_ss200.csv', 
                 CL_filepath = 5000, 
                 RT_filepath = '/Users/samueljon/Desktop/Desktop Folder/University of Arizona/Spring 2020/CHEE 443/CHRP-AI/DataAcquisition/Equipment Specs/ChillerCapacity.csv',
                 Ice_filepath = '/Users/samueljon/Desktop/Desktop Folder/University of Arizona/Spring 2020/CHEE 443/CHRP-AI/DataAcquisition/Equipment Specs/IceChillerCapacity.csv',
                 GPMmin_filepath = '/Users/samueljon/Desktop/Desktop Folder/University of Arizona/Spring 2020/CHEE 443/CHRP-AI/Lagrange/ChillerMinEvap.csv',
                 #WPD _filepath = 0,
                 time = 0):
        self.dT = np.append(np.append(np.repeat(abs(dT_ahsc),6),np.repeat(abs(dT_crb),6)),np.repeat(abs(dT_chrp),6))
        self.a = pd.read_csv(regression_filepath).loc[:,'a']
        self.b = pd.read_csv(regression_filepath).loc[:,'b']
        self.c = pd.read_csv(regression_filepath).loc[:,'c']
        self.a_Archive = pd.read_csv(regression_filepath).loc[:,'a']
        self.b_Archive = pd.read_csv(regression_filepath).loc[:,'b']
        self.c_Archive = pd.read_csv(regression_filepath).loc[:,'c']
        #self.CL = pd.read_csv(CL_filepath)[time]
        #self.CL_Archive = pd.read_csv(CL_filepath)[time]
        self.CL = CL_filepath #Delete these, just for test purposes
        self.CL_Archive = CL_filepath #Delete these, just for test purposes
        self.Plant = pd.read_csv(RT_filepath)['Plant']
        self.ChillerNum = pd.read_csv(RT_filepath)['Chiller']
        self.RT = pd.read_csv(RT_filepath)['Tons'].values
        self.RT_Archive = pd.read_csv(RT_filepath)['Tons'].values
        self.GPM_min = pd.read_csv(GPMmin_filepath)['GPM'].values
        #self.WPD1 pd.read_csv(WPD_filepath).loc[:,'WPD1']
        #self.WPD2 pd.read_csv(WPD_filepath).loc[:,'WPD2']
        self.Ice = pd.read_csv(Ice_filepath)['Tons'].values
        self.lag = 0 #Initialize lagrange
    
    def lagrange(self):
        #Returns a single value lagrange multiplier given RT, and a,b,c
        self.lag = (2*self.CL+np.sum((self.b/self.c)*self.RT))/np.sum((self.RT**2)/self.c)
        return self.lag
    
    def PLR(self): 
        #Returns Numpy Array of PLR for each chiller given lagrange, RT and b,c
        self.PLR_ = (self.lagrange()*self.RT-self.b)/(2*self.c)
        #print(self.PLR_.tolist()) #Remove hashtag to monitor inital PLR values 
        return self.PLR_
    
    def PLR_corr(self, ice = False):
        
        #PLR_Corrected: Array of all PLR's calculated fixing/removing any terms that violate the min/max constraint
        self.PLR_Corrected = self.PLR()
        
        
        #Conversion from PLR to GPM
        # ( 12000 BTU/hr / 1 Ref. Tons * Load/Max Load ) / ( (8.33 pounds * 60 minutes) * dT )
        self.GPM = (12000*self.PLR_Corrected*self.RT_Archive)/(500*self.dT)
        
        #if any dT are below 1 replace GPM with 0 and the corresponding dT with 1
        #Based on histroical data, dT < 1 inidicates the chillrs were off and need to be accounted for since
        #GPM is inverseely proportional to temperature resulting in NaN
        if any(self.dT<1):
            self.GPM[(self.dT<1)] = 0
            self.dT[(self.dT<1)] = 1
        
        #If Ice is true, subtract CL from the sum of all ice units, note this can be expanded in future projects to better
        #Handle thermal storage units 
        if ice:
                self.CL = self.CL_Archive - np.sum(self.Ice)
        
        
        #Runs loop while GPM<GPM_min or PLR>1
        while np.count_nonzero( ((self.GPM < self.GPM_min) & (self.GPM != 0)) | (self.PLR_Corrected > 1)) > 0:
            
            #for i in length of PLR_Corrected (18)
            for i in range(len(self.PLR_Corrected)):
               
                #### Minimum ####
                #Replace GPM values calculated less than the minimum GPM specified with 0
                #Chiller is deemed offline
                if self.GPM[i] < self.GPM_min[i]:
                    self.PLR_Corrected[i] = 0            
                
                
                #### NaN #####
                #If any PLR or GPM are NaN or GPM is inf replace PLR with 0 
                elif (np.isnan(self.PLR_Corrected[i])) | (np.isnan(self.GPM[i])) | (np.isinf(self.GPM[i])) == True:
                    self.PLR_Corrected[i] = 0 
                    
                    
                #### Maximum  ####   
                #Replace PLR values above 1 with 1
                elif self.PLR_Corrected[i] >= 1: #Maximum Value
                   self.PLR_Corrected[i] = 1 #Maxiumum Value
                   
            
            #self.RT replaces itself with RT values of the chillers that do not violate the Max/Min threshold
            self.RT = self.RT_Archive[(self.PLR_Corrected > 0) & (self.PLR_Corrected < 1)]
            
            #Regression Constants indexed to match new self.RT
            self.a = self.a_Archive[(self.PLR_Corrected > 0 ) & (self.PLR_Corrected < 1)]
            self.b = self.b_Archive[(self.PLR_Corrected > 0 ) & (self.PLR_Corrected < 1)]
            self.c = self.c_Archive[(self.PLR_Corrected > 0 ) & (self.PLR_Corrected < 1)]
            
            #self.CL: subtracts CL_Archive (original CL input) from chillers that are running at max capacity (PLR = 1)
            self.CL = self.CL_Archive - np.sum(self.RT_Archive[(self.PLR_Corrected == 1)])
            
            #lagrange_new: Returns new lagrange based off new self.RT & self.CL
            #Not necessary 
            lagrange_new = self.lagrange()
            
            #PLR_new: Returns new values of PLR using new self.RT & self.lagrange 
            PLR_new = self.PLR()
            
            #PLR_Corrected: Returns all PLR's correcting the values that did not violate the constrain with their new PLR (PLR_new)
            # and keeping chillers that were fixed to either 0 or 1
            self.PLR_Corrected[(self.PLR_Corrected > 0) & (self.PLR_Corrected < 1)] = PLR_new
            
            #Recalculates GPM using new PLR values
            self.GPM = (12000*self.PLR_Corrected*self.RT_Archive)/(500*self.dT)
            
            #Used to monitor PLR values as it iterates through the while loop
            print(self.PLR_Corrected.tolist())
            
        #dP: Converts GPM to operational values, dP using WPD 1 & 2 coefficients
        #dP = self.WPD1*(self.GPM**self.WPD2)
        
        #self.kW: Calcualtes the kW for each individual chiller
        self.kW = (self.a_Archive+self.b_Archive*self.PLR_Corrected+self.c_Archive*self.PLR_Corrected**2)*(self.PLR_Corrected*self.RT_Archive)
        
        #Print the final results & return PLR_Corrected
        FinalRes = pd.concat([self.Plant, self.ChillerNum, self.PLR_Corrected, self.GPM, self.kW], keys = ['Plant', 'Chiller', 'PLR Value', 'GPM', 'kW'], axis =1)
        print(FinalRes.to_string(index = False))
        print("Total kW:", np.sum(self.kW))
        print("Is CL met?", round(sum(self.PLR_Corrected*self.RT_Archive),2) == round(self.CL_Archive,2))
        print("Calculated CL is ",round(sum(self.PLR_Corrected*self.RT_Archive),2))
        return self.PLR_Corrected

if __name__ == '__main__':
   test = PLR_Calc(dT_ahsc = 13.65982258064520,
                 dT_crb = 12.141870967741900,
                 dT_chrp = 13.335096774193600,
                 CL_filepath = 11097.362290322600)
   PLR_test = test.PLR_corr()


