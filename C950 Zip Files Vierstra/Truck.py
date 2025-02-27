import Package
import HashTable

#Creating the Truck class
class Truck:
    def __init__(self, name, capacity, avg_speed, packages, miles, curr_address, depart_time):
        self.name = name
        self.capacity = capacity
        self.avg_speed = avg_speed
        self.packages = packages
        self.miles = miles
        self.curr_address = curr_address
        self.depart_time = depart_time
        self.elapse_time = depart_time

    def __str__(self):
        return "%s, %s, %s, %s, %s, %s, %s" % (self.name, self.capacity, self.avg_speed, self.packages,
                                             self.miles, self.curr_address, self.depart_time)

