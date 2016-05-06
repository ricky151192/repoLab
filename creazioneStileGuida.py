# -*- coding: utf-8 -*-

import os
import urllib2
import json
import re
import random
import csv
import string
import unicodedata
import datetime
import time
import sys
import urllib
import codecs
from google_direction_api_test import createRoute
from google_placesearch_api_test import placeSearch

class StreetHtmlParser:
  def __init__(self):
    self.regex = re.compile(u'<[a-zA-Z0-9]+( +[a-zA-Z0-9]+=\"[^"]*\")*>[^<]*</?[a-zA-Z0-9]+>')
    self.schemaDict = {'head on toward': 2, 'continue onto': 0, 'turn onto': 1, 'continue straight onto': 0, 'turns and becomes': 2, 'turns slightly and becomes': 2, 'keep to continue on': 1, 'at take the exit and stay on': 2, 'slight onto': 1, 'at take the exit onto': 2, 'turn to stay on': 1, 'continue straight to stay on': 0, 'turn at the 1st cross street onto': 1, 'keep to stay on': 1, 'head on toward /': 2, 'sharp onto': 1, 'make a at': 1, 'slight to stay on': 1, 'slight onto /': 1, 'merge onto': 0, 'keep at the fork follow signs for / and merge onto': 2, 'slight toward': 1, 'continue onto (signs for )': 0,  'slight to merge onto / toward /': 1, 'keep to continue on /': 1, 'take exit toward /': 1, 'take exit toward': 1,'enter the roundabout': -1, 'make a': -1}

  def parse(self, htmlStr):
    patternSchema = htmlStr
    patternParam = []

    matchedIterator = self.regex.finditer(htmlStr)
    for matched in matchedIterator:
      matchedStr = str(matched.group(0))
      patternSchema = patternSchema.replace(matchedStr, '');

      # ignora i div, contengono sempre informazioni diverse dalla via
      if matchedStr.startswith('<div') == False:
        patternParam.append(matchedStr[matchedStr.find('>')+1:matchedStr.rfind('<')])
      # print("matched at " + str(matched.start()) + ":" + str(matched.end()) + " : " + matchedStr)
    patternSchema = patternSchema.replace(', ', ' ').replace('  ', ' ').strip().lower()
    
    returnName = ''

    # se e' uno degli schemi ricorrenti la via e' sempre l'ultimo parametro
    if patternSchema.startswith('turn') or patternSchema.startswith('head') or patternSchema.startswith('at') or patternSchema.startswith('keep'):
      returnName = patternParam[-1]
    else:
      if self.schemaDict.has_key(patternSchema) == False:
        # altrimenti si cerca nel dizionario degli schemi oppure si ha un errore
        returnName = '' # non si sa' nulla se il patterno non e' considerato
      else:
        retParamIndex = self.schemaDict[patternSchema]
        if retParamIndex > 0:
          return patternParam[retParamIndex]
        else:
          # messaggio senza via
          return ""

    if len(returnName) == 0:
        print("WARNING: htmlStr: " + htmlStr);
        print("WARNING: pattern: \'" + patternSchema + "\' " + str(patternParam));
    
    return returnName

def stampaCSV(table_input, file_name, num_it):
  with open(file_name, 'w') as csvfile:
    csvfile.write(",".join(['Id_Itinerario', 'Id_Segmento', 'Data_It', 'Targa', 'Strada', 'Lat', 'Lng', 'VelocitaLimite', 'VelocitaRilevata', 'Km']) + "\n")

    for i in xrange(len(table_input)):
      for i2 in range(0, len(table_input[i])):
        if i2 != 0:
          csvfile.write(",")
        csvfile.write(str(table_input[i][i2]))
      csvfile.write("\n")

def checkLimitVelocity(velocity):
  new_velocity = random.sample([50,90,130],1)[0]
  division_old_new = round(new_velocity / float(velocity), 2)
  while(division_old_new == 2.6 or division_old_new == 0.38):
    new_velocity = random.sample([50,90,130],1)[0]
    division_old_new = round(new_velocity / float(velocity), 2)
  velocity = new_velocity
  return velocity


