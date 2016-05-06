# -*- coding: utf-8 -*-

import sys
import os
import urllib2
import json
import config
import util


def placeSearch(lat, lng):
    # print('placeSearch(\"' + str(lat) + '\", \"' + str(lng) + '\")')

    radius = 1000 # raggio ricerca
    typeList = ['bank', 'restourant', 'church','bar'] # tipo

    # make data dir
    data_dir = 'google-placesearch-api-test'
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    returnList = []

    for type in typeList:
        response_file_name = 'json-' + type + "-loc" + util.encodeFilename(str(lat)) + '__' + util.encodeFilename(str(lng)) + '.json'

        response_path = os.path.join(data_dir, response_file_name)
        if not os.path.exists(response_path):
            # make api request
            url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=' + str(lat) + ',' + str(lng) + '&radius=' + str(radius) + '&type=' + type + '&key=' + config.API_KEY
            # DEBUG print('url: ' + url);

            try:
                json_string = urllib2.urlopen(url, timeout=4).read()
            except socket.timeout as ex:
                print('WARNING: sockect-timeout')
                return None
            except urllib2.URLError as ex:
                print('WARNING: request ' + url + ' failed')
                print(ex)
                return None
            except:
                print('ERROR: request ' + url + ' failed')
                print(ex)
                sys.exit()
                return None

            # save response on file
            text_file = open(response_path, 'w')
            text_file.write(json_string)
            text_file.close()

            responseJson = json.loads(json_string)

            returnList.append(responseJson)
        else:
            # parse json file and extract data
            text_file = open(response_path, 'r')
            json_string = text_file.read()
            text_file.close()

            responseJson = json.loads(json_string)
            
            returnList.append(responseJson)

    return returnList
