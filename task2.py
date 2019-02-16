import parser_data
import parser_climb_data
from plot_data import plot_data
import csv


def clean_data(data, start, end, file_name):
    print("Write codprint(data)e to remove garbage data")
    data = data[start:end]

    print("Create new file without garbage data and save it in data folder")
    file_name_clean = file_name

    with open(file_name_clean, 'wb') as f:
        writer = csv.writer(f, delimiter=',')
        writer.writerows(data)


def main():
    # Get data
    file_name = "walking_steps_1.csv"  # Change to your file name
    data = parser_data.get_data(file_name)  # data -- time,X,Y,Z
    plot_data(data)
    clean_data(data, 114, 1140, "walking_steps_1_clean.csv")
    plot_data(parser_data.get_data("walking_steps_1_clean.csv"))

    file_name_2 = "walking_steps_2.csv"
    data2 = parser_data.get_data(file_name_2)
    plot_data(data2)
    clean_data(data2, 31, 1007, "walking_steps_2_clean.csv")
    plot_data(parser_data.get_data("walking_steps_2_clean.csv"))

#     file_name_3 = "climb_steps.csv"
    # data3 = parser_data.get_data("walking_steps_2.csv")
    # plot_data(data3)
    # data4 = parser_data.get_data("walking_steps_2_clean.csv")
    # plot_data(data4)
#     clean_data(data, 154, 950, "climb_steps_clean.csv")


if __name__ == "__main__":
    main()
