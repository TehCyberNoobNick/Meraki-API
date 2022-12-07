# Written By: Nicholas Cawthon-Church
# Date: 12/6/2022

import meraki
import json


API_KEY = input("Enter your Meraki Dashboard API key: ")
dashboard = meraki.DashboardAPI(API_KEY)

response = dashboard.organizations.getOrganizations()
print(json.dumps(response, indent=2, sort_keys=True))
print("This is a list of Organizations on your Dashboard. Copy the desired Organizations ID.")
print()
input("Press Enter to continue...")

org_id = input("Enter the desired Organization ID: ")
response = dashboard.organizations.getOrganizationNetworks(org_id)
print(json.dumps(response, indent=2, sort_keys=True))
print("This is a list of all Networks in the desired Organization. Copy the desired Network ID.")
print()
input("Press Enter to continue...")

network_id = input("Enter desired Network ID: ")


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


print("Goodbye.")