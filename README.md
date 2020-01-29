# Corona Geocoder

## LICENCE
GPL-3.0

## Description
Allow to geocode data provided by [John Hopkins University](https://systems.jhu.edu/) CSSE :

https://docs.google.com/spreadsheets/d/1yZv9w9zRKwrGTaR-YzmAqMefw4wMlaXocejdxZaTs6w/export?format=csv

Use loop to get location from Nominatim API :

https://nominatim.openstreetmap.org/

Nominatim is free and open source !

## Config
Read and change params : 
* URL = data url to download and geocode in the next time
* INPUTFILE = target path to save download data
* OUTPUTCSV = target path to save geocoding result as CSV
* OUTPUTJSON = target path to save geocoding result as GEOJSON

## Install

### Python3

[Help tutorial](https://www.digitalocean.com/community/tutorials/how-to-install-python-3-and-set-up-a-programming-environment-on-debian-10)

### pip
```
sudo apt update
sudo apt install python3-pip
```
### Geopy2
```
pip install geopy
```
https://geopy.readthedocs.io/en/stable/#geopy-2-0
