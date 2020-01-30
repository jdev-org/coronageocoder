#!/usr/bin/env python
# -*- coding: utf-8 -*-
# version: 1.0
# licence : gpl-3.0 or superior
# author: Gaetan Bruel
# email: gaetan.bruel@jdev.fr
# date: 29/01/2020
# description : a geocoder according to this data https://docs.google.com/spreadsheets/d/1yZv9w9zRKwrGTaR-YzmAqMefw4wMlaXocejdxZaTs6w 

from geopy.geocoders import Nominatim
import urllib.request
import csv
from config import *
import json

print('DOWNLOAD CSV >>>>>>>>>>>')
outpathCsv = OUTPUTCSV
outputPathJson = OUTPUTJSON
urllib.request.urlretrieve(URL, INPUTFILE)

# geocode csv
# Inspired by https://blog.adrienvh.fr/

geocoder = Nominatim()
inputFile = open(INPUTFILE, 'rt')
outputFile = open(OUTPUTCSV, 'w')

# create base method to create json
def createJson():
  data = {}
  data['type'] = 'FeatureCollection'
  data['features'] = []
  return data

try:
  print('READ CSV FILE >>>>>>>>>>>')
  outputData = csv.writer(outputFile, delimiter = ',', lineterminator = '\n')
  outputData.writerow(('adresse', 'latitude', 'longitude'))
  inputData = csv.reader(inputFile, delimiter = ',')
  # ignore first line
  next(inputData)
  # init json
  data = createJson()
  for line in inputData:
    if line[0] and line[1]:
      adresse = line[0] + ", " + line[1]
    elif line[1]:
      adresse = line[1]
    try:
      print('GEOCODE >>>>>>>>>>>')
      cleanAdresse = adresse.replace('Mainland China', 'China')
      location = geocoder.geocode(cleanAdresse, True, 30)
      # add line to csv
      print('CREATE CSV >>>>>>>>>>>')
      outputData.writerow((line[0],line[1],line[2],line[3],line[4],line[5], location.latitude, location.longitude))
      print('CREATE JSON >>>>>>>>>>>')
      # prepare json data to append
      geometry = {
        'type':'Point',
        'coordinates': [location.longitude, location.latitude]
      }
      properties = {
        'location': adresse,
        'update': line[2],
        'confirmed': line[3],
        'deaths': line[4],
        'recovered': line[5]
      }
      data['features'].append({
        'type': 'Feature',
        'geometry': geometry,
        'properties': properties
      })
    except Exception as inst:
      print(inst)
  
  # export to geojson
  with open(OUTPUTJSON, 'w') as outfile:
    json.dump(data, outfile)

finally:
  inputFile.close()
  outputFile.close()