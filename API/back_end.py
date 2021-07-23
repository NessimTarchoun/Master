import sys
import os
import json
from flask import app
import numpy as np

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),os.path.pardir)))
from event_parser.parsers import *

from os import environ, error

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
    
    if operation== None:
        count=0    
        for i in range (len(target_list_of_events)):
            if target_list_of_events[i]["class_of_operation"]== classs:
                count+=1
        #print ("wanted class",classs,"percentage:",count,'/',len(target_list_of_events) ,'==', round (count/len(target_list_of_events),2))
    else:
        count=0    
        for i in range (len(target_list_of_events)):
            if target_list_of_events[i]["class_of_operation"]== classs and target_list_of_events[i]["operation"]==operation:
                count+=1
        #print ("wanted class and ops",classs, operation, "percentage:",count,'/',len(target_list_of_events) ,'==', round (count/len(target_list_of_events),2))
    #return(tabulate(target_list_of_events,tablefmt="pretty"))
    print(target_list_of_events)
    #return(target_list_of_events, round(100*count/len(target_list_of_events),4),count)

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

def decode_JSON_events(jsonfilename):
    event=[]
    events_decoded=[]
    with open(jsonfilename) as json_file:
        events=json.load(json_file)
    for i in range(len(events)):
        event.append (Event(events[str(i)]["class_of_operation"],
                            events[str(i)]["operation"],
                            events[str(i)]["timestamp"],
                            events[str(i)]["data"]))
    for i in range(len(event)):
        events_decoded.append((type_of_operation(event[i])[0],
                            type_of_operation(event[i])[1],
                            event[i].t,
                            event[i].data))
    
    return(events_decoded)

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
            
def api_searching_by_id(wanted_class=None, timestamp1=None, timestamp2=None):
    with open('../events.json') as json_file:
        events=json.load(json_file)
    
    if wanted_class!=None and timestamp1!=None and timestamp2!=None :
        common_list=[]
        for i in range (len(events)):
            if ((events[str(i)]['timestamp']) >= timestamp1) and ((events[str(i)]['timestamp']) <= timestamp2) and ((events[str(i)]['class_of_operation']) == wanted_class):
                e=Event(events[str(i)]["class_of_operation"],
                            events[str(i)]["operation"],
                            events[str(i)]["timestamp"],
                            events[str(i)]["data"])
                common_list.append((type_of_operation(e)[0],
                            type_of_operation(e)[1],
                            e.t,
                            e.data))
        return (common_list)
    
    if wanted_class!=None and timestamp1==None and timestamp2==None :
        
        id_list=[]
        for i in range (len(events)):
            if (events[str(i)]['class_of_operation']) == wanted_class:
                e=Event(events[str(i)]["class_of_operation"],
                            events[str(i)]["operation"],
                            events[str(i)]["timestamp"],
                            events[str(i)]["data"])
                id_list.append((type_of_operation(e)[0],
                            type_of_operation(e)[1],
                            e.t,
                            e.data))
        return (id_list)
    
    if timestamp2!=None and timestamp1!=None:
    #elif 'ts1' in request.args and 'ts2' in request.args:
        ts_list=[]
        for i in range (len(events)):
            if ((events[str(i)]['timestamp']) >= timestamp1) and((events[str(i)]['timestamp']) <= timestamp2) :
                e=Event(events[str(i)]["class_of_operation"],
                            events[str(i)]["operation"],
                            events[str(i)]["timestamp"],
                            events[str(i)]["data"])
                ts_list.append((type_of_operation(e)[0],
                            type_of_operation(e)[1],
                            e.t,
                            e.data))
        return (ts_list)

    else:
        return (decode_JSON_events('../events.json'))

def percentage_of_class(class_searched=None, t1=None, t2=None):
    events=api_searching_by_id(wanted_class=class_searched, timestamp1=t1, timestamp2=t2)
    list_of_classs=(initialise_list_of_events('../events_config.json'))
    classs=[]
    appearance={}
    percentages={}
    
    for i in list_of_classs['main_classes']:
        classs.append((i,list_of_classs[str(i)]['designation'] ))
  
    for j in range( len(classs)):
        appearance[classs[j][1]]=0

    for i in range(len(events)):
        if events[i][0]!='undefined type of event':
            appearance[events[i][0]]=appearance[events[i][0]] + 1
        
    
    appearance["Costumer events"]=len(events)-sum(appearance.values())

    for i in appearance.keys():
        percentages[i]=round(appearance[i]/len(events)*100,2)

    return(percentages)
#print(percentage_of_class(t1=1,t2=2100000000000000))
#min('../events.json',12)
#max('../events.json',8)
#print (occurence_of_classes('../events.json', '../events_config.json', ts1=0, ts2=1943829632470))
#print(occurence_of_event('../events.json',classs=10,ts1=0, ts2=1943829632470))
#debugging_data('../events.json')