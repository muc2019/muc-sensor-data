import parser_climb_data
from plot_data import plot_data
import matplotlib.pyplot as plt
from scipy.signal import butter, lfilter, find_peaks
import util
import csv

order = 6
fs = 25.0
cutoff = 4

def clean_data(data, start, end, file_name):
    print("Write codprint(data)e to remove garbage data")
    data = data[start:end]

    print("Create new file without garbage data and save it in data folder")
    file_name_clean = file_name

    with open(file_name_clean, 'wb') as f:
        writer = csv.writer(f, delimiter=',')
        writer.writerows(data)

def parse_data(data):
    baro_arr = []
    mag_arr = []
    for entry in data:
        time, x, y, z, baro = entry
        mag_arr.append((time, x, y, z))
        baro_arr.append(baro)
    plot_data(mag_arr)
    plt.title("climb_steps_clean.csv Pre-segmented Barometer")
    plt.plot(baro_arr)
    plt.show()
    return[mag_arr, baro_arr]

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
    mag_arr = data[0]
    baro_arr = data[1]
    mag_data = util.vector_magnitude(mag_arr, plot = False)
    plt.title("climb_steps_clean.csv Segmented Climbing X, Y, Z Magnitude")
    plt.plot(mag_data)
    plt.show()
    plt.title("climb_steps_clean.csv Segmented Climbing Barometer Raw")
    plt.plot(baro_arr)
    plt.show()

    window = 80
    cumsum, moving_aves = [0], []
    for i, x in enumerate(baro_arr[5:], 1):
        cumsum.append(cumsum[i-1] + x)
        if i >= window:
            moving_ave = (cumsum[i] - cumsum[i-window])/window
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
    plt.title("climb_steps_clean.csv Segmented Climbing Barometer Moving Average")
    plt.plot(climbing, vals)
    plt.show()

    m_vals = []
    b_vals = []
    for entry in walking:
        m_vals.append(mag_data[entry])
        b_vals.append(baro_arr[entry])
    plt.title("climb_steps_clean.csv Segmented Walking X, Y, Z Magnitude")
    plt.plot(walking, m_vals)
    plt.show()

    plt.title("climb_steps_clean.csv Segmented Walking Barometer Raw")
    plt.plot(walking, b_vals)
    plt.show()
    return [mag_data, climbing]


def count_steps(data):
    print('count_steps')
    num_steps = 0
    '''
    This function counts the number of steps in data and returns the number of steps
    '''
    mag_data = data[0]
    climbing = data[1]
    vals = []
    for entry in climbing:
        vals.append(mag_data[entry])

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
    file_name = "climb_steps.csv"
    data = parser_climb_data.get_data(file_name)
    clean_data(data, 154, 950, "climb_steps_clean.csv")
    cleaned_data = parser_climb_data.get_data("climb_steps_clean.csv")
    parsed_data = parse_data(cleaned_data)

    segmented_data = segment_climbing_walking(parsed_data)
    number_of_steps = count_steps(segmented_data)
    print ("Number of steps counted are :{0:d}".format(number_of_steps))

if __name__ == "__main__":
    main()
