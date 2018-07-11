import numpy as np

def equalArray(array1, array2):
    '''Use if guaranteed non-empty deep arrays.'''
    if array2 is None:
        if array1 is None:
            return True
        return False
    elif len(array1) != len(array2):
        return False
    elif isinstance(array1[0], int) or isinstance(array1[0], np.uint8):
        for index in range(len(array1)):
            if array1[index] != array2[index]:
                return False
        return True
    else:
        for index in range(len(array1)):
            if not equalArray(array1[index], array2[index]):
                return False
        return True

