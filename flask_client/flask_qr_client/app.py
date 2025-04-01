
from flask import Flask, render_template, jsonify
import requests
import datetime

app = Flask(__name__)

GRAPHQL_ENDPOINT = "http://192.168.167.192:8091/graphql_mutation"


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
            return {
                "qrCodePayload": qr_data["qrCodePayload"],
                "expiryTime": qr_data["expiryTime"],  # Already formatted
                "instructorId": "INS123",
                "courseCode": "SEN312"
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
                instructor_id=qr_info["instructorId"],
                course_code=qr_info["courseCode"])
    return "Error fetching QR code", 500

@app.route("/get_qr_code")
def get_qr_code():
    qr_info = fetch_qr_code()
    return jsonify(qr_info if qr_info else {"error": "Failed to fetch QR Code"})

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5500)
