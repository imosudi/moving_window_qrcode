from.graphQLquery import *

# ===========================================
# GRAPHQL MUTATIONS
# ===========================================
class QRCodePayload(graphene.ObjectType):
    qr_code_payload = graphene.String()
    expiry_time = graphene.Int()

class GenerateQRCode(graphene.Mutation):
    class Arguments:
        instructor_id = graphene.String(required=True)
        course_code = graphene.String(required=True)

    Output = QRCodePayload

    def mutate(self, info, instructor_id, course_code):
        """Fetch course details from the database and generate a secure QR code payload."""
        course = Course.query.filter_by(instructor_id=instructor_id, course_code=course_code).first()
        if not course:
            raise Exception("Course not found or unauthorized instructor.")

        current_time = get_current_server_time()
        window_start = (current_time // TIME_WINDOW_DURATION) * TIME_WINDOW_DURATION
        nonce = generate_random_nonce()

        # Check for nonce reuse (security)
        if is_nonce_used(nonce):
            raise Exception("Nonce already used. Possible replay attack detected.")

        payload = {
            "instructor_id": course.instructor_id,
            "course_code": course.course_code,
            "course_level": course.course_level,
            "lecture_start": course.lecture_start.isoformat(),
            "lecture_end": course.lecture_end.isoformat(),
            "window_start": window_start,
            "nonce": nonce
        }

        enc_payload = hmac_sha256(payload, SECRET_KEY)

        # Mark nonce as used
        mark_nonce_as_used(nonce)

        # Log event
        log_event("QR Generation", payload, enc_payload, current_time)

        return QRCodePayload(qr_code_payload=enc_payload, expiry_time=window_start + TIME_WINDOW_DURATION)

class Mutation(graphene.ObjectType):
    generate_qr_code = GenerateQRCode.Field()

#schema_mutation = graphene.Schema(query=Query, mutation=Mutation)

# noinspection PyTypeChecker
graphql_query = graphene.Schema(query=Query)
schema_mutation = graphene.Schema(query=Query, mutation=Mutation)


# ===========================================
# DIRECT GRAPHENE INTEGRATION (replacing Flask-GraphQL)
# ===========================================

# Helper function to process GraphQL requests
def process_graphql_request(schema):
    # Handle GET requests (for GraphiQL interface)
    if request.method == 'GET':
        # Simple GraphiQL interface
        graphiql_html = '''
        <!DOCTYPE html>
        <html>
        <head>
            <title>GraphiQL</title>
            <link href="https://cdnjs.cloudflare.com/ajax/libs/graphiql/1.0.6/graphiql.min.css" rel="stylesheet" />
            <script src="https://cdnjs.cloudflare.com/ajax/libs/react/16.13.1/umd/react.production.min.js"></script>
            <script src="https://cdnjs.cloudflare.com/ajax/libs/react-dom/16.13.1/umd/react-dom.production.min.js"></script>
            <script src="https://cdnjs.cloudflare.com/ajax/libs/graphiql/1.0.6/graphiql.min.js"></script>
            <script src="https://cdnjs.cloudflare.com/ajax/libs/fetch/3.0.0/fetch.min.js"></script>
            <style>
                body {
                    height: 100%;
                    margin: 0;
                    overflow: hidden;
                }
                #graphiql {
                    height: 100vh;
                }
            </style>
        </head>
        <body>
            <div id="graphiql">Loading...</div>
            <script>
                function fetchGQL(params) {
                    return fetch(window.location.href, {
                        method: 'post',
                        headers: {
                            'Accept': 'application/json',
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify(params),
                        credentials: 'include',
                    }).then(function (response) {
                        return response.text();
                    }).then(function (responseBody) {
                        try {
                            return JSON.parse(responseBody);
                        } catch (e) {
                            return responseBody;
                        }
                    });
                }
                
                ReactDOM.render(
                    React.createElement(GraphiQL, {fetcher: fetchGQL}),
                    document.getElementById('graphiql')
                );
            </script>
        </body>
        </html>
        '''
        return graphiql_html

    # Handle POST requests
    data = request.get_json()
    
    if not data:
        return jsonify({"errors": [{"message": "No GraphQL query provided"}]}), 400
    
    # Execute the GraphQL query
    result = schema.execute(
        data.get('query'),
        variable_values=data.get('variables'),
        operation_name=data.get('operationName')
    )
    
    # Format the response
    response = {}
    if result.errors:
        response["errors"] = [str(error) for error in result.errors]
    if result.data:
        response["data"] = result.data
    
    return jsonify(response)


