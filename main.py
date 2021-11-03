#importing dependencies
import requests #library to make a webrequest

#here are my functions to avoid duplicated code

def importGasStationIDs():
    #import gas station IDs from file
    gasStationIDsfile = open("gas_stations.txt") #open file and save IDs in file object
    gasStationIDs = [] #create gas station list where IDs will be stored
    for line in gasStationIDsfile: #check line by line if IDs is an duplicate
        if line not in gasStationIDs: #if not 
            gasStationIDs.append(line) #append to the gas stations ID list

    gasStationIDsfile.close()
    print("\nImport of clever-tanken gas station IDs from text file completed.")
    return gasStationIDs

def startDataCollection(supportedFuels, gasStationIDs):
    
    #start data collection
    print("Data collection for every gas station...")

    base_url = "https://www.clever-tanken.de/tankstelle_details/" #the clever-tanken.de url
    gasStationsDatabase = [] #create empty gasStation List where info will be stored after requesting them
    
    for id in gasStationIDs:
        link = base_url + id #building a link based on every ID
        print("\nrequesting data of link:" + link)
        
        #doing the webrequest to the gas station site & catch error when something wents wrong with the webrequest
        try:
            website = requests.get(link).text
        
        #in case that the webrequest of that specific gasStation didn't work end the iteration before parsing
        except:
            print("requesting link" + link + "failed. Skipping that gas station.")
            continue  
        
        #start parsing the data
        try:
            thisGasStationData = getGasStationData(website, id, supportedFuels)#create List with info about the gas station: ID, Name, fuelprice1, fuelprice2, fuelpriceX..
            gasStationsDatabase.append(thisGasStationData) #append gas station list with id, name, fuel prices - creating a List of List (2D)

        except:
            print("error - parsing or storing gas station data from website HTML went wrong. Skipping that gas station.")
            continue
        
    print("\nData collected and stored.\n")
    return gasStationsDatabase
    

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
        index = website.find("price-type-name", lastIndex) #e.g. <div class="price-type-name">Diesel</div> --> finds index of "p" in price-type-name
        
        if index == -1: #if no "price-type-name" is found (anymore) break out of the loop
            break

        #for every price-type-name found --> parse the fuel name next to it
        for id, fuel in enumerate(supportedFuels): #iteration through index of list AND value needed --> used enumerate for that
            startIndex = index + 17 #e.g. <div class="price-type-name">Diesel</div> --> from letter "p" to ">" = 17
            endIndex = website.find("</div>", startIndex) #e.g. <div class="price-type-name">Diesel</div> --> finds index of first "</div>" element after price-type-name
            checkThisFuelString = website[startIndex:endIndex] #e.g. <div class="price-type-name">Diesel</div> --> extracts fuel name
            
            if checkThisFuelString == fuel: #checks if this fuel is in the supportedFuel list the user is interested in
                fuelPrice = getFuelRelatedPrice(website, endIndex) #if the fuel is one of those the user is interested in the related price will be parsed
                thisGasStationData[id + 2] = fuelPrice #gas station list has in comparison to the supportedFuel list ID & name on index 0 and 1 --> add 2
                #print("adding: ", fuel)

        lastIndex = index +1

    print("added", name, "to the list.")
    return thisGasStationData
        

def getGasStationName(website):
    #in the title Tag of the HTML the name and address of the gas station can be found
    #e.g. <title>ARAL Tankstelle Aral Tankstelle Kölner Str. 255 in 51149 Köln - Öffnungszeiten</title>
    startIndex = int(website.find("<title>")) + 7 #finds "<" in <title> --> + 7 to find the ">" before the string to parse starts
    endIndex = website.find("</title>") #finds "<" in </title> = first character after string ends
    name = website[startIndex:endIndex] #actually extract the string out of the html
    index = name.find(" - Öffnungszeiten") 
    name = name[0:index] #remove the "- Öffnungszeiten" from the string
    return name

#parsing the price belonging to the fuel
def getFuelRelatedPrice(website, endIndex):
    #the next "current-price" value in HTML after the fuel name is always the price belonging to it --> start search at endIndex of fuel name
    startIndex = website.find("current-price", endIndex) + 17 #e.g. <span id="current-price-1">1.63</span> finds index of letter "c" in current-price & + 17 --> ">"
    endIndex = website.find("</span>", startIndex) # finds "<" of </span> directly following the price
    priceString = website[startIndex:endIndex] #actually parses price e.g. "1.63" from HTML: <span id="current-price-1">1.63</span>
    price = float(priceString)
    return price


