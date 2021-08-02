import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),os.path.pardir)))

from event_parser.helpers import *
from event_parser.parsers import *
import unittest


class ParserTestSuite(unittest.TestCase):
    """ Test cases for event log parser """

    def test_simple_test(self):
        buff = read_data("tests/event_stream1.bin")
        list_of_classs = initialise_list_of_events()['main_classes']

        # Parse single event, [0] gets the first element of the returned list
        e = extract_data(buff)[0]
        self.assertTrue(e.c in list_of_classs, "Unexpected class.")
        self.assertTrue(e.o in range(16), "Unexpected operation.")
        self.assertNotEqual(e.t, 0, "Unexpected timestamp.")

    def test_debugging_event_data_width_defined(self):
        buff = read_data("tests/event_stream1.bin")
        list_of_classs = initialise_list_of_events()
        e = extract_data(buff)[0]

        if e.c == 6:
            self.assertIsNotNone(
                e.data, list_of_classs['6']['operations'][str(e.c)]['data-width'])


if __name__ == "__main__":
    unittest.main()
