"""
Workaround import error
pip install graphql-core==2.2.1
pip install graphene==2.1.8
"""
import os

#import graphene
from flask import Flask, config
from flask_graphql import GraphQLView
from flask_sqlalchemy import SQLAlchemy
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField

import config
from .dbconnect import *

from flask_migrate import Migrate
from flask_cors import CORS


app = Flask(__name__)



#print(dbhost, dbname, dbuser, pw)

# Database configuration for mysql
app.config['SECRET_KEY'] = 'verydifficult-cashubposweb-secret-key-goes-here'
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://{dbuser}:{pw}@{dbhost}/{dbname}" .format(dbuser=dbuser, pw=pw, dbhost=dbhost, dbname=dbname)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# Initialize Database
db = SQLAlchemy(app)
#db.init_app(app)

migrate = Migrate(app, db)
CORS(app)

from .models import *
from api.graphQLSchema import *
from api.graphQLmutation import *


from .routes import *

