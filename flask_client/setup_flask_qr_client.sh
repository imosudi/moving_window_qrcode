#!/bin/bash

# Define project name
PROJECT_NAME="flask_qr_client"

# Create project structure
echo "Creating project structure..."
mkdir -p $PROJECT_NAME/static
mkdir -p $PROJECT_NAME/templates

# Create Python Flask application files
touch $PROJECT_NAME/app.py
touch $PROJECT_NAME/requirements.txt

# Create static files
touch $PROJECT_NAME/static/styles.css
touch $PROJECT_NAME/static/script.js

# Create HTML template
touch $PROJECT_NAME/templates/index.html

# Add boilerplate content to files
echo "Adding boilerplate content..."

# app.py content
cat <<EOF > $PROJECT_NAME/app.py
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
            return {
                "qrCodePayload": qr_data["qrCodePayload"],
                "expiryTime": qr_data["expiryTime"],
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

EOF

# requirements.txt content
#echo "flask requests qrcode[pil]" > $PROJECT_NAME/requirements.txt
cat <<EOF > $PROJECT_NAME/requirements.txt
flask 
requests 
qrcode[pil]
EOF

# index.html content
cat <<EOF > $PROJECT_NAME/templates/index.html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Instructor QR Code</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='styles.css') }}">
    <script src="{{ url_for('static', filename='script.js') }}" defer></script>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
    <div class="container d-flex justify-content-center align-items-center vh-100">
        <div class="card shadow p-4 text-center">
            <h4 class="mb-3">QR Code for <span id="courseCode">{{ course_code }}</span></h4>
            <p class="text-muted">Instructor ID: <strong id="instructorId">{{ instructor_id }}</strong></p>
            <p><strong>QR Code Payload:</strong> <span id="qrPayload">{{ qr_code_payload }}</span></p>
            <p class="text-danger">Expires at: <span id="expiryTime">{{ expiry_time | timestamp_to_time }}</span></p>
            <img id="qrCodeImage" class="mb-3" src="https://api.qrserver.com/v1/create-qr-code/?size=200x200&data={{ qr_code_payload }}" alt="QR Code">
           
        </div>
    </div>

    <script>
        function formatTimestamp(timestamp) {
            const date = new Date(timestamp * 1000);
            return date.toLocaleTimeString('en-GB', { hour12: false });
        }
        document.addEventListener("DOMContentLoaded", function () {
            const expirySpan = document.getElementById("expiryTime");
            expirySpan.textContent = formatTimestamp(parseInt(expirySpan.textContent, 10));
        });
    </script>
</body>
</html>

EOF

# script.js content
cat <<EOF > $PROJECT_NAME/static/script.js
function fetchQRCode() {
    fetch("/get_qr_code")
        .then(response => response.json())
        .then(data => {
            if (data.qrCodePayload) {
                document.getElementById("qrPayload").innerText = data.qrCodePayload;
                document.getElementById("qrCodeImage").src = \`https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=\${data.qrCodePayload}\`;
                document.getElementById("expiryTime").innerText = data.expiryTime;

                // Schedule next fetch
                let refreshTime = (data.expiryTime * 1000) - Date.now();
                setTimeout(fetchQRCode, Math.max(refreshTime, 1000));
            }
        })
        .catch(error => console.error("Error fetching QR Code:", error));
}

// Initial fetch
fetchQRCode();
EOF

# styles.css content
cat <<EOF > $PROJECT_NAME/static/styles.css
body {
    font-family: Arial, sans-serif;
    text-align: center;
    margin-top: 20px;
}
.container {
    max-width: 400px;
    margin: auto;
    padding: 20px;
    border: 1px solid #ccc;
    border-radius: 10px;
    box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1);
}
img {
    margin: 10px 0;
}
EOF

echo "Project setup complete!"
echo "Navigate to '$PROJECT_NAME' and run:"
echo "  python3 -m venv venv && source venv/bin/activate"
echo "  pip install -r requirements.txt"
echo "  python app.py"
