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
from datetime import datetime
import sys
# local files
from config import *
from pgsql import *

finalMsg = 'SUCCESS'

# get source from web
urllib.request.urlretrieve(URL_CONFIRMED, PATH_CONFIRMED)
urllib.request.urlretrieve(URL_DEATHS, PATH_DEATHS)
urllib.request.urlretrieve(URL_RECOVERED, PATH_RECOVERED)

# open files
confirmed_file = open(PATH_CONFIRMED, 'rt')
deaths_file = open(PATH_DEATHS, 'rt')
recovered_file = open(PATH_RECOVERED, 'rt')

try:
  # read openend files
  confirmed_data = csv.reader(confirmed_file, delimiter = DELIMITER)
  deaths_data = csv.reader(deaths_file, delimiter = DELIMITER)
  recovered_data = csv.reader(recovered_file, delimiter = DELIMITER)
  
  # get col name
  confirmed_cols = next(confirmed_data)
  deaths_cols = next(deaths_data)
  recovered_cols = next(recovered_data)

  # connect to database
  engine = connect(SGBD, USER, PASSWORD, HOST, PORT, DB)
  session = prepareSession(engine)
  Case = sqlTable(engine, TABLE, SCHEMA)

  # parse and send to database
  for confirmed in confirmed_data:
    addData(confirmed, session, Case, confirmed_cols, 'confirmed')
    
  for death in deaths_data:
    addData(death, session, Case, deaths_cols, 'deaths')
  
  for recovered in recovered_data:
    addData(recovered, session, Case, recovered_cols, 'recovered')
  
    
except Exception as inst:
  print(inst)
  finalMsg = 'ERROR'

finally:
  confirmed_file.close()
  deaths_file.close()
  recovered_file.close()
  exitValue = datetime.now().strftime('%Y-%m-%d')
  print(exitValue)