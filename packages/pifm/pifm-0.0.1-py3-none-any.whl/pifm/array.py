class Array(list):
    """
    `Array` is a python list, with a few handy features:
    * if `array = Array()`, `array[len(array)]` can be assigned to (i.e. append to the array)
    * slices of Array are also Array.
    """

    def __add__(self, rhs):
        return Array(list.__add__(self, rhs))

    def __getslice__(self,i,j):
        return Array(list.__getslice__(self, i, j))

    def __mul__(self,other):
        return Array(list.__mul__(self,other))

    def __getitem__(self, item):
        result = list.__getitem__(self, item)
        if type([]) == type(result):
            return Array(result)
        else:
            return result

    def __setitem__(self, key, new_value):
        if key == len(self):
            self.append(new_value)
        else:
            super().__setitem__(key, new_value)
