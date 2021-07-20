import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),os.path.pardir)))
import json

class Event:
    def __init__(self, class_of_operation, operation, t, data):

        self.c = class_of_operation
        self.o = operation
        self.t = t
        self.data = data


def initialise_list_of_events(config_file):
    with open(config_file) as f:
        return (json.load(f))

def read_data(file_path):
    with open(file_path, 'rb') as file:
        bufferr = file.read()
    return(bufferr)

