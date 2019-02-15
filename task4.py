import parser_data_1
from plot_data import plot_data
import matplotlib.pyplot as plt
from scipy.signal import butter, lfilter, find_peaks
import util

order = 6
fs = 25.0
cutoff = 4


def butter_lowpass(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return b, a


def butter_lowpass_filter(data, cutoff, fs, order=5):
    b, a = butter_lowpass(cutoff, fs, order=order)
    y = lfilter(b, a, data)
    return y


def segment_climbing_walking(data):
    '''
    While collecting data on stairs there were times when you were also walking rather than climbing
    It is importing to remove the parts from the data where you were walking in between the flight of stairs
    Write your own algorithm to find segments in data which corresponds to climbing only

    This functions returns
    List of tuples (x,y,z) which corresponds to climbing only.
    i.e. remove data points from the original data which corresponds to walking
    '''

    print('segment_climbing_walking')
    # Further parsing the data
    time_arr = []
    x_arr = []
    y_arr = []
    z_arr = []
    baro_arr = []
    mag_arr = []
    for entry in data:
        time, x, y, z, baro = entry
        mag_arr.append((time, x, y, z))
        time_arr.append(time)
        x_arr.append(x)
        y_arr.append(y)
        z_arr.append(z)
        baro_arr.append(baro)
    new_data = util.vector_magnitude(mag_arr)
    # plt.title("climbing_steps_clean.csv Pre-segmented Barometer")
    # plt.plot(baro_arr)
    # plt.show()
    # Getting moving average
    N = 80
    cumsum, moving_aves = [0], []
    for i, x in enumerate(baro_arr[5:], 1):
        cumsum.append(cumsum[i-1] + x)
        if i >= N:
            moving_ave = (cumsum[i] - cumsum[i-N])/N
            moving_aves.append(moving_ave)
    climbing = []
    walking = []
    for i in range(len(moving_aves) - 1):
        if moving_aves[i] > moving_aves[i + 1]:
            climbing.append(i)
        else:
            walking.append(i)
        vals = []
    for entry in climbing:
        vals.append(baro_arr[entry])
    plt.title("climbing_steps_clean.csv Segmented Climbing Barometer")
    plt.scatter(climbing, vals)
    plt.show()
    return climbing


def count_steps(data):
    print('count_steps')
    num_steps = 0
    '''
    This function counts the number of steps in data and returns the number of steps
    '''
    vals = []
    for entry in data:
        vals.append(new_data[entry])

    plt.subplot(2, 1, 2)
    plt.plot(vals, 'b-', label='Raw Magnitude')
    y = butter_lowpass_filter(vals, cutoff, fs, order)
    y2 = y[5:-1]
    plt.plot(y2, 'r-', linewidth=2, label='Lowpass Filter')
    res = find_peaks(y2)
    plt.xlabel('Time [sec]')
    plt.grid()

    num_steps = len(res[0])
    pvals = []
    for entry in res[0]:
        pvals.append(vals[entry])
    plt.title("climbing_steps_clean.csv Number of Steps")
    plt.legend()
    plt.scatter(res[0], pvals, color="green")
    plt.show()
    print(num_steps)
    return num_steps


def main():
    # Get data
    file_name = "climb_steps_clean.csv"  # Change this to your data file name
    data = parser_data_1.get_data(file_name)

    segmented_data = segment_climbing_walking(data)
    number_of_steps = count_steps(segmented_data)
    # print ("Number of steps counted are :{0:d}".format(number_of_steps))


if __name__ == "__main__":
    main()
