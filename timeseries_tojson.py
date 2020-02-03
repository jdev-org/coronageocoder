#!/usr/bin/env python
# -*- coding: utf-8 -*-
# version: 1.0
# licence : gpl-3.0 or superior
# author: Gaetan Bruel
# email: gaetan.bruel@jdev.fr
# date: 29/01/2020
# description : create JSON from time series data https://docs.google.com/spreadsheets/d/1UF2pSkFTURko2OvfHWWlFpDFAr1UxCBA4JLwlSP6KFo


from geopy.geocoders import Nominatim
import urllib.request
import csv, json
from config import *
from datetime import datetime
import sys


print('DOWNLOAD CSV >>>>>>>>>>>')
outpathCsv = OUTPUTCSV
outputPathJson = OUTPUTJSON
DELIMITER = sys.argv[2]
finalMsg = 'NO ERROR'

# create base method to create json
def createJson():
  data = {}
  data['type'] = 'FeatureCollection'
  data['features'] = []
  return data


# line to json
def createJsonFeatures(line, colNames):
  features = []
  properties = {
      'state': line[0],
      'country': line[1]
  }
  geometry = {
    'type':'Point',
    'coordinates': [line[3], line[4]]
  }
  # create one feature by date
  i = 0
  for cell in line:
      if(i >= 6):
        date = datetime.strptime(colNames[i], '%m/%d/%Y %H:%M %p').strftime('%Y-%m-%dT%H:%M%S.%f')
        date = date[:-3]+'Z' 
        properties['date'] = date # date
        properties['confirmed'] = cell
        feature = {
          'type': 'Feature',
          'geometry': geometry,
          'properties': properties
        }
        features.append(feature)
      i += 1
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
  outputData = csv.writer(outputFile, delimiter = DELIMITER, lineterminator = '\n')
  # csv header
  outputData.writerow(('state', 'country', 'lat', 'long', 'date', 'confirmed'))
  print('CSV FILE >>>>>>>>>>>')
  for line in inputData:
      # CSV
      i = 0
      for cell in line:
        if(i >= 5 and cell != ''):
          date = datetime.strptime(colNames[i], '%m/%d/%Y %I:%M %p').strftime('%Y-%m-%dT%H:%M%S.%f')
          date = date[:-3]+'Z' 
          outputData.writerow((line[0], line[1], line[3], line[4], date, cell))
        i += 1
      # JSON
      jsonFeatures = createJsonFeatures(line, colNames)
      jsonData['features'].append(jsonFeatures)
  print('JSON FILE >>>>>>>>>>>')
  with open(OUTPUTJSON, 'w') as outfile:
    json.dump(jsonData, outfile)      
    
except Exception as inst:
  print(inst)
  finalMsg = 'ERROR'

finally:
  print('CLOSE FILES >>>>>>>>>>>')
  inputFile.close()
  outputFile.close()
  print('END SCRIPT WITH ' + finalMsg + '>>>>>>>>>>>')

