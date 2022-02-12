
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


def printTruncated(number):
    number = '%.1f'%(number)
    print(number)

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
    

print(temperatureList)

print("TEMPERATURE")

print("30 min change: ")
printTruncated(temperatureList[0] - temperatureList[3])

print("2 hour change: ")
printTruncated(temperatureList[0] - temperatureList[12])

print("6 hour change: ")
printTruncated(temperatureList[0] - temperatureList[36])

print("WIND SPEED")

print("30 min change: ")
printTruncated(windspeedList[0] - windspeedList[3])

print("2 hour change: ")
printTruncated(windspeedList[0] - windspeedList[12])

print("6 hour change: ")
printTruncated(windspeedList[0] - windspeedList[36])
