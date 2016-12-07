import urllib

subwayStatuses = {}

response = urllib.urlopen('http://web.mta.info/status/serviceStatus.txt')
text = response.read();
'''
text = text.replace("&lt;", "<")
text = text.replace("&gt;", ">")

print text
'''
#print text

subway = text[:text.find("</subway>")]
subwayLines = subway.split("<line>")

def getSpecificInfo(wholeInfo, whatToGet):
    tagToFind = "<" + whatToGet + ">"
    findOpeningTag = wholeInfo.find(tagToFind)
    if findOpeningTag != -1:
        startOfInfo = findOpeningTag + len(tagToFind);
        endOfInfo = wholeInfo.find("</" + tagToFind[1:])
        info = wholeInfo[startOfInfo : endOfInfo]
        return info
    return ""

def gangSignifyText(text):
    text = text.replace("&lt;", "<")
    text = text.replace("&gt;", ">")
    return text;

def constructStatusDetails(rawText):
    ret = ""
    details = gangSignifyText(statusDetails)
    while (details.find("</b>") != -1):
        ret += getSpecificInfo(details, "b") + "<br>"
        details = details.replace("<b>", "", 1)
        details = details.replace("</b>", "", 1)

    ret = ret.replace("\n", "<br>")
    return ret;
     
for elem in subwayLines:
    findName = elem.find("<name>")
    if findName != -1:
        lineName = getSpecificInfo(elem, "name")
        lineStatus = getSpecificInfo(elem, "status")
        statusDetails = getSpecificInfo(elem, "text")
        statusDetails = statusDetails.replace("&lt;", "<")
        statusDetails = statusDetails.replace("&gt;", ">")
        statusDetails = statusDetails.replace("\r", "")
        statusDetails = statusDetails.replace("\n", "<br>")
        subwayStatuses[lineName] = {"status": lineStatus, "details": statusDetails}

print "<table>"
for line in subwayStatuses.keys():
    print "<tr>"
    print "\t<td>" + line + "</td>"
    print "\t<td>" + subwayStatuses[line]["status"] + "</td>"
    print "</tr>"

print "</table>"
