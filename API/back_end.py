import sys
import os
import json
import numpy as np

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),os.path.pardir)))
from event_parser.parsers import *

from os import environ

def suppress_qt_warnings():
    environ["QT_DEVICE_PIXEL_RATIO"] = "0"
    environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    environ["QT_SCREEN_SCALE_FACTORS"] = "1"
    environ["QT_SCALE_FACTOR"] = "1"


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


def occurence_of_event(filename, classs=None, operation=None, ts1=None, ts2=None):
    from tabulate import tabulate 
    suppress_qt_warnings()
    with open(filename) as json_file:
        events=json.load(json_file)
    
    if ts1==None or ts2==None:
        target_list_of_events=[events[str(i)] for i in range (len(events))]
    else:
        target_list_of_events=[events[str(i)] for i in range (len(events))if ((events[str(i)]['timestamp']) >= ts1) and ((events[str(i)]['timestamp']) <= ts2)]
    count=0    
    if operation== None:
        for i in range (len(target_list_of_events)):
            if target_list_of_events[i]["class_of_operation"]== classs:
                count+=1
        #print ("wanted class",classs,"percentage:",count,'/',len(target_list_of_events) ,'==', round (count/len(target_list_of_events),2))
    else:
        for i in range (len(target_list_of_events)):
            if target_list_of_events[i]["class_of_operation"]== classs and target_list_of_events[i]["operation"]==operation:
                count+=1
        #print ("wanted class and ops",classs, operation, "percentage:",count,'/',len(target_list_of_events) ,'==', round (count/len(target_list_of_events),2))
    #return(tabulate(target_list_of_events,tablefmt="pretty"))
    
    return(round(count/len(target_list_of_events),4))

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



            
def occurence_of_classes(filename, events_config_file, ts1=None, ts2=None):
    import matplotlib.pyplot as plt
    list_of_classs=(initialise_list_of_events('../events_config.json'))
    classs=[]
    p=[]
    
    for i in list_of_classs['main_classes']:
        classs.append(list_of_classs[str(i)]['designation'] )
        p.append(occurence_of_event(filename, i,ts1,ts2))

    classs.append("costumer events")
    p.append(1 - sum (p))
    percentages=[{"classs":classs[i],"percentage":round(p[i]*100,2)} for i in range(len(p))]
    plt.figure(figsize=(20 , 10))
    plt.pie(p, labels = classs,pctdistance = 0.7, autopct = lambda p: str(round(p,2)) + '%',)
    plt.legend(loc="upper right", title= "Classes of events", bbox_to_anchor=(1, 0, 0.5, 1))

    #plt.show() 
    return (percentages)


#min('../events.json',12)
#max('../events.json',8)
#print (occurence_of_classes('../events.json', '../events_config.json', ts1=None, ts2=None))
#print(occurence_of_event('../events.json',classs=10,ts1=0, ts2=1000001273188791))
#debugging_data('../events.json')