def createDrivingStyleRoute(parsed_json, targa, rischio, date, num_it):
  streetHtmlParser = StreetHtmlParser()

  resultList = parsed_json['routes'][0]['legs']
  distance = resultList[0]['distance']['text']
  start_address = resultList[0]['start_address']
  start_location_lat = resultList[0]['start_location']['lat']
  start_location_lng = resultList[0]['start_location']['lng']
  end_address = resultList[0]['end_address']
  steps = resultList[0]['steps']

  driving_style = list([])
  driving_style.append([num_it, 0, date, targa, urllib.quote(start_address.encode('utf-8'), safe=''), start_location_lat, start_location_lng, 50, random.randrange(50), 0]) ## Partenza del veicolo

  velocity = 50
  items = [50,90,130]
  count_roads = 1
  numbers_roads = len(steps)
  tmp = 0
  for step_i in range(0, len(steps)):
    step = steps[step_i]
    lat = step['end_location']['lat']
    lng = step['end_location']['lng']
    street_raw = step['html_instructions'].encode('utf-8') ## nome strada

    distance_step = round(step['distance']['value']/float(1000), 2) ## distanza percorsa per strada
    
    street = urllib.quote(streetHtmlParser.parse(street_raw), safe='')

    if count_roads == numbers_roads - 1:
      if velocity == 130:
        velocity = 90
      elif velocity == 90:
        velocity = 50 
    elif count_roads == numbers_roads:
      velocity = 50
    else:
      velocity = checkLimitVelocity(velocity)
    count_roads +=1
    
    
    if rischio == 1:
      instance_velocity = random.randrange(velocity-25, velocity+5)
    elif rischio == 2:
      instance_velocity = random.randrange(velocity-10, velocity+15)
    else:
      instance_velocity = random.randrange(velocity+10, velocity+40)

    row = [num_it, step_i+1, date, targa, street, lat, lng, velocity, instance_velocity, distance_step]
    driving_style.append(row)

  return driving_style

def getRandomPlace(place_list):
  num_request = random.randrange(1, len(place_list))
  parsed_json = place_list[num_request]

  num_place = random.randrange(1, len(parsed_json['results']))
  street = parsed_json['results'][num_place]['vicinity'].encode('utf-8')

  return street

def getDateIt(date_assicurazione):
  list_start_date = date_assicurazione.split('/',3)
  tmp = datetime.date(int(list_start_date[0]), int(list_start_date[1]), int(list_start_date[2]))
  unix_date = time.mktime(tmp.timetuple())
  delta_num_unix = random.randrange(100000,1000000)
  unix_date = unix_date + delta_num_unix
  new_date = time.strftime("%Y/%m/%d", time.localtime(int(unix_date)))
  return new_date

def generaStileGuida(file_name, start, end):
  random.seed(42) # inizializziamo il random anche qui

  tabella_clienti = list(csv.reader(open(os.path.join("GenerazioneClienti", "tabella_clienti.csv"),"r")))
 
  del tabella_clienti[0]

  driving_style = []
  it_count = 0
    #print(cliente)
    #print(tabella_clienti[cliente])
  for cliente in xrange(start,end):  
    data_assicurazione = tabella_clienti[cliente][10]
    veicolo = tabella_clienti[cliente][0]
    livello_rischio = tabella_clienti[cliente][-1]

    #print(veicolo)
    # Milano - Roma - Torino - Napoli 
    list_cities = [(45.4642700, 9.1895100), (41.9, 12.416667), (45.05, 7.666667), (40.863, 14.2767)]

    choose_city = random.randrange(0,4)
    city = list_cities[choose_city]

    ## read json places
    place_list = placeSearch(city[0], city[1]) # milano

    num_it_random = random.randrange(5,16)

    for it_count in xrange(num_it_random):
      date_it = getDateIt(data_assicurazione)
      start_address = getRandomPlace(place_list)
      end_address = getRandomPlace(place_list)
    # print('## startaddress: ' + start_address + " to " + end_address + " (" + date_it + ")")

      route = createRoute(start_address, end_address)
      
      if route != None:
        driving_style += createDrivingStyleRoute(route, veicolo,livello_rischio, date_it, it_count)
        it_count = it_count + 1
  
  stampaCSV(driving_style, file_name, 0)


generaStileGuida("routes-list.csv", 0, 20)