def getCheapestGasStation(gasStationDatabase, requestedFuelDatabaseIndex):
    current = 100 #initiate current variable by setting current to 100 (unrealistic gas station price) following gas station prices will be always lower
    currentName = "" #initiate currentName variable
    
    #iterate through all gas stations
    for gasStation in gasStationDatabase:
        
        #replace price and name if the next gas station has a lower price than the one before
        if gasStation[requestedFuelDatabaseIndex] < current: #requestedFuelDatabaseIndex represents the index in the list of the requested fuel
            current = gasStation[requestedFuelDatabaseIndex] #save price of current cheapest gas station
            currentName = gasStation[1] #save name of current cheapest gas station
    
    cheapestGasStation = [currentName, current] #save name and price of the cheapest determined gas station to a list
    return cheapestGasStation #return that list


#START-POINT

#Welcome message
print("\n-------------------------------------------------------------")
print("Hello and Welcome to the gas station price comparison tool!")
print("-------------------------------------------------------------")
#here the user defines the fuels of interest
supportedFuels = input("\nPlease enter a comma seperated list of the fuels you want to consider. No spaces before or after a comma! \ne.g.:'Diesel,Super E10,Super E5,SuperPlus'\nInput: ").split(",")
print("\n\nYou entered following fuels: ", supportedFuels)


gasStationIDs = importGasStationIDs()
#data collection process is started and data is stored in a List (List of Lists)
gasStationsDatabase = startDataCollection(supportedFuels, gasStationIDs)

#this loops checks the user input for supported commands and executes them
while True:

    userInput = input("\n\nPlease enter:\n\n 'list' - to display all gas stations with the corresponding fuel prices\n\n 'cheapest' - to display only the cheapest gas station for a requested fuel\n\n 'add' - add clever-tanken ID of gas station to the file\n\n 'reload' - import IDs of gas stations from file and restart data collection\n\n 'quit' - quit the program\n\n Input: ")

    if userInput == "list": #check for user command "list"
        
        #iterating through every gas station in the gas station database
        for gasStation in gasStationsDatabase:
            
            print("\nName: ", gasStation[1], "- ID: ", gasStation[0]) #Print name and ID of every gas station

            #second iteration loop: display for every gas station the fuel prices the user defined in the beginning
            for index, fuel in enumerate (supportedFuels): #iteration through index & content of List needed:
                if gasStation[index + 2] != 100: #don't list fuels with no data (100 is set when no data is there)
                    print(fuel, " - ", gasStation[index + 2], "€")
                
            print("\n")


    elif userInput == "cheapest": #check for user command "cheapest"
        
        print("\nYou can compare these fuels: ", supportedFuels)
        requestedFuel = input("\nPlease enter the type of fuel you want to compare: ") #ask user for which fuel the cheapest gas station should be determined

        try:
            requestedFuelIndex = supportedFuels.index(requestedFuel) #find fuel price index in supportedFuels list by searching for the fuel the user requested
            #Fuel Price Index in gasStationDatabase
            requestedFuelDatabaseIndex = requestedFuelIndex + 2 #as the gasStationDatabase has ID and name at index 0 and 1 --> need to add 2 to the index
            validFuel = True #if the fuel user requests is in the initial selected supportFuel list set value to true

        except:
            validFuel = False #if a fuel is requested that is not in the supportedFuel list, the .index() function will error --> catch error and set value to False
            print("\nThat fuel is not supported.")

        if validFuel == True: #if fuel is supported start searching for the cheapest gas station
        
            cheapestGasStation = getCheapestGasStation(gasStationsDatabase, requestedFuelDatabaseIndex) #safe cheapest gas station (List consisting out of only one name & price)
            
            #in case that there was no data at all (no gas stations in ID list) or no price of that requested fuel --> the cheapestGasStation funtion would return:
            if cheapestGasStation[1] == 100 or cheapestGasStation[0] == "": #a price of 100€ or no name ""
                print("\nError - no data") #print no data error message
            
            else:
                print("-------------------------------------------------------------------------------------------")
                print("The cheapest gas station found for your request:")
                print(supportedFuels[requestedFuelIndex],": ",cheapestGasStation[1], "€ - ", cheapestGasStation[0]) #Print name of fuel, price in Euro and the name of gas station
                print("-------------------------------------------------------------------------------------------")

    elif userInput == "add":
        gasStationIDsfile = open("gas_stations.txt", "a") #open file and save IDs in file object // "a" --> append to file instead of replacing
        id = input("\nPlease enter the ID you want to insert: ") #user inserts ID he wants to add
        gasStationIDsfile.write("\n" + id) #append id to other ids in file in a new line
        gasStationIDsfile.close() #close file
    
    elif userInput == "reload": #check for user command "reload"
        gasStationIDs = importGasStationIDs()
        gasStationsDatabase = startDataCollection(supportedFuels, gasStationIDs) #import IDs of gas stations in gas_stations.txt file and restart the data collection
    
    elif userInput == "quit": #check for user command "quit"
        quit() #quits the program

    else:
        print("Unknown input. Ignoring.") #if the user input is not one of the commands above print error message
