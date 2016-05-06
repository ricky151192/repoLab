# -*- coding: utf-8 -*-

import sys
import os
import urllib
import urllib2
import json
import socket
import config
import util

def createRoute(origin, destination):
    # print('createRoute(\"' + origin + '\", \"' + destination + '\")')

    # make cache directory
    data_dir = 'google-direction-api-test'
    if not os.path.exists(data_dir):
      os.makedirs(data_dir)

    # encode address
    originEnc = urllib.quote(origin, safe='')
    destinationEnc = urllib.quote(destination, safe='')

    # calculate cache file name
    response_file_name = 'json-origin_' + util.encodeFilename(originEnc) + '-destination_' + util.encodeFilename(destinationEnc) + '.json'

    response_path = os.path.join(data_dir, response_file_name)
    responseJson = None
    if not os.path.exists(response_path):
        # make api request
        url = 'https://maps.googleapis.com/maps/api/directions/json?origin=' + originEnc + '&destination=' + destinationEnc + '&key=' + config.API_KEY
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
    else:
        # parse json file and extract data
        text_file = open(response_path, 'r')
        json_string = text_file.read()
        text_file.close()

        responseJson = json.loads(json_string)

    if (len(responseJson['routes']) > 0):
        return responseJson
    else:
        return None


# print(createRoute('toronto', 'montreal'))
# print(createRoute('Via Beato Angelico 7 Seregno', 'Viale Sarca 336 20125 Milano'))
# print(createRoute('Via ééàòù', 'Viale ìéèòàù'))

