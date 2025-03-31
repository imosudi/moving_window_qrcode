from . import app
#from .mysqltojson import flatToCascadedJson
import os, json
from flask import jsonify




# Flask Rest & Graphql Routes
@app.route('/')
def hello_world():
   
    return jsonify("dummy")
