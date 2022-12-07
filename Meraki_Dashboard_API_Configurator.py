# Written By: Nicholas Cawthon-Church
# Date: 12/6/2022

import meraki
import json
import csv
from pandas import *

def menu():
    print("[1].......Enter Your Meraki API Key")
    print("[2]...........Get Your Organization")
    print("[3]......Get Organizations Networks")
    print("[4]............Get Networks Devices")
    print("[5].........Get Client Band History")
    print("[6]......Claim Devices to a Network")
    print("[7]..................Rename Devices")
    print("[0]................Exit the Program")

def json_pretty(response):
    print(json.dumps(response, indent=2, sort_keys=True))
    print()
    input("Press any key to continue...")

def client_band_history(key):
    network_id = input("Enter desired Network ID: ")
    dashboard = meraki.DashboardAPI(key)

    def menu():
        print("Choose an Option:")
        print("[1]....... 2.4 GHz")
        print("[2]......... 5 GHz")
        print("[3]......... 6 GHz")
        print("[0]...Exit Program")

    print()
    menu()
    print()
    option = int(input("Enter desired menu option: "))

    while option != 0:
        
        if option == 1:
            response = dashboard.wireless.getNetworkWirelessClientCountHistory(network_id, timespan="172800", band="2.4")
            print(json.dumps(response, indent=2, sort_keys=True))
            print('''
            One object shows the number of clients that used the 2.4 band yesterday

            One object shows the number of clients that used the 2.4 GHz band today
            ''')

        elif option == 2:
            response = dashboard.wireless.getNetworkWirelessClientCountHistory(network_id, timespan="172800", band="5")
            print(json.dumps(response, indent=2, sort_keys=True))
            print('''
            One object shows the number of clients that used the 5 band yesterday

            One object shows the number of clients that used the 5 GHz band today
            ''')
        
        elif option == 3:
            response = dashboard.wireless.getNetworkWirelessClientCountHistory(network_id, timespan="172800", band="6")
            print(json.dumps(response, indent=2, sort_keys=True))
            print('''
            One object shows the number of clients that used the 6 band yesterday

            One object shows the number of clients that used the 6 GHz band today
            ''')

        else:
            print("Invalid Option")

        print()    
        menu()
        option = int(input("Enter desired menu option: "))
    

menu()
option = int(input("Enter desired menu option: "))

while option != 0:
    
    if option == 1:
        print()
        API_KEY = input("Please Enter your Meraki Dashboard API key: ")
        dashboard = meraki.DashboardAPI(API_KEY)

    elif option == 2:
        response = dashboard.organizations.getOrganizations()
        json_pretty(response)
    
    elif option == 3:
        org_id = input("Please Enter the Organization ID (found in menu option[2]): ")
        response = dashboard.organizations.getOrganizationNetworks(org_id)
        json_pretty(response)
    
    elif option == 4:
        net_id = input("Please Enter the Network ID (found in option[3]): ")
        response = dashboard.networks.getNetworkDevices(net_id)

    elif option == 5:
        client_band_history(API_KEY)

    elif option == 6:
        print("This Option requires a csv file be provided containing AP inventory data (Hostnames, Serials).")
        csv_check = input("Enter Y if you have this file ready: ")

        if csv_check == "Y":
            print("This is where you will do one of two options:")
            print("[1] Enter full path to the CSV")
            print("[2] Use the AP_CSV.csv document that is in the same directory as this python script.") 
            print()
            print("If it is in the same directory then just specify the full csv filename 'AP_CSV.csv'")
            csv_path = input("Enter the path to the CSV here (Quotes not needed): ")
            net_id = input("Please Enter the Network ID (found in option[3]): ")
            with open(str(csv_path)) as inv_data:
                data = csv.DictReader(inv_data)
                serials = []
                for colmn in data:
                    serials.append(colmn['Serial'])
            #Statement below must be ran for option 6
            dashboard.networks.claimNetworkDevices(net_id, serials)
            #print(serials)

        else:
            print("Exiting to Menu..")
            pass

    elif option == 7:
        print("This Option requires a csv file be provided containing AP inventory data (Hostnames, Serials).")
        csv_check = input("Enter Y if you have this file ready: ")

        if csv_check == "Y":
            print("This is where you will do one of two options:")
            print("[1] Enter full path to the CSV")
            print("[2] Use the AP_CSV.csv document that is in the same directory as this python script.") 
            print()
            print("If it is in the same directory then just specify the full csv filename 'AP_CSV.csv'")
            csv_path = input("Enter the path to the CSV here (Quotes not needed): ")
            net_id = input("Please Enter the Network ID (found in option[3]): ")
            with open(csv_path) as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')
                line_count = 0
                for row in csv_reader:
                    if line_count == 0:
                        print(f'Column names are{", ".join(row)}')
                        line_count += 1
                    else:
                        print('Attempting to rename device')

                        #Statement below must be ran for option 6
                        #dashboard.devices.updateDevice(row[1], name=row[0])
                        print(row[1], row[0])

        else:
            print("Exiting to Menu..")
            pass

    else:
        print("Invalid Option")

    print()    
    menu()
    option = int(input("Enter desired menu option: "))


print("Goodbye.")