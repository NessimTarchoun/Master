import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),os.path.pardir)))
import random
import unittest

#from API.api import *
from API.back_end import *

class Backend_Test_Suite(unittest.TestCase):
    def test_write_json_files(self):
        write_operations_in_json_file("./event_stream1.bin","./test_events.json")
        with open('./test_events.json') as json_file:
            events=json.load(json_file) 
        list_of_classs=(initialise_list_of_events("../events_config.json"))  
        self.assertIsNotNone(list_of_classs, "Unable to exttract mist of main classes")
    def test_extract_events(self):
        with open('./test_events.json') as json_file:
            events=json.load(json_file) 
        self.assertIsNotNone(events, "Unable to extract Data from the binary file")
    def test_searching_classes(self):
        searched_class= random.randint(1,8)
        number_of_classes=len(initialise_list_of_events("../events_config.json")['main_classes']) +1

        
        self.assertEqual(len(percentage_of_class(filepath="test_events.json",class_searched=searched_class)), number_of_classes)

    def test_debugguing_data(self):
        self.assertNotEqual(debugging_data('./test_events.json'),"Error while searching for Debugging Event/data")

    def test_decode_JSON_events(self):
        self.assertIsNotNone( decode_JSON_events('./test_events.json') )

if __name__ == "__main__":
    unittest.main()
