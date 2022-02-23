
'''

Espoo lyhyt historia
http://opendata.fmi.fi/wfs?service=WFS&version=2.0.0&request=getFeature&storedquery_id=fmi::observations::weather::timevaluepair&place=espoo&timestep=10&

Tuulen nopeutta palauttaa suureparametri ws_10min ja lämpötilaa t2m.

Arvo voi olla NaN, esim. jos viimeisin puuttuu, vaikka kellonaika on jo ohitettu.

'''

from xml.dom import minidom
from urllib.request import urlopen
import collections
import math
import time
from datetime import datetime

import telegram


def roundStr(number):
    return str(round(number, 1))

def writeFile(message):
    fileName = "./data/" + str(round(time.time())) + ".txt"
    textFile = open(fileName, "w")
    n = textFile.write(message)
    textFile.close()
    print("Wrote message:\n" + message)

# Returns measurements of a single thing in an orderedDict (ordered by time descending)
def getMeasurements(singleTimeSeries):
    dataDict = {}

    allMeasurements = singleTimeSeries.getElementsByTagName('wml2:MeasurementTVP')
#    print(allMeasurements)
    for singleMeasurement in allMeasurements:
#        print(singleMeasurement)
        timeElement = singleMeasurement.getElementsByTagName('wml2:time')
        time = timeElement[0].firstChild.nodeValue
#        print(time)
        valueElement = singleMeasurement.getElementsByTagName('wml2:value')
        value = valueElement[0].firstChild.nodeValue
#        print(value)
        dataDict[time] = float(value)
    
    orderedDict = collections.OrderedDict(sorted(dataDict.items(), reverse = True))

    orderedList = []

    # Make a list
    for time, value in orderedDict.items():
#        print (time + " " + str(value))

        # TODO: If there are missing values in between, time is calculated incorrectly. How to fix?
        # Skip Nan values
        if math.isnan(value):
            continue

        orderedList.append(value)

    return orderedDict, orderedList


# --------------------------------
# Setup

url = "http://opendata.fmi.fi/wfs?service=WFS&version=2.0.0&request=getFeature&storedquery_id=fmi::observations::weather::timevaluepair&place=espoo&timestep=10&"

file = urlopen(url)
#print(file) # debug

xmlData = minidom.parse(file)

allTimeSeries = xmlData.getElementsByTagName('wml2:MeasurementTimeseries')

# --------------------------------
# Getting data

#print(allTimeSeries)

# Loops timeseries. A timeseries contains multiple measurements of a single thing, like temperature.
for singleTimeSeries in allTimeSeries:
    id = singleTimeSeries.getAttribute("gml:id")
    print(id)

    # Temperature
    if id.endswith("t2m"):
        temperatureOrderedDict, temperatureList = getMeasurements(singleTimeSeries)
#        print(temperatureOrderedDict)
    elif id.endswith("ws_10min"):
        windspeedOrderedDict, windspeedList = getMeasurements(singleTimeSeries)
        print("HERE:")
        print(windspeedOrderedDict)
    

#print(temperatureList)
#print(windspeedList)

message = ""

# TEMPERATURE
change = temperatureList[0] - temperatureList[3]
if change > 2 or change < -2:    
    message = message + "lämpötilamuutos 30 min: " + roundStr(change) + "\n"
    message = message + "nyt " + str(temperatureList[0]) + " C\n"

change = temperatureList[0] - temperatureList[12]
if change > 4 or change < -4:
    message = message + "lämpötilamuutos 2 h: " + roundStr(change) + "\n"
    message = message + "nyt " + str(temperatureList[0]) + " C\n"

change = temperatureList[0] - temperatureList[36]
if change > 0.1 or change < -0.1:
    message = message + "lämpötilamuutos 6 h: " + roundStr(change) + "\n"
    message = message + "nyt " + str(temperatureList[0]) + " C\n"

# WIND
change = windspeedList[0] - windspeedList[3]
if change > 2 or change < -2:    
    message = message + "tuulen muutos 30 min: " + roundStr(change) + "\n"
    message = message + "tuuli " + str(windspeedList[0]) + " m/s\n"

change = windspeedList[0] - windspeedList[12]
if change > 4 or change < -4:    
    message = message + "tuulen muutos 2 h: " + roundStr(change) + "\n"
    message = message + "tuuli " + str(windspeedList[0]) + " m/s\n"

change = windspeedList[0] - windspeedList[36]
if change > 8 or change < -8:    
    message = message + "tuulen muutos 6 h: " + roundStr(change) + "\n"
    message = message + "tuuli " + str(windspeedList[0]) + " m/s\n"


#print("MGS:")
#print(message)

if (message):

    # Time, since this can be sent delayed
    now = datetime.now()
    timeStr = now.strftime("%-d.%-m.%Y @ %H.%M") + " UTC"
    message = message + timeStr

#    telegram.sendtext(message, True) # True = debug
    writeFile(message)