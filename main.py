from event_parser.parsers import *
from API.api_helpers import *
import json

def showMenu():
    print ("\nExample menu")
    print ("-----------------")
    print ("1) all operations in the binary file")
    print ("2) operations of a specific class")
    print ("3) operations between two timestamps\n")
    choice=int(input("Enter your choice: "))
    return choice



def main():
   choice = showMenu()
   if choice==1:
      formatted_display(  extract_data(read_data("tests/event_stream_2.bin"))) 
   elif choice ==2:
      classs=int(input("Enter the class you are searching for: "))
      formatted_display( research_of_a_specific_class("tests/event_stream_2.bin", classs)) 
   elif choice==3:
      t1=int(input("timestamp 1= "))
      t2=int(input("timestamp 2= "))
      formatted_display( events_between_two_timetamps("tests/event_stream_2.bin", t1, t2)) 
   #518356433086935, 1398450859550059)) 

   
if __name__ == "__main__":
   main()