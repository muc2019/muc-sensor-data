import parser_data_1
from plot_data import plot_data
import csv



def clean_data(data, start, end, file_name):
    print ("Write codprint(data)e to remove garbage data")
    data = data[start:end]
    
    print ("Create new file without garbage data and save it in data folder")
    file_name_clean = file_name

    with open(file_name_clean, 'wb') as f:
      writer = csv.writer(f, delimiter=',')
      writer.writerows(data)

def main():
    # Get data
    file_name = "climb_steps.csv"  # Change to your file name
#     file_name_2 = "walking_steps_2.csv"
    data = parser_data_1.get_data(file_name) #data -- time,X,Y,Z
#     data2 = parser_data.get_data(file_name_2)
#     clean_data(data, 114, 1140, "walking_steps_1_clean.csv")
    clean_data(data, 154, 950, "climb_steps_clean.csv")


if __name__== "__main__":
  main()

