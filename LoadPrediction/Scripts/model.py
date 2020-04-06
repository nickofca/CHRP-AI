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
import math


class LoadForecast():
    def __init__(self, trainDates = pd.date_range(datetime.date(2019,2,19),datetime.date(2019,3,30)),
                 testDates = pd.date_range(datetime.date(2019,12,7),datetime.date(2020,2,11))):
        ##Construct model architecture    
        ##Data Preprocessing 
        #Seperate the training and testing days
        #In order to prevent data leakage, training load should not come be mixed with testing (even for the past week data streams)
        self.trainDates = trainDates
        self.testDates = testDates
        
        ##Pertinent Variables
        #Date of interest
        self.minutelyFeatures = 9
        self.dailyFeatures = 2
        self.batch_size = 10
        
        ##Initialize the neural network
        #Predictions/known information for the current day and past week 
        # Includes: Weather
        #Includes: Past load and weather
        minutelyPresentInput = [keras.Input((1441,self.minutelyFeatures-1))]
        minutelyPastInput = [keras.Input((720,self.minutelyFeatures)) for day in range(1,7)]
        minutelyInput = minutelyPresentInput + minutelyPastInput
        CNNs = [keras.layers.SeparableConv1D(filters=3, kernel_size=4, data_format="channels_first")(minutelyInput) for minutelyInput in minutelyInput]
        
        #Concatenate CNN outputs and run through a gated reccurent unit
        cat = keras.layers.Concatenate()(CNNs)
        GRU = keras.layers.Bidirectional(keras.layers.GRU(16,return_sequences=True))(cat)
        
        #TODO: Consider a deconv layer
        #Deconv = keras.layers.Deconv1D()(GRU)
        
        #Daily features
        dailyInput = keras.Input((7,self.dailyFeatures))
        
        #Flatten both layers
        flatDaily = keras.layers.Flatten()(dailyInput)
        flatMinutely = keras.layers.Flatten()(GRU)
        
        #Combine daily and minutely data streams
        cat = keras.layers.concatenate([flatDaily,flatMinutely])
        
        #Fully connected section
        dense1 = keras.layers.Dense((16))(cat)
        dense2 = keras.layers.Dense((16))(dense1)
        dense3 = keras.layers.Dense((24))(dense2)
        
        #Assemble and compile the overall model
        self.model = keras.models.Model(inputs=[dailyInput]+minutelyInput, outputs=dense3)
        
        #Set the pertinent optimization parameters
        self.model.compile(loss='mean_squared_error', optimizer = "adagrad", metrics=['mse'])
        
    def train(self, batch_size = None):
        if batch_size == None:
            batch_size = self.batch_size
        #Train the model
        self.model.fit_generator(dataStream().generate(self.trainDates, batch_size=self.batch_size),steps_per_epoch=math.floor(len(self.trainDates)/self.batch_size), epochs= 25, 
                            validation_data =  dataStream().generate(self.testDates, batch_size=self.batch_size), validation_steps= math.floor(len(self.trainDates)/self.batch_size))
    
    def save(self, modelDir = "../Models/model.h5"):
        #Save the model
        self.model.save(modelDir)
        
    def plot(self, imageDir = "model.png"):
        #Plot the model with and without edges.
        keras.utils.plot_model(self.model, show_shapes = True, to_file= imageDir)
        