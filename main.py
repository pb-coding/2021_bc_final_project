#importing dependencies
import requests #library to make a webrequest

#here are my functions to avoid duplicated code

def getGasStationData(website, id, supportedFuels):
    
    #TEMPLATE CREATION
    #create list template with fake data so that there are values existing that can be replaced in this way --> thisGasStationData[index]
    thisGasStationData = [0,"blank name"] #ID and name of gas station
    
    #depending on the amount of supported fuels there need to be template data so that the data replacement progress does not error
    for fuel in supportedFuels:
        thisGasStationData.append(100) #e.g. X fuels filled with price 100

    #REPLACEMENT WITH REAL DATA
    thisGasStationData[0] = id #replace template data with ID of gas Station
    name = getGasStationName(website) #parse name from gas station
    thisGasStationData[1] = name #replace template data with name of database
    
    lastIndex = 0 #lastIndex of "price-type-name" has to be set to 0 so that parsing begins with the first charachter of the HTML of clever-tanken.de
    
    #iterating while parsing the HTML for "price-type-name" || price-type-name is a reliable indicator of the available fuels of that gas station
    while True:
        index = website.find("price-type-name", lastIndex)
        
        if index == -1: #if no "price-type-name" is found (anymore) break out of the loop
            break

        #more comments coming soon...
        for id, fuel in enumerate(supportedFuels): #iteration through index of list AND value needed --> used enumerate for that
            startIndex = index + 17
            endIndex = website.find("</div>", startIndex)
            checkThisFuelString = website[startIndex:endIndex]
            if checkThisFuelString == fuel:
                fuelPrice = getFuelRelatedPrice(website, endIndex)
                thisGasStationData[id + 2] = fuelPrice
                #print("adding: ", fuel)

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


def getCheapestGasStation(gasStationDatabase, requestedFuelDatabaseIndex):
    current = 100
    currentName = ""
    for gasStation in gasStationDatabase:
        if gasStation[requestedFuelDatabaseIndex] < current:
            current = gasStation[requestedFuelDatabaseIndex]
            currentName = gasStation[1]
    
    cheapestGasStation = [currentName, current]
    return cheapestGasStation


#START-POINT
#create empty gasStation List where info will be stored after requesting them
base_url = "https://www.clever-tanken.de/tankstelle_details/"
supportedFuels = ["Diesel","Super E10", "Super E5", "SuperPlus", "ARAL Ultimate Diesel"]
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
    
    try:
        thisGasStationData = getGasStationData(website, id, supportedFuels)
        gasStationsDatabase.append(thisGasStationData)

    except:
        print("error - parsing gas station data from website HTML went wrong. Skipping that gas station.")
        continue
    

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


    elif userInput == "cheapest":
        print("You can compare these fuels: ", supportedFuels)
        requestedFuel = input("Please enter the type of fuel you want to compare: ")
        try:
            requestedFuelIndex = supportedFuels.index(requestedFuel) #Fuel Price Index in supportedFuels List
            requestedFuelDatabaseIndex = requestedFuelIndex + 2 #Fuel Price Index in gasStationDatabase
            validFuel = True

        except:
            validFuel = False
            print("That fuel is not supported.")

        if validFuel == True:
        
            cheapestGasStation = getCheapestGasStation(gasStationsDatabase, requestedFuelDatabaseIndex)
            
            if cheapestGasStation[1] == 100 or cheapestGasStation[0] == "":
                print("error - no data")
            
            else:
                print(supportedFuels[requestedFuelIndex],": ",cheapestGasStation[1], "€ - ", cheapestGasStation[0])

    elif userInput == "quit":
        quit()

    else:
        print("Unknown input. Ignoring.")
