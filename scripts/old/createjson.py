#!/usr/bin/env python
# -*- coding: utf-8 -*-
# version: 1.0
# licence : gpl-3.0 or superior
# author: JDev
# email: gaetan.bruel@jdev.fr
# date: 29/01/2020
# description : a geocoder according to this data https://docs.google.com/spreadsheets/d/1yZv9w9zRKwrGTaR-YzmAqMefw4wMlaXocejdxZaTs6w 

from os import listdir, getcwd
from os.path import isfile, join
import csv, json
from geopy.geocoders import Nominatim
from config import *
import urllib.request

PATH = getcwd() + DATAPATH
n = 1 

##
# use geocoder to get XY fro address
# #
def geocode(address):
  geocoder = Nominatim()
  # geocode
  location = geocoder.geocode(address, True, 30)
  return location

##
# create simple geojson base
# #
def createJson():
  json = {}
  json['type'] = 'FeatureCollection'
  json['features'] = []
  return json

##
# create json properties from feature infos
# #
def locationToJson(line, location, colNames):
  i = 0
  properties = {}
  # geom
  geometry = {
    'type':'Point',
    'coordinates': [location.longitude, location.latitude]
  }

  # get properties from col
  for col in colNames:    
    # save props
    properties[col] = line[i]
    # join json
    i+=1
  feature = {
    'type': 'Feature',
    'geometry': geometry,
    'properties': properties
  }
  return feature

##
# from line, get location
# #
def getLocation(line) :
  # clean adress
  adresse = ''
  if line[0] and line[1]:
    adresse = line[0] + ", " + line[1]
  elif line[1]:
    adresse = line[1]
  adresse = adresse.replace('Mainland China', 'China')
  # geocode
  location = geocode(adresse)
  # create feature for json
  return location

##
# read and convert csv feature to geojson
# #
def csvToJson(fPath, delimiter):
  inputFile = open(fPath, 'rt')      
  inputData = csv.reader(inputFile, delimiter = delimiter)
  outputData = csv.writer(outputFile, delimiter = ',', lineterminator = '\n')
  colNames = next(inputData)
  for line in inputData:
    location = getLocation(line)
    feature = locationToJson(line, location, colNames)
    outJson['features'].append(feature)

outJson = createJson()

# parse files from dir
for f in listdir(PATH):
  if isfile(join(PATH,f)):
    print('READ FILE' + str(n) + '>>>>')
    try:
      csvToJson(join(PATH,f),';')
    except Exception as inst:
      print(inst)
    n = n + 1

# parse file from web
print('GET CSV FROM WEB >>>>')
urllib.request.urlretrieve(URL, INPUTFILE)
print('GEOCODE FILE >>>>')
csvToJson(INPUTFILE, ',')

# export json to file
with open(OUTPUTJSON, 'w') as outfile:
  json.dump(outJson, outfile)

print('END SCRIPT >>>>')