import util
import matplotlib.pyplot as plt
from plot_data import plot_data
import parser_data
from scipy.signal import butter, lfilter, find_peaks
import numpy as np

order = 6
fs = 30.0
cutoff = 3.667

def butter_lowpass(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return b, a

def butter_lowpass_filter(data, cutoff, fs, order=5):
    b, a = butter_lowpass(cutoff, fs, order=order)
    y = lfilter(b, a, data)
    return y

def count_steps(data, title):
    print("Accelerometer data graph")
    # plot_data(data)
    num_steps = 0
    '''
    ADD YOUR CODE HERE. This function counts the number of steps in data and returns the number of steps
    '''
    data = util.vector_magnitude(data, plot = False)
    plt.subplot(2, 1, 2)
    plt.plot(data, 'b-', label='Raw Magnitude')
    y = butter_lowpass_filter(data, cutoff, fs, order)
    y2=y[5:-1]
    plt.plot(y2, 'r-', linewidth=2, label='Lowpass Filter')
    res = find_peaks(y2)
    plt.xlabel('Time [sec]')
    plt.grid()

    num_steps = len(res[0])
    vals = []
    for entry in res[0]:
      vals.append(data[entry])
    plt.title(title)
    plt.legend()
    plt.scatter(res[0], vals, color = "green")
    plt.show()
    return num_steps

def main():
    # Get data
    file_name = "walking_steps_1_clean.csv"  # Change to your file name
    data = parser_data.get_data(file_name)
    util.vector_magnitude(data, "walking_steps_1_clean.csv Magnitude")
    file_name2 = "walking_steps_2_clean.csv"  # Change to your file name
    data2 = parser_data.get_data(file_name2)
    util.vector_magnitude(data2, "walking_steps_2_clean.csv Magnitude")
    util.moving_average(data, 5, "walking_steps_1_clean.csv Moving Average")
    util.moving_average(data2, 5, "walking_steps_1_clean.csv Moving Average")
    number_of_steps = count_steps(data, "walking_steps_1_clean.csv Number of Steps")
    print ("Number of steps counted are :{0:d}".format(number_of_steps))
    number_of_steps2 = count_steps(data2, "walking_steps_2_clean.csv Number of Steps")    
    print ("Number of steps counted are :{0:d}".format(number_of_steps2))

if __name__== "__main__":
  main()

