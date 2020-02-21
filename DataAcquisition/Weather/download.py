#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 21 10:46:08 2020

@author: nickofca
"""

import pandas as pd
import datetime

def pull(year):
    pd.date_range(datetime.date(year,1,1))
    