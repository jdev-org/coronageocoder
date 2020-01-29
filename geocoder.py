from geopy.geocoders import Nominatim
import urllib.request
import csv
from config import *

# get file
print('Beginning file download with urllib2...')
outpathCsv = OUTPUTCSV
outputPathJson = OUTPUTJSON
urllib.request.urlretrieve(URL, INPUTFILE)

# geocode csv# source: #https: //blog.adrienvh.fr/2015/01/18/geocoder-en-masse-plusieurs-milliers-dadresses-avec-python-et-nominatim/

geocoder = Nominatim()
inputFile = open(INPUTFILE, 'rt')
outputFile = open(OUTPUTCSV, 'w')
import json

# create base method to create json
def createJson():
  data = {}
  data['type'] = 'FeatureCollection'
  data['features'] = []
  return data

try:
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
      cleanAdresse = adresse.replace('Mainland China', 'China')
      location = geocoder.geocode(cleanAdresse, True, 30)
      # add line to csv
      outputData.writerow((line[0],line[1],line[2],line[3],line[4],line[5], location.latitude, location.longitude))
      # prepare json data to append
      geometry = {
        'type':'Point',
        'coordinates': [location.latitude, location.longitude]
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