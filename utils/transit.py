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

#helper function for getSubwayStatus()
#takes dictionary of subway line info
#makes html table for subway status
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

#helper function for getSubwayStatus()
#turns subwayLines (chunk of xml) into a dictionary
#separates and stores status info for each subway line
#returns a dictionary
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

#this function is called by app.py
#returns table of subway statuses
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
def stopsOnRouteDropdown(busNum):
    with app.app_context():
        key = app.config["BUSTIME"]
        response = urllib.urlopen('http://bustime.mta.info/api/where/stops-for-route/MTA%20NYCT_' + busNum + '.json?key=' + key + '&includePolylines=false&version=2')
        text = json.loads(response.read())
        listOfStops = text['data']['references']['stops']
        
        stopNames = []
        for stop in listOfStops:
            nameAndInfo = stop['name'] +  ' (' + stop['direction'] + ') #' + stop['code']
            stopNames.append(nameAndInfo)
        stopNames.sort()
        
        ret = '''<div class="form-group">
        <label for="Stop">Stop:</label>
        <select name="stop" class="form-control" id="stop">'''
        
        for name in stopNames:
            ret += '<option>' + name + '</option>'

        ret += '</select></div>'
        return ret


#takes a busNum (ex Q28, M1) and stopID for bus stop (ex 501758) -- both strings
#returns html of the distances of buses approaching the stop
def getBusesRelativeToStop(busNum, stopID):
    with app.app_context():
        key = app.config["BUSTIME"]
        response = urllib.urlopen('http://bustime.mta.info/api/siri/stop-monitoring.json?key=' + key + '&OperatorRef=MTA&MonitoringRef=' + stopID + '&LineRef=MTA%20NYCT_' + busNum)
        text = json.loads(response.read())
        
        retVal = ""
        buses = text['Siri']['ServiceDelivery']['StopMonitoringDelivery'][0]['MonitoredStopVisit']
                
        for bus in buses:

            retVal += bus['MonitoredVehicleJourney']['MonitoredCall']['Extensions']['Distances']['PresentableDistance']
            retVal += "<br>"

        return retVal


