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

def tableifySubwayStatus(d):
    ret = ""
    ret += "<table>"
    for status in sorted(d.iterkeys()):
        ret += "<tr>"
        ret += "\t<td>" + status + "</td>"
        ret += "\t<td>" + d[status]["status"] + "</td>"
        ret += "</tr>"

    ret +="</table>"

    return ret

def dictifySubwayStatus(subwayLines):        
    subwayStatuses = {}
    for elem in subwayLines:
        findName = elem.find("<name>")
        if findName != -1:
            lineName = getInfoFromInsideTags(elem, "name")
            lineStatus = getInfoFromInsideTags(elem, "status")
            statusDetails = getInfoFromInsideTags(elem, "text")
            statusDetails = gangSignify(statusDetails)
            statusDetails = statusDetails.replace("\r", "")
            statusDetails = statusDetails.replace("\n", "<br>")
            subwayStatuses[lineName] = {"status": lineStatus, "details": statusDetails}
    return subwayStatuses
             
def getSubwayStatus():
    response = urllib.urlopen('http://web.mta.info/status/serviceStatus.txt')
    text = response.read();
    subway = getInfoFromInsideTags(text, "subway")
    subwayLines = []
    while (subway.find("<line>") != -1):
        subwayLines.append(getInfoFromInsideTags(subway, "line"))
        subway = subway.replace("<line>", "", 1)
        subway = subway.replace("</line>", "", 1)

    return tableifySubwayStatus(dictifySubwayStatus(subwayLines))

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
        
def listStopsOnRoute(busNum):
    with app.app_context():
        key = app.config["BUSTIME"]
        response = urllib.urlopen('http://bustime.mta.info/api/where/stops-for-route/MTA%20NYCT_' + busNum + '.json?key=' + key + '&includePolylines=false&version=2')
        text = json.loads(response.read())
        listOfStops = text['data']['references']['stops']
        return str(listOfStops)
#        listOfStopNames = []
        stopNames = ""
        # for stop in listOfStops:
        #     listOfStopNames.append(stop['name'])
        # listOfStopNames.sort()
        for stop in listOfStops:
            stopNames += stop['name'] + "<br>"
        return stopNames

def getBusesRelativeToStop(busNum, stopID):
    with app.app_context():
        key = app.config["BUSTIME"]
        response = urllib.urlopen('http://bustime.mta.info/api/siri/stop-monitoring.json?key=' + key + '&OperatorRef=MTA&MonitoringRef=' + stopID + '&LineRef=MTA%20NYCT_' + busNum)
        text = json.loads(response.read())
        retVal = ""
        buses = text['Siri']['ServiceDelivery']['StopMonitoringDelivery'][0]['MonitoredStopVisit']
        for bus in buses:
            retVal += bus['MonitoredVehicleJourney']['MonitoredCall']['Extensions']['Distances']['PresentableDistance'] + "<br>"
        return retVal
