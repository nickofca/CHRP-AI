#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 11 09:21:55 2020

Consider the following options:
    For including the daylong features (i.e. things that do not change minute by minute)
    3. Include the present features after the GRU layer.
    
    For the load output
    1. Use a deconvolutional layer after an initial fully connected. It is suggested that linear interpolation is used to improve deconvolution.
    2. Use a very wide fully connected layer (as wide as we want predictions to be resolute)

    For all layers
    - A variety of types of layers and hyperparameters
    - Different optimization methods
    - EarlyStopping?
    - Bagged model?
    
    
@author: nickofca
"""

import keras
import datetime

##Pertinent Variables
#Date of interest
day = datetime.date(2020,3,1)
nFeatures = 10

##Initialize the neural network
#Predictions/known information for the current day 
# Includes: Weather
presentFeatures = keras.Input((nFeatures,1441))    #Number of features by the number of minutes per day
presentCNN = keras.layers.Conv1D()(presentFeatures)

#Data for the past days
#Includes: Past load and weather
pastFeatures = [keras.Input((nFeatures,1441)) for day in range(7)]
pastCNN = [keras.layers.Conv1D()(pastFeature) for pastFeature in pastFeatures]

#Concatenate CNN outputs and run through a gated reccurent unit
pastCNN.append(presentCNN)
allCNN = keras.layers.concatenate(pastCNN)
GRU = keras.layers.GRU()(allCNN)

#TODO: Consider a deconv layer
#Deconv = keras.layers.Deconv1D()(GRU)

#Fully connected section
dense1 = keras.layers.Dense((32))(GRU)
dense2 = keras.layers.Dense((64))(dense1)
dense3 = keras.layers.Dense((1441))(dense2)

#Assemble and compile the overall model
model = keras.models.Model(inputs=[presentFeatures,pastFeatures], outputs=[dense3])
model.compile()

model.fit()

