# Source: This code file  follows the WGU Let's GO Hashing Webinar.
# https://wgu.hosted.panopto.com/Panopto/Pages/Viewer.aspx?id=f08d7871-d57a-496e-a6a1-ac7601308c71

#Note key is the package_id
#HashTable class using chaining to avoid collisions
class HashTableWithChaining:
    # Constructor with optional initial capacity parameter.
    # Assigns all buckets with an empty list.
    def __init__(self, initial_capacity=10):
        # initialize the hash table with empty bucket list entries.
        self.table = []
        for i in range(initial_capacity):
            self.table.append([])

    #inserts new item into the hash table
    def insert(self, key, item):  # does both insert and update
        # get the bucket list where this item will go.
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]

        # update key if it is already in the bucket
        for kv in bucket_list:
            if kv[0] == key:
                kv[1] = item
                return True
        # if not, insert the item to the end of the bucket list.
        key_value = [key, item]
        bucket_list.append(key_value)
        return True

    #searches the hash table for an item with the matching key.
    def search(self, key): #search for pacakgaes with package_id as the key
        # get the bucket list where this key would be.
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]

        # search for the key in the bucket list
        for kv in bucket_list:
            if kv[0] == key: #only chooses the correct package_id from the bucket
                return kv[1]
        return None

    #same search function but only returns the componets needed for viewing delivery status
    def search_delivery_components(self, key): #search for pacakgaes with package_id as the key
        # get the bucket list where this key would be.
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]

        # search for the key in the bucket list
        for kv in bucket_list:
            if kv[0] == key: #only chooses the correct package_id from the bucket
                #adds only the status component to a string and returns the string
                components= f" {kv[1].address } with a deadline of {kv[1].delivery_deadline} "
                return components
        return None

    #Removes an item from the hash table that has a matching key
    def remove(self, key):
        # get the bucket list where this item will be removed from.
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]

        # remove the item from the bucket list if it is present.
        for kv in bucket_list:
            if kv[0] == key:
                bucket_list.remove([kv[0], kv[1]])



