import urllib
import json
from flask import current_app as app

#takes a string of html and the tag to look for
#returns text found within the first occurrence of TAG
#returns empty string if tag not found
#expects that tags are paired (open and close tags present)
#ex: getInfoFromInsideTags( "<h>Hello</h>", "h" ) -> "Hello"
def getInfoFromInsideTags(wholeInfo, tag):
    tagToFind = "<" + tag + ">"
    findOpeningTag = wholeInfo.find(tagToFind)
    if findOpeningTag != -1:
        startOfInfo = findOpeningTag + len(tagToFind);
        endOfInfo = wholeInfo.find("</" + tagToFind[1:])
        info = wholeInfo[startOfInfo : endOfInfo]
        return info
    return ""

#takes html text
#returns text with &lt; and &gt; repalced with < and > respectively
def gangSignify(text):
    text = text.replace("&lt;", "<")
    text = text.replace("&gt;", ">")
    return text;

#helper function for getTrainyStatus()
#takes dictionary of train line info
#contructs html for a table for train status
def tableifyStatus(d):
    ret = ""
    ret += "<table>"
    for line in sorted(d.iterkeys()):
        ret += "<tr>"
        ret += "\t<td>" + line + "</td>"
        ret += "\t<td>" + d[line]["status"] + "</td>"
        ret += "</tr>"
    ret +="</table>"
    return ret


#helper function for getTrainStatus()
#turns trainLines (chunk of xml) into a dictionary
#separates and stores status info for each train line
#returns a dictionary
def dictifyTrainStatus(trainLines):
    trainStatuses = {}
    for elem in trainLines:
        findName = elem.find("<name>")
        if findName != -1:
            lineName = getInfoFromInsideTags(elem, "name")
            lineStatus = getInfoFromInsideTags(elem, "status")
            statusDetails = getInfoFromInsideTags(elem, "text")
            statusDetails = gangSignify(statusDetails)
            statusDetails = statusDetails.replace("\r", "")
            statusDetails = statusDetails.replace("\n", "<br>")
            trainStatuses[lineName] = {"status": lineStatus, "details": statusDetails}
    return trainStatuses

#typeOfTrain either "subway" or "LIRR"
#returns an html table of the statuses
def getTrainStatus(typeOfTrain):
    response = urllib.urlopen('http://web.mta.info/status/serviceStatus.txt')
    text = response.read();
    trainInfo = getInfoFromInsideTags(text, typeOfTrain)
    trainLines = []
    while (trainInfo.find("<line>") != -1):
        trainLines.append(getInfoFromInsideTags(trainInfo, "line"))
        trainInfo = trainInfo.replace("<line>", "", 1)
        trainInfo = trainInfo.replace("</line>", "", 1)
    return dictifyTrainStatus(trainLines)

#this function is called by app.py
#returns html table of subway statuses
def getSubwayStatus():
    return getTrainStatus("subway")

#this function is called by app.py
#returns html table of LIRR statuses
def getLIRRStatus():
    return getTrainStatus("LIRR")

#currently not used
'''
def listBusLocations(busNum):
    with app.app_context():
        key = app.config["BUSTIME"]
        response = urllib.urlopen('http://api.prod.obanyc.com/api/siri/vehicle-monitoring.json?key=' + key + "&LineRef=" + busNum+ "&DirectionRef=0")
        text = json.loads(response.read())
        listOfBuses = text['Siri']['ServiceDelivery']['VehicleMonitoringDelivery'][0]['VehicleActivity']

        locations = []
        for bus in listOfBuses:
            locations.append( bus['MonitoredVehicleJourney']['MonitoredCall']['StopPointName'])
        return locations
        '''

#this function is called by app.py
#takes a busNum (ex Q28, M1) -- string
#returns html code for dropdown menu listing the bus's stops
def stopsOnRoute(busNum):
    with app.app_context():
        key = app.config["BUSTIME"]
        response = urllib.urlopen('http://bustime.mta.info/api/where/stops-for-route/MTA%20NYCT_' + busNum + '.json?key=' + key + '&includePolylines=false&version=2')
        text = json.loads(response.read())
        if text['code'] == 404:
            return None
        
        listOfStops = text['data']['references']['stops']

        stopNames = []
        for stop in listOfStops:
            nameAndInfo = [stop['name'], stop['direction'], stop['code']]
            stopNames.append(nameAndInfo)
        stopNames.sort()
        return stopNames


#takes a busNum (ex Q28, M1) and stopID for bus stop (ex 501758) -- both strings
#returns html of the distances of buses approaching the stop
def getBusesRelativeToStop(busNum, stopID):
    with app.app_context():
        key = app.config["BUSTIME"]
        response = urllib.urlopen('http://bustime.mta.info/api/siri/stop-monitoring.json?key=' + key + '&OperatorRef=MTA&MonitoringRef=' + stopID + '&LineRef=MTA%20NYCT_' + busNum)
        text = json.loads(response.read())

        retVal = ""
        buses = text['Siri']['ServiceDelivery']['StopMonitoringDelivery'][0]['MonitoredStopVisit']
        return buses
