import os
from flask import Flask, redirect, url_for, request, render_template, jsonify
import pdb
from flask_cors import CORS, cross_origin
from bson.json_util import loads, dumps
import pyrebase

app = Flask(__name__)
CORS(app)

# Set up database connection.
config = {
    'apiKey': "AIzaSyDpFoAzfFzzcCmYkMwkAz61wUY_O5z9KM4", 
    'authDomain': "cloudide-3d6ca.firebaseapp.com", 
    'databaseURL': "https://cloudide-3d6ca.firebaseio.com", 
    'projectId': "cloudide-3d6ca", 
    'storageBucket': "cloudide-3d6ca.appspot.com", 
    'messagingSenderId': "42881595105"
}
firebase = pyrebase.initialize_app(config)

# Set up the user
auth = firebase.auth()
user = auth.sign_in_with_email_and_password('williampshiel@gmail.com', 'password')

# Get refrence to db
db = firebase.database()
# db = client['flask-test']


@app.route('/')
def todo():
    """ Retrieves the todo lists items """
    todos = db.child('todos').get(user['idToken']).val()

    return None

@app.route('/', methods=['POST'])
def new():
    """ Saves a new item to the todo list """
    request_json = request.get_json()
    todo_wrapper = {} 
    todo = {'name': request_json['name'], 'description': request_json['description']}
    todo_wrapper['todo'] = todo 

    # Save item to database
    db.child("todos").push(todo_wrapper, user['idToken'])

    return redirect(url_for('todo'))


@app.route('/filter', methods=['GET'])
def filter_items():
    """ filters the todo list by inputted text. """
    item_filter = request.args.get('name')

    # Filter items by the selected text
    filtered_items = db.todos.find({ 'name': item_filter })

    return dumps(filtered_items)


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
