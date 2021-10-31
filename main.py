#importing dependencies
import requests #library to make a webrequest

#here are my functions to avoid duplicated code

def getGasStationData(website, id, supportedFuels):
    
    thisGasStationData = [0,"blank name"]
    for fuel in supportedFuels:
        thisGasStationData.append(100)

    thisGasStationData[0] = id
    
    name = getGasStationName(website)
    thisGasStationData[1] = name
    
    lastIndex = 0
    
    while True:
        index = website.find("price-type-name", lastIndex)
        
        if index == -1:
            break

        for id, fuel in enumerate(supportedFuels):
            startIndex = index + 17
            endIndex = website.find("</div>", startIndex)
            checkThisFuelString = website[startIndex:endIndex]
            if checkThisFuelString == fuel:
                fuelPrice = getFuelRelatedPrice(website, endIndex)
                thisGasStationData[id + 2] = fuelPrice
                print("adding: ", fuel)

        lastIndex = index +1

    print("added", name, "to the list.")
    return thisGasStationData
        

def getGasStationName(website):
    startIndex = int(website.find("<title>")) + 7
    endIndex = website.find("</title>")
    name = website[startIndex:endIndex]
    index = name.find(" - Öffnungszeiten")
    name = name[0:index]
    return name

def getFuelRelatedPrice(website, endIndex):
    startIndex = website.find("current-price", endIndex) + 17
    endIndex = website.find("</span>", startIndex)
    priceString = website[startIndex:endIndex]
    price = float(priceString)
    return price

def getGasStationPrice(website):
    startIndex = website.find("current-price-1") + 15 + 2
    endIndex = website.find("</span>", startIndex)
    priceString = website[startIndex:endIndex]
    price = float(priceString)
    return price


def getCheapestGasStation(gasStationData):
    current = 100
    currentName = ""
    for gasStation in gasStationData:
        if gasStation[1] < current:
            current = gasStation[1]
            currentName = gasStation[0]
    
    cheapestGasStation = [currentName, current]
    return cheapestGasStation


#START-POINT
#create empty gasStation List where info will be stored after requesting them
base_url = "https://www.clever-tanken.de/tankstelle_details/"
supportedFuels = ["Diesel","Super E10", "Super E5", "SuperPlus"]
gasStationsDatabase = []

print("read text file where all clever-tanken gas station IDs of interest are stored..")
gasStationLinks = open("gas_stations.txt")

print("Data collection for every gas station...")
for id in gasStationLinks:
    link = base_url + id
    print("\nrequesting data of link:" + link)
    
    #catch error when something wents wrong with webrequest
    try:
        website = requests.get(link).text
    
    #in case that the webrequest of that specific gasStation didn't work end the iteration before parsing
    except:
        print("requesting link" + link + "failed. Skipping that gas station.")
        continue  
    
    #try:
        

        #price = getGasStationPrice(website)
    thisGasStationData = getGasStationData(website, id, supportedFuels)
    gasStationsDatabase.append(thisGasStationData)

    #except:
    #    print("error - parsing gas station data from website HTML went wrong. Skipping that gas station.")
    #    continue
    

print("data collected and stored.\n")

while True:

    userInput = input("Please enter:\n 'list' - to display all gas stations with the corresponding diesel prices\n 'cheapest' - to display only the cheapest one\n Input: ")

    if userInput == "list":
        for gasStation in gasStationsDatabase:
            
            print("\nName: ", gasStation[1], "- ID: ", gasStation[0])

            for index, fuel in enumerate (supportedFuels):
                if gasStation[index + 2] != 100:
                    print(fuel, " - ", gasStation[index + 2], "€")
                
            print("\n")


    #TODO cheapest function needs to be adjusted to support several fuels
    elif "cheapest":
        cheapestGasStation = getCheapestGasStation(gasStationsDatabase)
        if cheapestGasStation[1] == 100 or cheapestGasStation[0] == "":
            print("error - no data")
        
        else:
            print("Price:",cheapestGasStation[1], "€ - ", cheapestGasStation[0])
    
    else:
        print("Unknown input. Ignoring.")
