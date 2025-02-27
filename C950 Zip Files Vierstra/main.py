# Jacob Vierstra
# StudentID: 010903152
# C950 DSA2 WGUPS Project

import csv
import datetime
from Package import my_package_hash
from Truck import Truck

#getting distance data from CSV file
#def load_distances(address_list):
with open('CSV/WGUPS_Distance_Table.csv') as csv_data:
    distance_data = csv.reader(csv_data)
    distance_data = list(distance_data)

# Loads address data from CSV file
def load_address_data():
    address_dict = {}
    with open('CSV/WGUPS_Address_Table.csv') as addresses:
        #next(addresses)
        address_data = csv.reader(addresses, delimiter=',') # # uses ',' to differentiate address components
        counter = 0
        for address in address_data: #Loop for getting the correct indexes in the CSV for each address
            address_dict[address[2].lstrip().split('\n')[0]] = counter
            counter += 1
        return address_dict

#determines the distances between two addresses
def distance_matrix(address, address1):
    index = address_dict[address]
    index1 = address_dict[address1]
    if distance_data[index][index1] == "": #if no value is returned flips the indexes to return the distance
        return float(distance_data[index1][index])
    return float(distance_data[index][index1])

address_dict = load_address_data()

#Intializing the three trucks
truck1 = Truck(1, 16, 18, [1,6,13,14,15,16,19,20,25,29,30,31,34,37,40], 0, "4001 South 700 East", datetime.timedelta(hours=8, minutes=0) )
truck2 = Truck(2, 16, 18, [3,5,7,8,9,10,27,35,36,38,39], 0, "4001 South 700 East", datetime.timedelta(hours=10, minutes=20) )
truck3 = Truck(3, 16, 18, [2,4,11,12,17,18,21,22,23,24,26,28,32,33], 0, "4001 South 700 East", datetime.timedelta(hours=9, minutes=5) )

package_depart_time = {} #create dictionary for determining if package are at hub or in route.

#function to return the truck number based off of the package ID
def get_truck_number(i):
    truck_num_1 = [1,6,13,14,15,16,19,20,25,29,30,31,34,37,40]
    truck_num_2 = [3,5,7,8,9,10,27,29,35,36,37,38,39]
    truck_num_3 = [2,4,11,12,17,18,21,22,23,24,26,28,32,33]
    if i in truck_num_1:
        return 'Truck 1'
    elif i in truck_num_2:
        return 'Truck 2'
    elif i in truck_num_3:
        return 'Truck 3'



#formats the datetime to be able to manipulate and determine package delivery time
def format_datetime(value):
    total_seconds = int(value.total_seconds())
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours:02}:{minutes:02}:{seconds:02}"


#Nearest neighbor algorithm with a time complexity of O(N^2)
#Starts at the hub and determines which package on the truck to delivery by whichever address is closest
#Loops until all packages are delivered
def delivery_path(truck):
    package_log = {}
    package_on_truck = truck.packages
    package_delivered = [] #creates empty list to know what packages have been delivered
    #Sets packages depart time to when the truck leaves
    for package in truck.packages:
        package_depart_time[package] = truck.depart_time

    while package_on_truck:
        next_delivery = None #next address the truck visits
        closest_delivery = 999 #set to 999 since the closest delivery is always less
        for package_id in package_on_truck:
            package = my_package_hash.search(package_id)
            package.status = "en route"
            distance = distance_matrix(truck.curr_address, package.address)
            if distance < closest_delivery:
                closest_delivery_address = package.address
                closest_delivery = distance
                next_delivery = package
        truck.curr_address = closest_delivery_address
        truck.miles += closest_delivery
        next_delivery.status = f'Delivered at {format_datetime(truck.depart_time + datetime.timedelta(minutes=truck.miles/18*60))}'
        package_on_truck.remove(next_delivery.package_id) #Removes package from list for being on the truck
        package_delivered.append(next_delivery.package_id) #Adds to list of delivered packages
    truck.packages = package_delivered
    truck.miles += distance_matrix(truck.curr_address,  '4001 South 700 East') #Trucks returns back to HUB
    format_datetime(truck.depart_time + datetime.timedelta(minutes=truck.miles / 18 * 60))



