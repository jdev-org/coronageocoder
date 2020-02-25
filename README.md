# Corona Geocoder

## LICENCE
GPL-3.0

## Description
Allow to geocode data provided by [John Hopkins University](https://systems.jhu.edu/) CSSE :

https://docs.google.com/spreadsheets/d/1yZv9w9zRKwrGTaR-YzmAqMefw4wMlaXocejdxZaTs6w/

Use loop to get location from Nominatim API :

https://nominatim.openstreetmap.org/

Nominatim is free and open source !

## Config ogr2ogr
Read and change params : 
* URL = data url to download and geocode in the next time
* INPUTFILE = target path to save download data
* OUTPUTCSV = target path to save geocoding result as CSV
* OUTPUTJSON = target path to save geocoding result as GEOJSON

## config sql
* DELIMITER = input file delimiter as , or ;
* URL_CONFIRMED = url to download confirmed data source as time series
* URL_DEATHS = url to download deaths data source as time series
* URL_RECOVERED = url to download recovered data source as time series

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

# SQLAlchemy and GeoAlchemy2
pip install SQLAlchemy
pip install GeoAlchemy2

# PostgreSQL
```sudo apt install postgresql
sudo apt install postgis```

# Create DB

* DB
```CREATE DATABASE corona;```

* USER
```CREATE USER geoserver WITH PASSWORD 'geoServer20';
GRANT ALL PRIVILEGES ON DATABASE "corona" to geoserver;```

* SCHEMA
```CREATE SCHEMA geoserver;
ALTER SCHEMA geoserver OWNER TO geoserver;```

* Create table into corona DB
```\c corona
CREATE TABLE geoserver.datacorona (
	id SERIAL PRIMARY KEY,
	state VARCHAR(255),
	couNtry VARCHAR(255),
	long float8,
	lat float8,
	date DATE,
	confirmed INT,
	deaths INT,
	recovered INT
);
CREATE EXTENSION postgis;
SELECT AddGeometryColumn('geoserver','datacorona','geom',4326,'POINT',2);
ALTER TABLE geoserver.datacorona OWNER TO geoserver;```

## Time support in GeoServer
https://docs.geoserver.org/stable/en/user/services/wms/time.html
