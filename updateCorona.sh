

#!/bin/sh

###################################################################
#Script Name	: updateCorona
#Description	: trigger python script and  push data into database
#Args           :                                                                                           
#Author       	:Gaetan B, Pierre J
#Email         	:jdev.fr                                           
###################################################################

echo "***START SCRIPT***"

lastDate=""
FILE=./date.txt

### python args
SCRIPT=./scripts/ogr2ogr/timeseries_tojson.py
URL="https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Confirmed.csv"
DELIMITER=","

### OGR options
# DB options
USER=""
PWD=""
DB="corona"
PORT=5432
HOST=localhost
TABLE=""

#  geojson file source
RESULT=./result/geodata.geojson


# check if file exist to get date value
if [ -f "$FILE" ]
then
        echo "File exist!"
        lastDate=$(cat "$FILE")
fi

# get data and create CSV - JSON data files
res=$(python3 $SCRIPT $URL $DELIMITER)

# update db if not already done
echo "last update => $lastDate"
echo "new date => $res"

if [ -z "$lastDate" -o "$res" != "$lastDate" ]
then
        #update database
        echo "Update DB"
        ogr2ogr -f "PostgreSQL" PG:"host=$HOST port=$PORT dbname=$DB user=$USER password=$PWD" $RESULT -nln $TABLE -overwrite
        >$FILE
        echo $res >> $FILE
else
        echo "Nothing to update!"
fi

echo "***END SCRIPT***"
