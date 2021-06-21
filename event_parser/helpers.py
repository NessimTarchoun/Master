class Event:

    def __init__(self, class_of_operation, operation, t, data):

        self.c = class_of_operation
        self.o = operation
        self.t = t
        self.data = data


def initialise_list_of_events():
    # argument for file
    import json
    with open('events_config.json') as f:
        return (json.load(f))


def read_data(file_path):
    with open(file_path, 'rb') as file:
        bufferr = file.read()
    return(bufferr)
