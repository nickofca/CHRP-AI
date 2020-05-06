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
from Tools.Tools import dataSplitting
import pandas as pd
import math
import tensorflow as tf
import numpy as np

#TODO: Get weeks of the year and shuffle them into training and test


class LoadForecast():
    def __init__(self, dateRange = pd.date_range(datetime.date(2019,2,19),datetime.date(2020,2,11)), testingFrac = .1):
        #Initialize data stream
        self.ds = dataStream(hourly = True)
        
        ##Construct model architecture    
        ##Data Preprocessing 
        #Seperate the training and testing days
        #In order to prevent data leakage, training load should not come be mixed with testing (even for the past week data streams)
        self.testingFrac = testingFrac
        self.trainDates, self.testDates = dataSplitting(dateRange, testingFrac)
        
        ##Pertinent Variables
        #Date of interest
        self.minutelyFeatures = 9
        self.dailyFeatures = 2
        self.batch_size = 20
        self.epochs = 10
        
        self.conv_filters = 16
        self.kernel_size = 16
        self.conv_layers = 3

        self.dense_daily_size = 16        
        self.dense_daily_layers = 2
        
        self.dense_size = 64
        self.dense_layers = 2
        
        
        ##Initialize the neural network
        #Predictions/known information for the current day and past week 
        # Includes: Weather
        #Includes: Past load and weather
        hourlyInput = keras.Input((168,self.minutelyFeatures))

        ##Convolutional layers
        CNNs = [keras.layers.Conv1D(filters=self.conv_filters, kernel_size = kSize*3 + 3, padding = "same", data_format = "channels_last")(hourlyInput) for kSize in range(3)]
        pools = [keras.layers.MaxPool1D(data_format = "channels_last")(CNN) for CNN in CNNs]

        #Concatenate CNN outputs and run through a gated reccurent unit
        cat = keras.layers.Concatenate(axis = 1)(pools)
        GRU = keras.layers.Bidirectional(keras.layers.GRU(16, return_sequences=True))(cat)
        
        #Take the mean of each layer
        hourly = keras.layers.Lambda(keras.backend.mean, arguments={"axis":1})(GRU)
        
        #Daily features
        dailyInput = keras.Input((7,self.dailyFeatures))
        denseDaily = keras.layers.Dense((self.dense_daily_size))(dailyInput)
        for i in range(self.dense_daily_layers-1):
            denseDaily = keras.layers.Dense((self.dense_daily_size))(denseDaily)
            
        #Flatten both layers
        flatDaily = keras.layers.Flatten()(denseDaily)
        
        #Combine daily and minutely data streams
        cat = keras.layers.concatenate([flatDaily, hourly])
        
        #Fully connected section
        dense = keras.layers.Dense((self.dense_size))(cat)
        for i in range(self.dense_layers-1):
            dense = keras.layers.Dense((self.dense_size))(dense)
        out = keras.layers.Dense((24))(dense)
        
        #Assemble and compile the overall model
        self.model = keras.models.Model(inputs=[dailyInput,hourlyInput], outputs=out)
        
        #Set the pertinent optimization parameters
        self.model.compile(loss='mean_squared_error', optimizer = "adam", metrics=['mae'])
        
    def train(self, batch_size = None, epochs = None):
        #Fill in parameters with 
        if batch_size == None:
            batch_size = self.batch_size
        
        #Train the model
        self.history = self.model.fit_generator(self.ds.generate(self.trainDates, batch_size=self.batch_size),
                                                steps_per_epoch = math.floor(len(self.trainDates)/self.batch_size),
                                                epochs= self.epochs,
                                                validation_data = self.ds.generate(self.testDates, batch_size=self.batch_size), 
                                                validation_steps= math.floor(len(self.trainDates)/self.batch_size))
    
    def save(self, modelDir = "../Models/modelPaperMod.h5", withHist = True):
        #Save the model
        if withHist:
            lastMAE = self.history.history["val_mean_absolute_error"][-1]
            modelDir = "../Models/model_valMAE_" + str(lastMAE)[:8] + ".h5"
        self.model.save(modelDir)
        
    def plot(self, imageDir = "../Figures/modelPaperMod.png"):
        #Plot the model with and without edges.
        keras.utils.plot_model(self.model, show_shapes = True, to_file= imageDir)
        
    def load(self, modelDir = "../Models/modelPaperMod.h5"):
        #Load the model from the specified directory
        self.model = keras.models.load_model(modelDir, custom_objects={'tf': tf})

    def evaluate(self,length = "all"):
        if length == "all":
            length = len(self.testDates)
        self.testTruth = next(self.ds.generate(self.testDates[0:length],length))[1]
        self.testPrediction = self.model.predict_generator(self.ds.generate(self.testDates,length),steps = 1)
        self.error = self.testTruth - self.testPrediction
        self.pctErrorDF = self.error / self.testTruth
        self.pctError = np.mean(np.abs(self.pctErrorDF))
        
if __name__ == '__main__':
    train = True
    initialize = True
    if initialize:
        lfPaper = LoadForecast()
    if train:
        lfPaper.train()
        lfPaper.save(withHist = False)
    #Real Values of a sample out of test
    lfPaper.evaluate("all")
    error = lfPaper.error
    pctError = lfPaper.pctError
    
        
        