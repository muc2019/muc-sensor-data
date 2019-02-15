from scipy.io.wavfile import read
from optparse import OptionParser
import sys
import os

# Feel free to store stuff in global variable

def prepare_classifier(training_data_files, label):
    print("prepare your classifier here")
    #Below is a hint for you to read audio data
    for training_data_file in training_data_files:
        sample_rate, data = read(training_data_file)

def recognize(file_name):
    # input file_name, output label. Will only run after prepare_classifier is called
    sample_rate, data = read(file_name)


def test(test_data_files, truth_labels):
    recognized_labels = [recognize(test_data_file) for test_data_file in test_data_files]
    # recognized_labels = truth_labels
    points_awarded = 0
    for recognized, truth in zip(recognized_labels, truth_labels):
        if recognized == truth:
            points_awarded = points_awarded + 1
    print('{0:d}/{1:d} correct recognition'.format(points_awarded, len(truth_labels)))
    if points_awarded != len(truth_labels):
        print ('     truth labels: ' + '\t'.join(truth_labels))
        print ('recognized labels: ' + '\t'.join(recognized_labels))
    else:
        print('Congrats! you got 100% correct!')

def grading(training_file_label_tuple_list, testing_file_label_tuple_list):
    prepare_classifier(*zip(*training_file_label_tuple_list))
    test_result = test(*zip(*testing_file_label_tuple_list))

def main():
    parser = OptionParser()
    parser.add_option('--train', action='store', dest='train',
                        default='task5_training_data',
                        help='path to training data. File name in' +
                        'the folder is \'{label_name} {number}.wav\'' +
                        'for example: Blow 4.wav' )
    parser.add_option('--test', action='store', dest='test',
                        default='task5_training_data',
                        help='Path to test data. File name in' +
                        'the folder is \'{label_name} {number}.wav\'' +
                        'for example: Blow 4.wav' )
    options, args = parser.parse_args(sys.argv)
    # print(options)
    if not os.path.exists(options.train):
        print('Trainig folder path does not exist')
    if not os.path.exists(options.test):
        print('Test folder path does not exist')

    training_files = os.listdir(options.train)
    training_file_label_tuple_list = [('{0}/{1}'.format(options.train, file), ' '.join(file.split()[0:-1])) for file in training_files]

    testing_files = os.listdir(options.train)
    testing_file_label_tuple_list = [('{0}/{1}'.format(options.test, file), ' '.join(file.split()[0:-1])) for file in testing_files]

    grading(training_file_label_tuple_list, testing_file_label_tuple_list)

if __name__== "__main__":
  main()


