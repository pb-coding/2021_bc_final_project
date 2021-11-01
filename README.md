# 2021_bc_final_project
Final project for my business coding classes:

This is a gas price comparison program for user selected gas stations based on extracted data of the clever-tanken.de website.
Gas station specific ID's can be stored in the gas_stations.txt file - only clever-tanken.de ID's are supported.

Implemented features:
* 'list' - to display all gas stations with the corresponding prices
* 'cheapest' - to display the cheapest gas sttation regarding the requested fuel

Actually you could use the "add to favorite" feature of clever-tanken.de for that, but I wanted to build such kind of a feature on my own as a challenge.

Upcoming features:
* reloading the gas_stations.txt link list with a "reload" command without the need to restart the program
* adding links not only by inserting them into the gas_stations.txt but adding them with a command in the program.
* checking for duplicate IDs in gas_stations.txt