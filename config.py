#config.py
import os
import socket
import sys
from os import environ as env
import multiprocessing

PORT = int(env.get("PORT", 8091))
DEBUG_MODE = int(env.get("DEBUG_MODE", 1))
HOST='0.0.0.0'

#Gunicorn config
bind = ":" + str(PORT)
workers = multiprocessing.cpu_count() * 2 + 1
threads = 2 * multiprocessing.cpu_count()


def get_ip():
    """Get the server's IP address"""
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    return ip_address

server_ip = get_ip()
#client_ip = request.remote_addr