#Determine delivery path for each truck using the algorithm
delivery_path(truck1)
delivery_path(truck2)
delivery_path(truck3)

#Determines where the package is at a given time
def determine_package(time, packageID):
    package = my_package_hash.search(packageID)
    time_entered = datetime.time(int(time[0]),int(time[1]),int(time[2]))

    #updates the wrong address of package 9 at 10:20:00
    if packageID == 9:
        if time_entered < datetime.time(10,20,00):
            package.address = "300 State St"
            package.zip_code = "84103"
        else:
            package.address = "410 S State St"
            package.zip_code = "84111"

    depart_time = format_datetime(package_depart_time[packageID])
    packages_en_route_at = datetime.time(int(depart_time[:2]),int(depart_time[3:5]),int(depart_time[6:]))

    package_status = "At the hub"

    if len(package.status) > 11:  # not delivered yet
        # gets time package was delivered in correct format
        package_delivered_at = datetime.time(int(package.status[-8:-6]), int(package.status[-5:-3]),int(package.status[-2:]))
        # logic to know if the package status compared to the time entered
        if time_entered >= package_delivered_at:
            package_status = package.status
            return package_status
    if time_entered >= packages_en_route_at: #package.departure time
        package_status = "En route"

    return package_status

#Returns the status of a chosen package at a choosen time
def get_single_package_status(choose_package, choose_time):
    package_status = ''
    package_status = (determine_package(choose_time, choose_package)) #determines that status and stores it in a string to use in print function
    determine_package(choose_time, choose_package)
    print(f'Package {choose_package} is on {get_truck_number(choose_package)} with the status {package_status} with address of'
            f'{my_package_hash.search_delivery_components(choose_package)}')

#Returns the status of all packages at a given time in HH:MM:SS format
def get_all_package_status(time):
    package_status = []
    for i in range(1,41): #loops through all 40 packes
        package_status.append(determine_package(time, i))
    for index, status in enumerate(package_status):
        print(f'Package {index + 1} is on {get_truck_number(index + 1)} with the status {status} with address of'
              f'{my_package_hash.search_delivery_components(index + 1)}')


#Command Line Interface that is interactive
# Gets  total miles of all trucks, any package at any time, and all packages at any times

print("---------------------------------------------------------")
print("Welcome to the finest postal service in the West, WGUPS!")
print("---------------------------------------------------------")

text = ''

#Keep running until 'exit' is entered
#Programmed responses based on inputs '1', '2', '3', and 'exit'
while text != 'exit' :
    text = input('What would you like to know? Press the number to continue \n'
                 '1. Total miles? \n'
                 '2. Get a single package status \n'
                 '3. Get all package status \n'
                 '4. Type "exit" to end program \n')

    # Returns total miles of all three trucks
    if text == '1':
        print("You selected: Total miles.")
        print(f'The total miles traveled to deliver all 40 packages is: {truck1.miles + truck2.miles + truck3.miles} miles \n')

    # Returns location of any package at anytime
    elif text == '2':
        choose_package = int(input('you selected: single package status. please enter package id.'))
        choose_time = input('Please enter a time in (Format HH:MM:SS) \n').split(':')
        get_single_package_status(choose_package, choose_time)

    #Returns location of all packages at any time
    elif text == '3':
        choose_time = input('Please enter a time in (Format HH:MM:SS) \n').split(':')
        get_all_package_status(choose_time)

    # Exits and ends the program
    elif text == 'exit':
        print("You selected: exit. Goodbye")
    else:
        print("Invalid option. Please enter 1, 2, 3, or exit.")


