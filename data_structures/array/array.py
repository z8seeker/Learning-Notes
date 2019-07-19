class Array:
    """an implementation of array ADT
    """
    def __init__(self, size: int)
        self._size = size
        self._data = [None for i in range(size)]
    
    def __getitem__(self, index: int) -> object
        return self._data[index]
    
    def __setitem__(self, index: int, value: object):
        self._data[index] = value
    
    def __len__(self):
        return self._size
    
    def get(self, index: int):
        assert self._size > index, 'index out of range'
        return self._data[index]
    
    def insert(self, index: int, value: object):
        assert self._size > index, 'index out of range'
        self._data[index] = value
    
    def delete(self, index: int):
        assert self._size > index, 'index out of range'
        del self._data[index]
