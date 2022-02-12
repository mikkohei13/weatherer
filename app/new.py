
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
    return orderedDict


url = "http://opendata.fmi.fi/wfs?service=WFS&version=2.0.0&request=getFeature&storedquery_id=fmi::observations::weather::timevaluepair&place=espoo&timestep=10&"

file = urlopen(url)
#print(file) # debug

xmlData = minidom.parse(file)

allTimeSeries = xmlData.getElementsByTagName('wml2:MeasurementTimeseries')

#print(allTimeSeries)

for singleTimeSeries in allTimeSeries:
    id = singleTimeSeries.getAttribute("gml:id")
    print(id)

    if id.endswith("t2m"):
        temperatureDict = getMeasurements(singleTimeSeries)
#        print(temperatureDict)

i = 0
temperatureList = []

for time, temperature in temperatureDict.items():
    print (time + " " + str(temperature))

    # Skip Nan values
    if math.isnan(temperature):
        continue

    temperatureList.append(temperature)
    i = i + 1
    

print(temperatureList)

print("30 min change: ")
print(temperatureList[0] - temperatureList[3])

print("2 hour change: ")
print(temperatureList[0] - temperatureList[12])

print("6 hour change: ")
print(temperatureList[0] - temperatureList[36])
