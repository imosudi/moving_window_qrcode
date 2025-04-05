
from flask import Flask, render_template, jsonify, request
import requests, datetime, qrcode
import io
import base64
import time
from flask_cors import CORS  # Import CORS


app = Flask(__name__)

#CORS(app)  # Enable CORS globally


# Mock Database (In-memory storage for simplicity)
instructor_qr_codes = {}

# GraphQL Endpoint (Replace with your actual API URL)
GRAPHQL_API_URL = "http://192.168.55.192:8091/graphql_mutation"
GRAPHQL_ENDPOINT = "http://127.0.0.1:8091/graphql_mutation"


# Custom filter to convert Unix timestamp to HH:MM:SS
def timestamp_to_time(value):
    return datetime.datetime.fromtimestamp(value).strftime('%H:%M:%S')

app.jinja_env.filters['timestamp_to_time'] = timestamp_to_time  # Register filter

def fetch_qr_code():
    query = {
        "query": '''
            mutation {
                generateQrCode(instructorId: "INS123", courseCode: "SEN312") {
                    qrCodePayload
                    expiryTime
                    payload{
                        ... on MessageField{
                            instructorId
                            courseCode
                            courseLevel
                            lectureStart
                            lectureEnd
                            windowStart
                            nonce
                        }
                    }
                }
            }
        '''
    }
    try:
        response = requests.post(GRAPHQL_ENDPOINT, json=query)
        response.raise_for_status()
        data = response.json()
        
        if "data" in data and "generateQrCode" in data["data"]:
            qr_data = data["data"]["generateQrCode"]
            #qr_data["expiryTime"] = timestamp_to_time(qr_data["expiryTime"]),
            print("qr_data: ", qr_data); #time.sleep(300)
            return {
                "qrCodePayload": qr_data["qrCodePayload"],
                "expiryTime": qr_data["expiryTime"],  
                "payload": qr_data["payload"],
                "instructorId": qr_data["payload"]["instructorId"], #"INS123",
                "courseCode": qr_data["payload"]["courseCode"], #"SEN312"
            }

    except requests.RequestException as e:
        print(f"Error fetching QR Code: {e}")

    return None


@app.route("/")
def index():
    qr_info = fetch_qr_code()
    if qr_info:
        return render_template("index.html", 
                qr_code_payload=qr_info["qrCodePayload"], 
               expiry_time=qr_info["expiryTime"],
               payload=qr_info["payload"],
                instructor_id=qr_info["instructorId"],
                course_code=qr_info["courseCode"])
    return "Error fetching QR code", 500

@app.route("/get_qr_code")
def get_qr_code():
    qr_info = fetch_qr_code()
    return jsonify(qr_info if qr_info else {"error": "Failed to fetch QR Code"})


@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/instructor')
def instructor_page():
    instructor_id   = 'INS123'
    course_code     = 'SEN312'
    return render_template('instructor.html', instructor_id=instructor_id, course_code=course_code)

@app.route('/student')
def student_page():
    return render_template('student.html')

@app.route('/generate_qr', methods=['POST'])
def generate_qr():
    data = request.json
    instructor_id = data.get("instructor_id")
    course_code = data.get("course_code")
    expiry_time = int(time.time()) + 60  # QR Code valid for 60 seconds
    
    qr_payload = f"{instructor_id}:{course_code}:{expiry_time}"
    instructor_qr_codes[instructor_id] = {'qr_code': qr_payload, 'expiry': expiry_time}
    
    qr = qrcode.make(qr_payload)
    buf = io.BytesIO()
    qr.save(buf, format="PNG")
    qr_base64 = base64.b64encode(buf.getvalue()).decode("utf-8")
    
    return jsonify({"qr_code": qr_base64, "expiry": expiry_time})

@app.route('/submit_attendance', methods=['POST'])
def submit_attendance():
    data = request.json
    scanned_payload = data.get("scanned_payload")
    student_id = data.get("student_id")
    print("scanned_payload: ", scanned_payload, "\n", "student_id: ", student_id); time.sleep(300)
    try:
        response = requests.post(GRAPHQL_API_URL, json={
            "query": f"""
            mutation {{
                validateAttendance(encrypted_payload: "{scanned_payload}", student_id: "{student_id}") {{
                    status
                    error_message
                }}
            }}
            """
        })
        result = response.json()
        return jsonify(result.get("data", {}).get("validateAttendance", {}))
    except Exception as e:
        return jsonify({"status": "ERROR", "error_message": str(e)})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5500, ssl_context=('./ssl_cert/cert.pem', './ssl_cert/key.pem'))

