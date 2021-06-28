import flask
from flask import request, jsonify
import json

app = flask.Flask(__name__)
app.config["DEBUG"] = True


# Create some test data for our catalog in the form of a list of dictionaries.

@app.route('/', methods=['GET'])
def home():
    return '''<h1>Distant Reading Archive</h1>
<p>A prototype API for distant reading of science fiction novels.</p>'''

# A route to return all of the available entries in our catalog.
@app.route('/events/all', methods=['GET'])
def api_all():
    with open('../events.json') as json_file:
        events=json.load(json_file)
    return (events)


@app.route('/events', methods=['GET'])
def api_id():
    with open('../events.json') as json_file:
        events=json.load(json_file)
    # Check if an ID was provided as part of the URL.
    # If ID is provided, assign it to a variable.
    # If no ID is provided, display an error in the browser.
    if 'id' in request.args:
        wanted_class = int(request.args['id'])
    else:
        return "Error: No id field provided. Please specify an id."

    # Create an empty list for our results
    results = []

    # Loop through the data and match results that fit the requested ID.
    # IDs are unique, but other fields might return many results
    
    for i in range (len(events)):
      #print (len(events))
        if (events[str(i)]['class_of_operation']) == wanted_class:
            list.append(events[str(i)])

    # Use the jsonify function from Flask to convert our list of
    # Python dictionaries to the JSON format.
    return (list)

app.run()

def draft_function():
    with open('./events.json') as json_file:
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
  