import csv
from HashTable import HashTableWithChaining
#This code followed the C950 Webinar 2
# https://wgu.hosted.panopto.com/Panopto/Pages/Viewer.aspx?id=eee77a88-4de8-4d42-a3c3-ac8000ece256


# Creating the Package class
class Package:
    def __init__(self, package_id, address, city, state, zip_code, delivery_deadline, weight, special_notes, status):
        self.package_id = package_id
        self.address = address
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.delivery_deadline = delivery_deadline
        self.weight = weight
        self.special_notes = special_notes
        self.status = status

    def __str__(self):
        return "%s, %s, %s, %s, %s, %s, %s, %s, %s" % (self.package_id, self.address, self.city, self.state, self.zip_code,
                                                      self.delivery_deadline, self.weight, self.special_notes,
                                                      self.status)

#Loads the package data into the hash table
def load_package_data(my_package_hash):
    id_list = []
    with open('CSV/WGUPS_Package_File.csv') as csv_data:
        package_data = csv.reader(csv_data, delimiter=',') # uses ',' to differentiate package components
        next(package_data)  # skips header
        #Each component is at an increasing package index
        for package in package_data:
            package_id = int(package[0])
            address = package[1]
            city = package[2]
            state = package[3]
            zip_code = package[4]
            delivery_deadline = package[5]
            weight = package[6]
            special_notes = package[7]
            status = "At the HUB"
            # package object
            pack = Package(package_id, address, city, state, zip_code, delivery_deadline, weight, special_notes, status)
             # insert it into the hash table
            my_package_hash.insert(package_id, pack)

        return id_list

# Hash table instance
my_package_hash = HashTableWithChaining()

#loads the package data into the hash table
load_package_data(my_package_hash)


#used to demonstrate search/lookup function
#for i in range(1,41):
#    print(my_package_hash.search(i))