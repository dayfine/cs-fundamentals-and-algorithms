class HashTable():
    def __init__(self):
        self.size = 31
        self.slots = [None] * self.size
        self.data = [None] * self.size

    def put(self, key, val):
        hashvalue = self.hash(key, len(self.slots))

        if self.slots[hashvalue] = None:
            self.slots[hashvalue] = key
            self.data[hashvalue] = val
        elif self.slots[hashvalue] == key:
            # overwrite
            self.data[hashvalue] = val

        else:
            # collison
            nextslot = self.hash(hashvalue, len(self.slots))

            # while no empty slot and not (having to) override
            while (self.slots[nextslot] != None and
                   self.slots[nextslot] != key):
                #keep rehashing
                nextslot = self.hash(hashvalue, len(self.slots))

            if self.slots[nextslot] == None:
                self.slots[hashvalue] = key
                self.data[hashvalue] = val
            else:
                self.data[hashvalue] = val

    def get(self, key):
        initslot = self.hash(key, len(self.slots))

        position = initslot
        while (self.slots[position] != None and
               self.slots[position] != key):
            position = self.hash(position, len(self.slots))
            if position == initslot:
                return None

        return self.data[position]

    def len(self):
        return self.size

    def hash(self, key):
        return key % self.size

    def __contains__(self, item):
        pass

    def __getitem__(self, key):
        return self.get(key)

    def __setitem__(self, key, val):
        self.put(key, val)

    def __delitem__(self, key):
        pass
