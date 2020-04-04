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
from DataAcquisition.dataStream import dataStream
import pandas as pd
import keras.backend as back
import math

##Data Preprocessing 
#Seperate the training and testing days
#In order to prevent data leakage, training load should not come be mixed with testing (even for the past week data streams)
trainDates = pd.date_range(datetime.date(2019,2,19),datetime.date(2019,3,30))
testDates = pd.date_range(datetime.date(2019,12,7),datetime.date(2020,2,12))

##Pertinent Variables
#Date of interest
day = datetime.date(2020,3,1)
minutelyFeatures = 9
dailyFeatures = 2
batch_size = 10

##Initialize the neural network
#Predictions/known information for the current day and past week 
# Includes: Weather
#Includes: Past load and weather
minutelyInput = [keras.Input((720,minutelyFeatures)) for day in range(7)]
CNNs = [keras.layers.SeparableConv1D(filters=32, kernel_size=4, data_format="channels_first")(minutelyInput) for minutelyInput in minutelyInput]

#Concatenate CNN outputs and run through a gated reccurent unit
cat = keras.layers.Concatenate()(CNNs)
GRU = keras.layers.Bidirectional(keras.layers.GRU(16,return_sequences=True))(cat)

#TODO: Consider a deconv layer
#Deconv = keras.layers.Deconv1D()(GRU)

#Daily features
dailyInput = keras.Input((7,dailyFeatures))

#Flatten both layers
flatDaily = keras.layers.Flatten()(dailyInput)
flatMinutely = keras.layers.Flatten()(GRU)

#Combine daily and minutely data streams
cat = keras.layers.concatenate([flatDaily,flatMinutely])

#Fully connected section
dense1 = keras.layers.Dense((32))(cat)
dense2 = keras.layers.Dense((64))(dense1)
dense3 = keras.layers.Dense((720))(dense2)

#Assemble and compile the overall model
model = keras.models.Model(inputs=[dailyInput]+minutelyInput, outputs=dense3)
keras.utils.plot_model(model, show_shapes = True, to_file="model.png")
keras.utils.plot_model(model, to_file="modelNoLabels.png")

model.compile(loss='mean_squared_error', optimizer = "adagrad")

model.fit_generator(dataStream().generate(trainDates, batch_size=batch_size),steps_per_epoch=math.floor(len(trainDates)/batch_size), epochs= 25, 
                    validation_data =  dataStream().generate(testDates, batch_size=batch_size), validation_steps= math.floor(len(trainDates)/batch_size))

