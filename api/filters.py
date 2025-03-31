#filter.py
from graphene_sqlalchemy_filter import FilterSet
 
from app.models import *

 
ALL_OPERATIONS = ['eq', 'ne', 'like', 'ilike', 'is_null', 'in', 'not_in', 'lt', 'lte', 'gt', 'gte', 'range']

           
    