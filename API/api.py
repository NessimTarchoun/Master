import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),os.path.pardir)))
import flask
from flask import request, render_template
import json
from API.back_end import *
app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.route('/', methods=['GET'])
def home():
    return(render_template("./index.html"))

def Data_in_table(*args):
    if len (args)==0:
        list_of_events=decode_JSON_events('../events.json')
    else:
        list_of_events=args[0]
    return render_template('./data_table.html', events=list_of_events)


@app.route('/events', methods=['GET'])
def api_searching_by_id():
    with open('../events.json') as json_file:
        events=json.load(json_file)

    if 'ts1' in request.args and 'ts2' in request.args and 'id' in request.args:
        timestamp1 = int(request.args['ts1'])
        timestamp2 = int(request.args['ts2'])
        wanted_class = int(request.args['id'])
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
        return render_template('./data_table.html', events=common_list)
    
    if 'id' in request.args:
        wanted_class = int(request.args['id'])
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
        return render_template('./data_table.html', events=id_list)
    
    elif 'ts1' in request.args and 'ts2' in request.args:
        timestamp1 = int(request.args['ts1'])
        timestamp2 = int(request.args['ts2'])
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
        return render_template('./data_table.html', events=ts_list)


    else:
        return render_template('./data_table.html', events=decode_JSON_events('../events.json'))


@app.route('/pie')
def pie():
    Data= (occurence_of_classes('../events.json', '../events_config.json', ts1=None, ts2=None))
    labels=[Data[i]['classs'] for i in range (len(Data))]
    values=[Data[i]['percentage'] for i in range (len(Data))]
    colors = ["#F7464A", "#46BFBD", "#FDB45C", "#FEDCBA","#ABCDEF", "#DDDDDD", "#ABCABC", "#4169E1","#C71585", "#FF4500", "#FEDCBA", "#46BFBD"]
    return render_template('./pie_chart.html', title='Occurence of Classes', max=17000, set=zip(values, labels, colors[:len(values)]))

@app.route('/bar')
def bar():
    Data= (occurence_of_classes('../events.json', '../events_config.json', ts1=None, ts2=None))
    labels=[Data[i]['classs'] for i in range (len(Data))]

    values=[Data[i]['percentage'] for i in range (len(Data))]
    return render_template('./bar_chart.html', title='Occurence of Classes', max=60, labels=labels, values=values)


@app.route('/line')
def linechart():
    with open('../events.json') as json_file:
        events=json.load(json_file)
    line_labels=[i+1 for i in range (50)]
    line_values=[events[str(i)]['timestamp'] for i in range (50)]
    return render_template('./line_chart.html', title='timestamp evolution', max= line_values[-1] ,labels=line_labels, values=line_values)


@app.route('/welcome_page')
def welcome_page():

    #-----------pie chart parametrs---------------------------
    pie_Data= (occurence_of_classes('../events.json', '../events_config.json', ts1=None, ts2=None))
    pie_labels=[pie_Data[i]['classs'] for i in range (len(pie_Data))]
    pie_values=[pie_Data[i]['percentage'] for i in range (len(pie_Data))]
    pie_colors = ["#F7464A", "#46BFBD", "#FDB45C", "#FEDCBA","#ABCDEF", "#DDDDDD", "#ABCABC", "#4169E1","#C71585", "#FF4500", "#FEDCBA", "#46BFBD"]
    
    #-----------bar chart parametrs----------------------

    Data= (occurence_of_classes('../events.json', '../events_config.json', ts1=None, ts2=None))
    bar_labels=[Data[i]['classs'] for i in range (len(Data))]
    bar_values=[Data[i]['percentage'] for i in range (len(Data))]
    
    #-------------- line chart parametrs------------------------
    with open('../events.json') as json_file:
        events=json.load(json_file)
    line_labels=[i+1 for i in range (50)]
    line_values=[events[str(i)]['timestamp'] for i in range (50)]
    #return render_template('./welcome_page.html', max= line_values[-1] ,labels=line_labels, values=line_values)

    # return render_template('./welcome_page.html', set=zip(pie_values, pie_labels, pie_colors[:len(pie_values)]), line_max= line_values[-1] ,line_labels=line_labels, line_values=line_values, bar_labels=bar_labels, bar_values=bar_values)

    return render_template('./welcome_page.html',set=zip(pie_values, pie_labels, pie_colors[:len(pie_values)]), 
    line_max= line_values[-1] ,line_labels=line_labels, line_values=line_values, bar_labels=bar_labels, 
    bar_values=bar_values, events=decode_JSON_events('../events.json'))
    
   # return render_template('./welcome_page.html', title='Occurence of Classes', line_max=17000, set=zip(pie_values, pie_labels, pie_colors[:len(pie_values)]))



@app.route('/visualization')
def visualization():
    return(render_template('./vis.html',title='fgrefd'))
    
app.run()