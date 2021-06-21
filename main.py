#import sys
#sys.path.insert(1,'C:/Users/LENOVO/Master/event_parser/package/')
from event_parser.parsers import *


def main():
  # c=read_data("tests/event_stream1.bin")
   c=read_data("tests/event_stream_2.bin")
   formatted_display(  extract_data(c)) 
   

if __name__ == "__main__":
   main()