from event_parser.parsers import *

def main():
  # c=read_data("tests/event_stream1.bin")
   
   formatted_display(  extract_data(read_data("tests/event_stream_2.bin"))) 
   

if __name__ == "__main__":
   main()