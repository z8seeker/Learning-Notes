class HashTable:
    """
    use linear probing method to resolve collision
    """
    def __init__(self, size=11):
        self.size = size
        self.len = 0
        self.slots = [None] * self.size
        self.data = [None] * self.size

    def put(self, key, value):
        slot = self._find_slot(key, insert=True)
        if slot is not None:
            self.slots[slot] = key
            self.data[slot] = value
        else:
            raise ValueError("Table is full!")

    def get(self, key):
        exist_key = self._find_slot(key)
        if exist_key:
            slot = self._find_slot(key, insert=True)
            return self.data[slot]
        else:
            return None

    def delete(self, key):
        exist_key = self._find_slot(key)
        if exist_key:
            slot = self._find_slot(key, insert=True)
            self.slots[slot] = None
            self.data[slot] = None
            self.len -= 1

    def __getitem__(self, key):
        return self.get(key)

    def __setitem__(self, key, value):
        return self.put(key, value)

    def __delitem__(self, key):
        return self.delete(key)

    def __len__(self):
        return self.len

    def _find_slot(self, key, insert=False):
        initial = hash_value = self.hash(key)
        while True:
            if self.slots[hash_value] is None:
                if insert:
                    self.len += 1  # add a new key/value pair
                    return hash_value
                else:
                    return False
            else:
                if self.slots[hash_value] == key:
                    if insert:
                        return hash_value  # replace
                    else:
                        return True
                else:
                    hash_value = self.rehash(hash_value)
                    if initial == hash_value:
                        # traversal visit the table, and not find
                        return None

    def hash(self, key):
        return key % self.size

    def rehash(self, old_hash_value):
        return (1 + old_hash_value) % self.size


class ResizableHashTable(HashTable):
    MIN_SIZE = 11
    def __init__(self):
        super().__init__(self.MIN_SIZE)

    def put(self, key, value):
        super().put(key, value)
        if self.len > (self.size * 2) // 3:
            self.resize()

    def resize(self):
        keys, values = self.slots, self.data
        self.size = 1 + self.size * 2  # this will be the new size
        self.len = 0
        self.slots = [None] * self.size
        self.data = [None] * self.size
        for key, value in zip(keys, values):
            if key is not None:
                self.put(key, value)
