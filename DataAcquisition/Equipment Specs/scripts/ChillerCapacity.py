#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 15 11:20:33 2020

@author: samueljon
"""

import pandas as pd

ChillerCapacity = pd.read_excel('/Users/samueljon/Desktop/Desktop Folder/University of Arizona/Spring 2020/CHEE 443/Chiller Capacity.xlsx' ,sheet_name = 'Capacity')
ChillerCapacity.to_csv('ChillerCapacity.csv', index = False)

class chillercap(object):
    
    def __init__(self,  plant = 'AHSC', chillernumber = 1, file = '/Users/samueljon/Desktop/Desktop Folder/University of Arizona/Spring 2020/CHEE 443/CHRP-AI/DataAcquisition/Equipment Specs/ChillerCapacity.csv'):
        self.plant = plant
        self.chillernumber = chillernumber
        self.data = pd.read_csv(file)
        
    def capacity(self):
        capacity = self.data.set_index(['Plant', 'Chiller'])
        cap = capacity.loc[self.plant].loc[self.chillernumber]['Tons']
        return cap

if __name__ == '__main__':
    ch_cap = chillercap(plant = 'AHSC', chillernumber = 1, file = '/Users/samueljon/Desktop/Desktop Folder/University of Arizona/Spring 2020/CHEE 443/CHRP-AI/DataAcquisition/Equipment Specs/ChillerCapacity.csv')
    chiller_capacity = ch_cap.capacity()