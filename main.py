#importing dependencies
import requests #library to make a webrequest

#here are my functions to avoid duplicated code
def makeWebrequest(url):
    try:
        responseFromWebsite = requests.get(url)
    
    #catch error when something wentsw wrong with webrequest
    except:
        return "error"

    
    #return success + clever-tanken content
    return responseFromWebsite.text

def parseGasStationInfo(website):
    name = getGasStationName(website)
    price = getGasStationPrice(website)
    print(name, price)


def getGasStationName(website):
    startIndex = int(website.find("<title>")) + 7
    endIndex = website.find("</title>")
    name = website[startIndex:endIndex]
    index = name.find(" - Öffnungszeiten")
    name = name[0:index]
    return name

def getGasStationPrice(website):
    startIndex = website.find("current-price-1") + 15 + 2
    endIndex = website.find("</span>", startIndex)
    priceString = website[startIndex:endIndex]
    #price = int(priceString)
    return priceString

    

#read text file which stores all clever-tanken links of gasstations that are of interest
file = open("gas_stations.txt")

#create a list and then store the links in a list to be able to call the links seperately
gasStationLinks = []
for i in file:
    gasStationLinks.append(i)


#webrequests to clever-tanken
#print(makeWebrequest(gasStationLinks[0]))

for link in gasStationLinks:
    website = makeWebrequest(link)
    
    #in case that the webrequest of that specific gasStation didn't work end the iteration before parsing
    if website == "error":
        break    
    
    parseGasStationInfo(website)