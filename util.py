from scipy.signal import butter, lfilter
import matplotlib.pyplot as plt
import numpy

def vector_magnitude(data, title = "", plot = True):
    """ function to calculate the magnitude of a vector

    Calculate the magnitude of the vector superposition of data (for
    example, acceleration) on x, y, and z axis

    Arguments:
        data: array of (x, y, z) tuples for a vector

    Returns:
        array of the magnitude of a vector

    """
    result = []
    for entry in data:
        time, x, y, z = entry
        mag = ((x ** 2) + (y ** 2) + (z ** 2)) ** .5
        result.append(mag)
    if plot == True:
        plt.title(title)
        plt.plot(result)
        plt.show()
    return result



def moving_average(data, window_size, title):
    """ moving average filter

    Implement a simple moving average filter to use as a low pass
    filter

    Arguments:
        data: data be filtered
        window_size: window_size chosen for the data

    Returns:
        The filtered data.

    TODO:
        Finish this function. Think about how you want to handle
        the size difference between your input array and output array.
        You can write it yourself or consider using numpy.convole for
        it:
        https://docs.scipy.org/doc/numpy/reference/generated/numpy.convolve.html

    """
    mylist = vector_magnitude(data, plot = False)
    N = window_size
    cumsum, moving_aves = [0], []

    for i, x in enumerate(mylist, 1):
        cumsum.append(cumsum[i-1] + x)
        if i>=N:
            moving_ave = (cumsum[i] - cumsum[i-N])/N
            moving_aves.append(moving_ave)
    plt.title(title)
    plt.plot(moving_aves)
    plt.show()




