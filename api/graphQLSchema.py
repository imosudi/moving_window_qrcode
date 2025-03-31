
#graphQLSchema.py

from app import app
from .graphQLmutation import *
#from flask_graphql import GraphQLView



# /graphql-query
# /graphql-query
@app.route('/graphql_query', methods=['GET', 'POST'])
def graphql_query():
    return process_graphql_request(schema_query)

"""app.add_url_rule("/graphql-query", view_func=GraphQLView.as_view(
    "graphql-query",
    schema=schema_query,
    graphiql=True
))
"""
# /graphql-mutation
@app.route('/graphql_mutation', methods=['GET', 'POST'])
def graphql_mutation():
    return process_graphql_request(schema_mutation)


"""app.add_url_rule("/graphql-mutation", view_func=GraphQLView.as_view(
    "graphql-mutation",
    schema=schema_mutation,
    graphiql=True
))
"""
"""
# ===========================================
# GRAPHQL ENDPOINT
# ===========================================
app.add_url_rule("/graphql", view_func=GraphQLView.as_view(
    "graphql",
    schema=schema_mutation,
    graphiql=True
))
"""