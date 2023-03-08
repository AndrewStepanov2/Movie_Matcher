import socket
import threading

# Returns the IP address of the computer that calls it as a string
# socket.gethostbyname(socket.gethostname()) doesn't work as it will return 127.0.1.1
# The function sets up a UDP connection with Google Public DNS
def get_IP():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close()
    return ip

# Sets up a socket for the host
# Starts a thread for accepting clients
def start_hosting(variables_for_user_link):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((get_IP(), 42424))
    server.settimeout(0.2)
    server.listen()
    variables_for_user_link.append([])
    variables_for_user_link.append([])
    variables_for_user_link.append([])
    thread = threading.Thread(target=host_accept_client, args=(server, variables_for_user_link))
    thread.start()
    return (server, thread)

# Function for a thread for the host to accept clients
# Starts a thread for each client
def host_accept_client(server, variables_for_user_link):
    clientID = 0
    while variables_for_user_link[0]:
        try:
            client, address = server.accept()
            variables_for_user_link[1].append(client)
            variables_for_user_link[2].append(True)
            thread = threading.Thread(target=host_serve_client, args=((client, clientID, variables_for_user_link)))
            thread.start()
            variables_for_user_link[3].append(thread)
            clientID += 1
        except socket.timeout:
            pass
    server.settimeout(None)

# Function to be used by the host
# Function for the threads for each client to run
# For right now, it does nothing interesting
def host_serve_client(client, clientID, variables_for_user_link) :
    while variables_for_user_link[2][clientID]:
        to_send = input("")
        client.send(to_send.encode("ascii"))
        to_recv = client.recv(1024).decode("ascii")
        print(to_recv)
        if to_send == "quit":
            break
    host_server_shutdown(variables_for_user_link)


# Function for closing the socket the host is using
# Terminates the threads for each client before closing the host's socket
def host_server_shutdown(variables_for_user_link):
    for i in range(len(variables_for_user_link[2])):
        variables_for_user_link[2][i] = False
        variables_for_user_link[3][i].join()
    variables_for_user_link[4].close()

# Sets up a socket for the client
# Starts a thread for the connection to the host
def client_join_server(host_IP, variables_for_user_link):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host_IP, 42424))
    thread = threading.Thread(target=client_get_served, args=(client, variables_for_user_link))
    thread.start()
    return(client, thread)

# Function to be used by the client
# Handles the connection to the host
# For right now, it does nothing interesting
def client_get_served(client, variables_for_user_link):
    while variables_for_user_link[0]:
        to_recv = client.recv(1024).decode("ascii")
        print(to_recv)
        to_send = input("")
        client.send(to_send.encode("ascii"))
        if to_send == "quit":
            break
    client_shutdown(variables_for_user_link)

# Function for closing the socket the client is using
# Terminates the thread handling the connection to the host before closing the client's socket
def client_shutdown(variables_for_user_link):
    variables_for_user_link[0] = False
    variables_for_user_link[2].join()
    variables_for_user_link[1].close()