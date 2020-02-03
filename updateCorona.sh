#!/bin/sh
lastDate=$(cat date.txt)
> date.txt
res=$(python3 ./scripts/timeseries_tojson.py 'https://docs.google.com/spreadsheets/d/1UF2pSkFTURko2OvfHWWlFpDFAr1UxCBA4JLwlSP6KFo/export?format=csv' ',')
echo $res >> date.txt

if [$lastDate = $res]
then
	echo "Update database"
	ogr2ogr -f "PostgreSQL" PG:"host=localhost port=5432 schema=public dbname=corona user=geoserver password=geoServer20" ./result/geodata.geojson -nln datacorona
fi

