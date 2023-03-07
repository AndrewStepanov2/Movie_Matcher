import socket

# Returns the IP address of the computer that calls it as a string
# socket.gethostbyname(socket.gethostname()) doesn't work as it will return 127.0.1.1
def get_IP():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close()
    return ip