#!/usr/bin/env python
# -*- coding: utf-8 -*-
# version: 1.1
# licence : gpl-3.0 or superior
# author: Gaetan Bruel
# email: gaetan.bruel@jdev.fr
# date: 29/01/2020
# description : a geocoder according to this data https://docs.google.com/spreadsheets/d/1yZv9w9zRKwrGTaR-YzmAqMefw4wMlaXocejdxZaTs6w 
# change : 
#   replace source csv byhttps://docs.google.com/spreadsheets/d/1wQVypefm946ch4XDp37uZ-wartW4V7ILdg-qYiDXUHM
#   change date format to read PM/AM

from geopy.geocoders import Nominatim
import urllib.request
import csv, json
from config import *
from datetime import datetime
import sys

outpathCsv = OUTPUTCSV
outputPathJson = OUTPUTJSON
URL = sys.argv[1]
DELIMITER = sys.argv[2]
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
  outputData = csv.writer(outputFile, delimiter = ',', lineterminator = '\n')
  outputData.writerow(('state','country','date','confirmed','deaths','recovered', 'latitude', 'longitude'))
  inputData = csv.reader(inputFile, delimiter = DELIMITER)
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
      cleanAdresse = adresse.replace('Mainland China', 'China')
      location = geocoder.geocode(cleanAdresse, True, 30)
      # add line to csv
      date = line[2]
      formatDate = '%m/%d/%Y %H:%M'
      ampm = date[-2:].upper()
      if ampm == 'AM' or ampm == 'PM':
        formatDate += ' %p'  
      date = datetime.strptime(date, formatDate)
      if date.hour == 12 and ampm == 'AM':
            date.hour = '00'
      date = date.strftime('%Y-%m-%dT%H:%M:%S.%f')
      date = date[:-3]+'Z'

      outputData.writerow((line[0], line[1], date, line[3], line[4], line[5], location.latitude, location.longitude))
      # prepare json data to append
      geometry = {
        'type':'Point',
        'coordinates': [location.longitude, location.latitude]
      }
      properties = {
        'location': adresse,
        'date': date,
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
  exitValue = datetime.now().strftime('%Y-%m-%dT%H:%M%S.%f')[:-3]+'Z'
  print(exitValue)