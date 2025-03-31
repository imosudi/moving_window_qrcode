

import os, json, hmac, hashlib, time
from flask import jsonify, request

from app.models import Role, User, Attendance, Nonce, Course
from app import app, db

# ===========================================
# CONFIGURATION
# ===========================================
SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkey")
TIME_WINDOW_DURATION = 300  # 5 minutes
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

def is_nonce_used(nonce):
    return db.session.query(Nonce).filter_by(nonce=nonce).first() is not None

def mark_nonce_as_used(nonce):
    new_nonce = Nonce(nonce=nonce, timestamp=get_current_server_time())
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
