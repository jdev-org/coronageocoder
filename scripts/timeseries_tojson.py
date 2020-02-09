#!/usr/bin/env python
# -*- coding: utf-8 -*-
# version: 1.0
# licence : gpl-3.0 or superior
# author: Gaetan Bruel
# email: gaetan.bruel@jdev.fr
# date: 29/01/2020
# description : create JSON from time series data https://docs.google.com/spreadsheets/d/1UF2pSkFTURko2OvfHWWlFpDFAr1UxCBA4JLwlSP6KFo


import urllib.request
import csv, json
from config import *
from datetime import datetime
import sys


outpathCsv = OUTPUTCSV
outputPathJson = OUTPUTJSON
DELIMITER = sys.argv[2]
URLTS = sys.argv[1]
finalMsg = 'SUCCESS'

# create base method to create json
def createJson():
  data = {}
  data['type'] = 'FeatureCollection'
  data['features'] = []
  return data

def reformatDate(value):
  formatDate = '%m/%d/%Y %I:%M'
  if '2020' not in value:
        formatDate = '%m/%d/%y %H:%M'
  ampm = value[-2:].upper()
  if ampm == 'AM' or ampm == 'PM':
    formatDate += ' %p'  
  date = datetime.strptime(value, formatDate)
  if date.hour == 12 and ampm == 'AM':
        date.hour = '00'
  date = date.strftime('%Y-%m-%dT%H:%M:%S.%f')
  date = date[:-3] + 'Z'
  return date

# line to json
def createJsonFeatures(line, colNames):
  features = []
  c = 5
  cols = colNames[c:]
  for name in cols:
      properties = {
        'state': line[0],
        'country': line[1],
        'date': reformatDate(name),
        'confirmed': line[c]
      }
      geometry = {
        'type':'Point',
        'coordinates': [float(line[4]), float(line[3])]
      }
      feature = {
        'type': 'Feature',
        'geometry': geometry,
        'properties': properties
      }
      features.append(feature)
      c = c + 1
  return features    

urllib.request.urlretrieve(URLTS, INPUTFILE) # GET DATA FROM WEB

inputFile = open(INPUTFILE, 'rt') #READ THIS FILE
outputFile = open(OUTPUTCSV, 'w') #WRITE THIS FILE

jsonData = createJson()

try:
  # input file
  inputData = csv.reader(inputFile, delimiter = DELIMITER)
  colNames = next(inputData)
  # prepare output csv file
  outputData = csv.writer(outputFile, delimiter = ';', lineterminator = '\n')
  # csv header
  outputData.writerow(('state', 'country', 'long', 'lat', 'date', 'confirmed'))
  for line in inputData:
      # CSV
      i = 0
      for cell in line:
        if(i >= 5 and cell != ''):
          outputData.writerow((line[0], line[1], line[3], line[4], reformatDate(colNames[i]), cell))
        i += 1
      # JSON
      jsonFeatures = createJsonFeatures(line, colNames)
      for feature in jsonFeatures:
        jsonData['features'].append(feature)
  with open(OUTPUTJSON, 'w') as outfile:
    json.dump(jsonData, outfile)      
    
except Exception as inst:
  print(inst)
  finalMsg = 'ERROR'

finally:
  inputFile.close()
  outputFile.close()
  exitValue = datetime.now().strftime('%Y-%m-%d')
  print(exitValue)