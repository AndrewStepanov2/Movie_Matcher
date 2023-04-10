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
    variables_for_user_link.append([]) # for storing the clients that join the server run by the host
    variables_for_user_link.append([]) # for storing boolean values that we can change to stop the threads that handle the clients
    variables_for_user_link.append([]) # for storing the movie title and vote of a client
    variables_for_user_link.append([]) # for storing a boolean value to indicate if a client has voted or not
    variables_for_user_link.append([]) # for storing the threads that handles the clients
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
            variables_for_user_link[3].append("")
            variables_for_user_link[4].append(False)
            thread = threading.Thread(target=host_serve_client, args=((client, clientID, variables_for_user_link)))
            thread.start()
            variables_for_user_link[5].append(thread)
            clientID += 1
        except socket.timeout:
            pass
    server.settimeout(None)

# Function to be used by the host
# Function for the threads for each client to run
# For right now, it does nothing interesting
def host_serve_client(client, clientID, variables_for_user_link):
    client.settimeout(0.2)
    client.send(generate_random_string().encode("ascii"))
    while variables_for_user_link[2][clientID]:
        try:
            vote = client.recv(1024).decode("ascii").split("\x09")
            variables_for_user_link[3][clientID] = vote
            variables_for_user_link[0].testing_label.text = "Client #" + str(clientID+1) + " has " + vote[1] + "d " + vote[0]
            #variables_for_user_link[4][clientID] = True
            #while variables_for_user_link[4][clientID]:
            #    """Wait for vote to be recorded before sending a new movie title"""
            client.send(generate_random_string().encode("ascii"))
        except socket.timeout:
            pass

# Function for closing the socket the host is using
# Terminates the threads for each client before closing the host's socket
def host_server_shutdown(variables_for_user_link):
    for i in range(len(variables_for_user_link[2])):
        variables_for_user_link[2][i] = False
        variables_for_user_link[5][i].join()
    variables_for_user_link[6].close()

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
    client.settimeout(0.2)
    while variables_for_user_link[0]:
        try:
            movie = client.recv(1024).decode("ascii")
            variables_for_user_link[1] = movie
            variables_for_user_link[2] = True
            while variables_for_user_link[2]:
                if not variables_for_user_link[0]:
                    variables_for_user_link[1] = "voting\x09stoppe"
                    variables_for_user_link[2] = False
            client.send(variables_for_user_link[1].encode("ascii"))
        except socket.timeout:
            pass
    variables_for_user_link[1] = "\x09shutdown"
    variables_for_user_link[2] = True

# Function for closing the socket the client is using
# Terminates the thread handling the connection to the host before closing the client's socket
def client_shutdown(variables_for_user_link):
    variables_for_user_link[0] = False
    variables_for_user_link[4].join()
    variables_for_user_link[3].close()

import random
def generate_random_string():
    random_string = ""
    x = random.randint(2,7)
    for i in range(x):
        random_string += str(random.randint(0,9))
    return random_string