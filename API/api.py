import flask
from flask import request, jsonify
import json

app = flask.Flask(__name__)
app.config["DEBUG"] = True



@app.route('/', methods=['GET'])
def home():
    return '''<h1>Event log API</h1>'''

# A route to return all of the available entries in our catalog.
@app.route('/events/all', methods=['GET'])
def api_all():
    with open('events.json') as json_file:
        extracted_events=json.load(json_file)
    return (extracted_events)


@app.route('/events', methods=['GET'])
def api_id():
    li_st=[]
    with open('events.json') as json_file:
        events=json.load(json_file)

    if 'id' in request.args:
        wanted_class = int(request.args['id'])
    else:
        return "Error: No id field provided. Please specify an id."

    for i in range (len(events)):
        if (events[str(i)]['class_of_operation']) == wanted_class:
            li_st.append(events[str(i)])
    list_json= json.dumps(li_st)
    return (list_json)

app.run()

def draft_function():
    with open('events.json') as json_file:
        events=json.load(json_file)
    #print(events)
    list=[]
    wanted_class= 10
    for i in range (len(events)):
          #print (len(events))
        if (events[str(i)]['class_of_operation']) == wanted_class:
            list.append(events[str(i)])

    # Use the jsonify function from Flask to convert our list of
    # Python dictionaries to the JSON format.
    print (list)
      #print events[i]

api_all()  