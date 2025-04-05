## gunicorn -c config.py --reload --preload app:app
from app import app
import config

"""
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=config.PORT, debug=config.DEBUG_MODE)
"""

if __name__ == '__main__':
    app.run(debug=config.DEBUG_MODE, host=config.HOST, port=config.PORT, ssl_context=('/home/mosud/Documents/dev/moving_window_qrcode/flask_client/flask_qr_client/ssl_cert/cert.pem', '/home/mosud/Documents/dev/moving_window_qrcode/flask_client/flask_qr_client/ssl_cert/key.pem'))


