import urllib




#print text



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


def constructStatusDetails(rawText):
    ret = ""
    details = gangSignify(statusDetails)
    while (details.find("</b>") != -1):
        ret += getInfoFromInsideTags(details, "b") + "<br>"
        details = details.replace("<b>", "", 1)
        details = details.replace("</b>", "", 1)

    ret = ret.replace("\n", "<br>")
    return ret;

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

print getSubwayStatus()
