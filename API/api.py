import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),os.path.pardir)))
import flask
from flask import request
import json

app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.route('/', methods=['GET'])
def home():
    return '''<h1>Event log API</h1>'''

@app.route('/events/', methods=['GET'])
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
                common_list.append(events[str(i)])
        return (json.dumps(common_list))
    
    if 'id' in request.args:
        wanted_class = int(request.args['id'])
        id_list=[]
        for i in range (len(events)):
            if (events[str(i)]['class_of_operation']) == wanted_class:
                id_list.append(events[str(i)])
        return(json.dumps(id_list))
    
    elif 'ts1' in request.args and 'ts2' in request.args:
        timestamp1 = int(request.args['ts1'])
        timestamp2 = int(request.args['ts2'])
        ts_list=[]
        for i in range (len(events)):
            if ((events[str(i)]['timestamp']) >= timestamp1) and((events[str(i)]['timestamp']) <= timestamp2) :
                ts_list.append(events[str(i)])
        return(json.dumps(ts_list))

    else:
        return (json.dumps(events))

app.run()