import sys
import os
import json
import numpy as np
from numpy.core.numeric import NaN
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),os.path.pardir)))
from event_parser.parsers import *

def percentage(x,y):
    return (str(round((x/y*100),2)) + '%')

def write_operations_in_json_file(binary_file_path, json_file_name):
    import json
    list = extract_data(read_data(binary_file_path))
    f = open(json_file_name, 'w') 
    data={}

    for i in list:
        data[str(list.index(i))] = {'class_of_operation': i.c,
                'operation': i.o,
                'timestamp': i.t,
                'data': i.data}
    
    json.dump(data, f, ensure_ascii=False, indent= 4, separators=(',', ':'))
    f.close()


def occurence_of_event(filename,*args):
    operation=t1=t2=NaN
    with open(filename,) as json_file:
        events=json.load(json_file)
    if len (args) >= 1:
        classs=args[0]
        if len (args) == 2:
            operation=args[1]
        elif len (args)==3:
            operation=NaN
            t1=args[1]
            t2=args[2]
            
        if len (args)==4:
            operation=args[1]
            t1=args[2]
            t2=args[3]

    else:
        print ('pass at least 1 parameters')
    
    if np.isnan(t1) or np.isnan(t2):
        target_list_of_events=[events[str(i)] for i in range (len(events))]
    else:
        target_list_of_events=[events[str(i)] for i in range (len(events))if ((events[str(i)]['timestamp']) >= t1) and ((events[str(i)]['timestamp']) <= t2)]
    
    if np.isnan(operation) :
        count=0
        for i in range (len(target_list_of_events)):
            if target_list_of_events[i]["class_of_operation"]== classs:
                count+=1
        print ("wanted class",classs,"percentage:",count,'/',len(target_list_of_events) ,'==', percentage (count,len(target_list_of_events)))
    else:
        count=0
        for i in range (len(target_list_of_events)):
            if target_list_of_events[i]["class_of_operation"]== classs and target_list_of_events[i]["operation"]==operation:
                count+=1
        print ("wanted class and ops",classs, operation, "percentage:",count,'/',len(target_list_of_events) ,'==', percentage (count,len(target_list_of_events)))


def debugging_data(filename):
    from tabulate import tabulate

    list_of_dbg_data=[]
    with open(filename) as json_file:
        events=json.load(json_file)
    for i in range (len(events)):
        if events[str(i)]['data']!= "":
            list_of_dbg_data.append([i,events[str(i)]['data']])
    print(
        tabulate(
            list_of_dbg_data,
            headers=[
                "index of debugging event",
                "data"],
            tablefmt="pretty"))
    return(list_of_dbg_data)


def min (filepath, *args):
    with open(filepath) as json_file:
        events=json.load(json_file)
    classs= args[0]
    
    if len(args)>=2:
        operation=args[1]
        for i in range(len(events)):
            if events[str(i)]["class_of_operation"]==classs and events[i]["operation"]==operation:
                print(i,events[i])
                break
    else:
        for i in range(len(events)):
            if events[str(i)]["class_of_operation"]==classs:
                print(i,events[str(i)])
                break


def max (filepath, *args):
    with open(filepath) as json_file:
        events=json.load(json_file)
    classs= args[0]
    
    if len(args)>=2:
        operation=args[1]
        for i in range(len(events)-1,0, -1):
            if events[str(i)]["class_of_operation"]==classs and events[i]["operation"]==operation:
                print(i,events[i])
                break
    else:
        for i in range(len(events)-1,0,-1):
            if events[str(i)]["class_of_operation"]==classs:
                print(i,events[str(i)])
                break
        


min('../events.json',12)
max('../events.json',8)

#occurence_of_event('../events.json',7)
#debugging_data('../events.json')