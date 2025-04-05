

import os, json, hmac, hashlib, time
import ast
from flask import jsonify, request

from app.models import Role, User, Attendance, Nonce, Course
from app import app, db

# ===========================================
# CONFIGURATION
# ===========================================
SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkey")
TIME_WINDOW_DURATION = 120  # 5 minutes
CLOCK_TOLERANCE = 30  # Balanced approach: 30 seconds tolerance
NONCE_LENGTH = 16  # Secure nonce length

# ===========================================
# HELPER FUNCTIONS
# ===========================================
def get_current_server_time():
    return int(time.time())

def generate_random_nonce():
    return os.urandom(NONCE_LENGTH).hex()

def hmac_sha256(payload, secret_key):
    json_payload = json.dumps(payload, sort_keys=True).encode()
    return hmac.new(secret_key.encode(), json_payload, hashlib.sha256).hexdigest()

def decrypt_hmac(encrypted_payload, original_payload, secret_key=SECRET_KEY):
    try:
        # Recompute the HMAC using the original payload
        computed_hmac = hmac_sha256(original_payload, secret_key)

        # Verify HMAC to ensure integrity
        if not hmac.compare_digest(computed_hmac, encrypted_payload):
            raise ValueError("HMAC verification failed. Payload might be tampered with.")

        return original_payload  # Return the original payload if verification is successful

    except Exception as e:
        print(f"Decryption error: {e}")
        return None  # Return None if verification fails

def validate_attendance(encrypted_payload, student_id):
    # 1. Assume student authentication is already verified by middleware.
    print("\n\n", "validate_attendance funtion", "\n\n")
    print(encrypted_payload, student_id)
    encrypted_payload_andpayload = encrypted_payload
    encrypted_payload = encrypted_payload_andpayload.split(" | ")[0]
    print("encrypted_payload: ", encrypted_payload); #time.sleep(300)
    
    payload_str = encrypted_payload_andpayload.split(" | ")[1]
    print("payload_str: ", payload_str, type(payload_str))

    payload_dict  = ast.literal_eval(payload_str)
    print("payload_dict: ", payload_dict, type(payload_dict))
    # 2. Decrypt or verify the encrypted payload.
    print(encrypted_payload, "\n", SECRET_KEY); #time.sleep(300)
    
    payload = decrypt_hmac(encrypted_payload, payload_dict, SECRET_KEY)
    print("payload: ", payload); #time.sleep(300)
    if payload is None:
        return {"status": "ERROR", "message": "Invalid or tampered QR code."}

    # 3. Check that the QR code is still within the valid moving window.
    t_current = get_current_server_time()
    if t_current < (payload["window_start"] - CLOCK_TOLERANCE) or \
       t_current > (payload["window_start"] + TIME_WINDOW_DURATION + CLOCK_TOLERANCE):
        return {"status": "ERROR", "message": "QR code expired."}

    # 4. Prevent replay attacks by ensuring the nonce hasn't been used.
    if is_nonce_used(payload["nonce"]):
        return {"status": "ERROR", "message": "This QR code has already been used."}

    # 5. Mark the nonce as used to block any replay.
    mark_nonce_as_used(payload["nonce"])
    

    # 6. Record the attendance in the system.
    record_attendance(student_id, t_current, payload)

    # 7. Log the validation event for future auditing.
    log_event("Attendance Validation", {
        "student_id": student_id,
        "payload": payload,
        "timestamp": t_current
    })

    return {"status": "SUCCESS", "message": "Attendance recorded."}

def is_nonce_used(nonce):
    return db.session.query(Nonce).filter_by(nonce=nonce).first() is not None

def mark_nonce_as_used(nonce):
    new_nonce = Nonce(nonce=nonce, timestamp=get_current_server_time())
    #new_nonce = Nonce(nonce=nonce, timestamp=get_current_server_time().isoformat())
    db.session.add(new_nonce)
    db.session.commit()

def record_attendance(student_id, timestamp, payload):
    new_attendance = Attendance(student_id=student_id, timestamp=timestamp, payload=json.dumps(payload))
    db.session.add(new_attendance)
    db.session.commit()

def log_event(event_type, details, optional_enc_payload=None, optional_timestamp=None):
    print({
        "event_type": event_type,
        "details": details,
        "encrypted_payload": optional_enc_payload,
        "timestamp": optional_timestamp or get_current_server_time()
    })


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


