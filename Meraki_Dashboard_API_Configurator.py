# Written By: Nicholas Cawthon-Church
# Date: 12/6/2022

#Meraki v1 Library (install w/ pip)
import meraki
import json
import csv
from pandas import *

#This is the Menu Function
def menu():
    print("[1]...........Get Your Organization")
    print("[2]......Get Organizations Networks")
    print("[3]............Get Networks Devices")
    print("[4].........Get Client Band History")
    print("[5]......Claim Devices to a Network")
    print("[6]..................Rename Devices")
    print("[0]................Exit the Program")

#This is a function to show pretty json data
def json_pretty(response):
    print(json.dumps(response, indent=2, sort_keys=True))
    print()
    input("Press Enter key to continue...")

#This function pulls client band information and passes the API key into the function as a parameter.
def client_band_history(key):
    #Gets the network ID that the user wants to query
    network_id = input("Enter desired Network ID: ")
    dashboard = meraki.DashboardAPI(key)

    #This menu is isolated from the main menu function.
    def menu():
        print("Choose an Option:")
        print("[1]....... 2.4 GHz")
        print("[2]......... 5 GHz")
        print("[3]......... 6 GHz")
        print("[0]...Exit Program")

    print()
    #prints the menu for this function.
    menu()
    print()
    #Variable holding user menu option.
    option = int(input("Enter desired menu option: "))

    #This is where the function determines the users option and functions accordingly.
    while option != 0:
        #Is it option 1?
        if option == 1:
            #Uses NetID to get number of clients using specified band over a 48 hour timespan.
            response = dashboard.wireless.getNetworkWirelessClientCountHistory(network_id, timespan="172800", band="2.4")
            print(json.dumps(response, indent=2, sort_keys=True))
            print('''
            The First object shows the number of clients that used the 2.4 GHz band yesterday

            The Second object shows the number of clients that used the 2.4 GHz band today
            ''')
        #Is it option 2?
        elif option == 2:
            #Uses NetID to get number of clients using specified band over a 48 hour timespan.
            response = dashboard.wireless.getNetworkWirelessClientCountHistory(network_id, timespan="172800", band="5")
            print(json.dumps(response, indent=2, sort_keys=True))
            print('''
            The First object shows the number of clients that used the 5 GHz band yesterday

            The Second object shows the number of clients that used the 5 GHz band today
            ''')
        #Is it option 3?
        elif option == 3:
            #Uses NetID to get number of clients using specified band over a 48 hour timespan.
            response = dashboard.wireless.getNetworkWirelessClientCountHistory(network_id, timespan="172800", band="6")
            print(json.dumps(response, indent=2, sort_keys=True))
            print('''
            The First object shows the number of clients that used the 6 GHz band yesterday

            The Second object shows the number of clients that used the 6 GHz band today
            ''')

        else:
            print("Invalid Option")

        print()    
        menu()
        option = int(input("Enter desired menu option: "))
    
#First time the menu is called. (This is when it prints to user)
menu()

#Variable to store user menu option.
option = int(input("Enter desired menu option: "))
print("\n")

#Variable to store users API key
API_KEY = input("Please Enter your Meraki Dashboard API key: ")
print("\n")

#Initializes Meraki dashboard with user API key.
dashboard = meraki.DashboardAPI(API_KEY)

#This is where the program determines the users option and functions accordingly.
while option != 0:

    #Is it option 1?
    if option == 1:
        #Uses API key to get all organizations your account is associated with.=.
        response = dashboard.organizations.getOrganizations()
        json_pretty(response)

    #Is it option 2?
    elif option == 2:
        #Uses OrgID from option 1 to get all the networks for a specified org.
        org_id = input("Please Enter the Organization ID (found in menu option[1]): ")
        response = dashboard.organizations.getOrganizationNetworks(org_id)
        json_pretty(response)

    #Is it option 3?
    elif option == 3:
        #Uses NetID from option 2 to get all devices on a specified network.
        net_id = input("Please Enter the Network ID (found in option[2]): ")
        response = dashboard.networks.getNetworkDevices(net_id)
        json_pretty(response)

    #Is it option 4?
    elif option == 4:
        #Passes the API key to the client_band_history function as an argument.
        client_band_history(API_KEY)

    #Is it option 5?
    elif option == 5:
        #Prompts the user a CSV file is required for this option.
        print("This Option requires a csv file be provided containing AP inventory data (Hostnames, Serials).")
        print("\n")
        csv_check = input("Enter Y if you have this file ready: ")
        print("\n")
        #Checks users input for CSV confirmation
        if csv_check == "Y":
            print("This is where you will do one of two options:")
            #Option 1 requires path like C:\Users\username\Documents\AP_CSV.csv
            print("[1] Enter full path to the CSV")
            print("[2] Use the AP_CSV.csv document that is in the same directory as this python script.") 
            print("\n")
            print("If it is in the same directory then just specify the full csv filename 'AP_CSV.csv'")
            csv_path = input("Enter the path to the CSV here (Quotes not needed): ")
            net_id = input("Please Enter the Network ID (found in option[3]): ")

            '''data = read_csv(csv_path)
            serials = data['Serial'].tolist()
            #print(serials)
            dashboard.networks.claimNetworkDevices(net_id, serials)'''

            with open(str(csv_path)) as inv_data:
                data = csv.DictReader(inv_data)
                serials = []
                for colmn in data:
                    serials.append(colmn['Serial'])

            print(serials)
            #This function claims devices from inventory into a network.
            dashboard.networks.claimNetworkDevices(net_id, serials)
        #If user doesn't have the CSV ready.
        else:
            print("Exiting to Menu..")
            pass

    #Is it option 6?
    elif option == 6:
        #Prompts the user a CSV file is required for this option.
        print("This Option requires a csv file be provided containing AP inventory data (Hostnames, Serials).")
        print("\n")
        csv_check = input("Enter Y if you have this file ready: ")
        print("\n")
        #Checks users input for CSV confirmation
        if csv_check == "Y":
            print("This is where you will do one of two options:")
            #Option 1 requires path like C:\Users\username\Documents\AP_CSV.csv
            print("[1] Enter full path to the CSV")
            print("[2] Use the AP_CSV.csv document that is in the same directory as this python script.") 
            print("\n")
            print("If it is in the same directory then just specify the full csv filename 'AP_CSV.csv'")
            csv_path = input("Enter the path to the CSV here (Quotes not needed): ")
            #Opens CSV
            with open(csv_path) as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')
                #Counts rows
                line_count = 0
                #Iterates through rows (row[0] = column A on given row)
                for row in csv_reader:
                    if line_count == 0:
                        print(f'Column names are{", ".join(row)}')
                        print("\n")
                        line_count += 1
                    else:
                        print(f'Attempting to update {row[1]} name to {row[0]}')
                        print("\n")
                        #Updates device Names using the serial(row[1] or column-B, and the name(row[0] or column-A))
                        dashboard.devices.updateDevice(row[1], name=row[0])
                        #print(row[1], row[0])
        #If user doesn't have the CSV ready.
        else:
            print("Exiting to Menu..")
            pass
    #If user choses option outside of 0-6
    else:
        print("Invalid Option")
    #If user choses invalid option the menu opens back up for user.
    print()    
    menu()
    option = int(input("Enter desired menu option: "))


print("Goodbye.")