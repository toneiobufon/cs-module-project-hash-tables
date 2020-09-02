class HashTableEntry:
    """
    Linked List hash table key/value pair
    """
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None


# Hash table can't have fewer than this many slots
MIN_CAPACITY = 8


class HashTable:
    """
    A hash table that with `capacity` buckets
    that accepts string keys

    Implement this.
    """

    def __init__(self, capacity):

        # Your code here
        self.capacity = capacity
        self.size = 0
        self.contents = [None]*capacity


    def get_num_slots(self):
        """
        Return the length of the list you're using to hold the hash
        table data. (Not the number of items stored in the hash table,
        but the number of slots in the main list.)

        One of the tests relies on this.

        Implement this.
        """
        # Your code here
        return self.capacity


    def get_load_factor(self):
        """
        Return the load factor for this hash table.

        Implement this.
        """
        # Your code here
        lofactor = self.size/self.capacity
        
        return lofactor


    def fnv1(self, key):
        """
        FNV-1 Hash, 64-bit

        Implement this, and/or DJB2.
        """

        # Your code here
        FNV_prime = 0x100000001b3 
        offset_basis = 0xcbf29ce484222325

        hash = offset_basis
        for k in key:
            # This is the "clamping" part
            hash = hash * FNV_prime
            hash = hash ^ ord(k)
        return hash


    def djb2(self, key):
        """
        DJB2 hash, 32-bit

        Implement this, and/or FNV-1.
        """
        # Your code here
        hash = 5381
        for n in key:
            hash = (hash * 33) + ord(n)
        return hash



    def hash_index(self, key):
        """
        Take an arbitrary key and return a valid integer index
        between within the storage capacity of the hash table.
        """
        # return self.fnv1(key) % self.capacity

        return self.djb2(key) % self.capacity

    def put(self, key, value):
        """
        Store the value with the given key.

        Hash collisions should be handled with Linked List Chaining.

        Implement this.
        """
        # Your code here
        #day one
        # newNode = HashTableEntry(key, value)
        # newIndex = self.hash_index(key)
        # self.contents[newIndex] = newNode
        # self.size +=1

        #day two, to avoid collision
       
        keyIndex = self.hash_index(key)

        if self.contents[keyIndex] is None:

            newNode = HashTableEntry(key, value)
            newIndex = self.hash_index(key)
            self.contents[newIndex] = newNode

            newNode.next = None
            self.size +=1

        curNode = self.contents[keyIndex]
        while curNode:
            if curNode.key == key:
                curNode.value = value
            else:
                oldHead = curNode
                newNode = HashTableEntry(key, value)
                self.contents[keyIndex] = newNode
                newNode.next = oldHead
                self.size +=1
            curNode = curNode.next

        #increase size if bigger than 0.7    
        if self.get_load_factor() > 0.7:
            newLimit = self.capacity*2
            self.resize(newLimit)




    def delete(self, key):
        """
        Remove the value stored with the given key.

        Print a warning if the key is not found.

        Implement this.
        """
        # Your code here
        #day one
        # indexOfKey = self.hash_index(key)
        # deleted = self.contents[indexOfKey]
        # self.contents[indexOfKey] = None
        # return deleted

        #day two, to avoid collision
        indexOfKey = self.hash_index(key)

        if self.contents[indexOfKey] is None:
            return None
        if self.contents[indexOfKey].key == key:
            self.size -=1
            self.contents[indexOfKey] = self.contents[indexOfKey].next
            return key
        else:
            if self.contents[indexOfKey].next is None:
                return None
            prevNode = None
            curNode = self.contents[indexOfKey]

            while curNode:
                if curNode.key == key:
                    prevNode.next = curNode.next
                    self.size -=1
                    return key
                
                prevNode = curNode
                curNode = curNode.next






    def get(self, key):
        """
        Retrieve the value stored with the given key.

        Returns None if the key is not found.

        Implement this.
        """
        # Your code here
        #day one
        # lookup = self.hash_index(key)

        # if self.size == 0:
        #     return None
        # if self.contents[lookup] is None:
        #     return None
        # else:
        #     return self.contents[lookup].value

        #day two, to avoid collision
        lookup = self.hash_index(key)
        curNode = self.contents[lookup]

        if self.size == 0:
            return None
        
        if self.contents[lookup] is None:
            return None
        
        while curNode is not None:
            if curNode.key == key:
                return curNode.value
            curNode = curNode.next


            



    def resize(self, new_capacity):
        """
        Changes the capacity of the hash table and
        rehashes all key/value pairs.

        Implement this.
        """
        # Your code here
        #hash table refers to new array
        self.capacity = new_capacity
        # new arra with double the capacity of old array
        oldList = [None]* self.capacity

        self.contents = self.contents + oldList

        for i in range(self.capacity):
            entry = self.contents[i]

            if entry is not None:
                curNode = self.contents[i]

                while curNode:
                    self.delete(self.contents[i].key)

                    self.put(curNode.key, curNode.value)
                    curNode = curNode.next
                    





if __name__ == "__main__":
    ht = HashTable(8)

    ht.put("line_1", "'Twas brillig, and the slithy toves")
    ht.put("line_2", "Did gyre and gimble in the wabe:")
    ht.put("line_3", "All mimsy were the borogoves,")
    ht.put("line_4", "And the mome raths outgrabe.")
    ht.put("line_5", '"Beware the Jabberwock, my son!')
    ht.put("line_6", "The jaws that bite, the claws that catch!")
    ht.put("line_7", "Beware the Jubjub bird, and shun")
    ht.put("line_8", 'The frumious Bandersnatch!"')
    ht.put("line_9", "He took his vorpal sword in hand;")
    ht.put("line_10", "Long time the manxome foe he sought--")
    ht.put("line_11", "So rested he by the Tumtum tree")
    ht.put("line_12", "And stood awhile in thought.")

    print("")

    # Test storing beyond capacity
    for i in range(1, 13):
        print(ht.get(f"line_{i}"))

    # Test resizing
    old_capacity = ht.get_num_slots()
    ht.resize(ht.capacity * 2)
    new_capacity = ht.get_num_slots()

    print(f"\nResized from {old_capacity} to {new_capacity}.\n")

    # Test if data intact after resizing
    for i in range(1, 13):
        print(ht.get(f"line_{i}"))

    print("")
