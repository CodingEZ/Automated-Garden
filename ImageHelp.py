import numpy as np
from matplotlib import pyplot as plt

def equalArray(array1, array2):
    '''Use if guaranteed non-empty deep arrays.'''
    if array2 is None:
        if array1 is None:
            return True
        else:
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

def display(imgNames, imgs):
    numImgs = len(imgNames)
    #plt.figure(num=1, figsize=(4*numImgs, 4))
    plt.figure(num=1, figsize=(2*numImgs, 4*((numImgs+1)//2)))
    for i in range(numImgs):
        #plt.subplot(1,numImgs,i+1)
        plt.subplot((numImgs+1)//2, 2, i+1)
        plt.imshow(imgs[i], 'gray')
        plt.title(imgNames[i])
    plt.show()

