#importing dependencies
import requests #library to make a webrequest

#here are my functions to avoid duplicated code

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
    price = float(priceString)
    return price


def showCheapestPrice(gasStationData):
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
gasStationData = []    

print("read text file where all clever-tanken gas station links of interest are stored..")
gasStationLinks = open("gas_stations.txt")

print("Data collection for every gas station...")
for link in gasStationLinks:
    print("\nrequesting data of link:" + link)
    
    #catch error when something wents wrong with webrequest
    try:
        website = requests.get(link).text
    
    #in case that the webrequest of that specific gasStation didn't work end the iteration before parsing
    except:
        print("requesting link" + link + "failed. Skipping that gas station.")
        break  
    
    try:
        name = getGasStationName(website)
        price = getGasStationPrice(website)

    except:
        print("error - parsing gas station data from website HTML went wrong. Skipping that gas station.")
        break
    
    gasStationData.append([name,price])
    print("added " + name + " to the list.")

print("data collected and stored.\n")

while True:

    userInput = input("Please enter:\n 'list' - to display all gas stations with the corresponding diesel prices\n 'cheapest' - to display only the cheapest one\n Input: ")

    if userInput == "list":
        for gasStation in gasStationData:
            print("Price:",gasStation[1], "€ - ", gasStation[0])


    elif "cheapest":
        cheapestGasStation = showCheapestPrice(gasStationData)
        if cheapestGasStation[1] == 100 or cheapestGasStation[0] == "":
            print("error - no data")
        
        else:
            print("Price:",cheapestGasStation[1], "€ - ", cheapestGasStation[0])
    
    else:
        print("Unknown input. Ignoring.")
