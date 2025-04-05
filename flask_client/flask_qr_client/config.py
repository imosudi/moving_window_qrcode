import socket , netifaces
from flask import request



def get_serving_ip():
    """Get the IP address through which Flask is serving requests"""
    # This function will be called when a request is received
    # to determine the actual IP being used
    host = request.host.split(':')[0]
    return host

def get_ip():
    """Get the server's IP address"""
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    return ip_address

def get_all_ips():
    """Get all IP addresses of the server"""
    ip_addresses = []
    
    # Get all network interfaces
    interfaces = netifaces.interfaces()
    
    for interface in interfaces:
        # Get the addresses for this interface
        addresses = netifaces.ifaddresses(interface)
        
        # Check if IPv4 addresses exist for this interface
        if netifaces.AF_INET in addresses:
            for address_info in addresses[netifaces.AF_INET]:
                ip = address_info['addr']
                # Skip loopback addresses
                if not ip.startswith('127.'):
                    ip_addresses.append({
                        'interface': interface,
                        'ip': ip
                    })
    
    return ip_addresses

ip_addresses = get_all_ips()

server_ip = get_ip()
#client_ip = request.remote_addr

serving_ip = get_serving_ip()