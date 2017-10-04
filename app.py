import os
from flask import Flask, redirect, url_for, request, render_template, jsonify
from pymongo import MongoClient
import pdb
from flask_cors import CORS, cross_origin
from bson.json_util import loads, dumps

app = Flask(__name__)
CORS(app)

# Set up database connection.
client = MongoClient("mongodb://admin:password@ds157873.mlab.com:57873/flask-test")
db = client['flask-test']


@app.route('/')
def todo():
    """ Retrieves the todo lists items """
    _items = db.todos.find()
    items = [item for item in _items]

    return dumps(items)


@app.route('/', methods=['POST'])
def new():
    """ Saves a new item to the todo list """
    request_json = request.get_json()
    item_doc = {'name': request_json['name'], 'description': request_json['description']}
    # Save items to database
    db.todos.insert_one(item_doc)

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
