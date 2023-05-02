import socket
import threading

# Returns the IP address of the computer that calls it as a string
# socket.gethostbyname(socket.gethostname()) doesn't work as it will return 127.0.1.1
# The function sets up a UDP connection with Google Public DNS and takes the IP address from that connection
def get_IP():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
    s.connect(("8.8.8.8", 80)) 
    ip = s.getsockname()[0] 
    s.close() 
    return ip 

# Sets up a socket for the host
# Starts a thread for accepting clients
def start_hosting(variables_for_user_link, movie_database, user_votes):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((get_IP(), 42424))
    server.settimeout(0.2)
    server.listen()
    variables_for_user_link.append([]) # for storing the clients that join the server run by the host
    variables_for_user_link.append([]) # for storing boolean values that we can change to stop the threads that handle the clients
    variables_for_user_link.append([]) # for storing the movie title and vote of a client
    variables_for_user_link.append([]) # for storing a boolean value to indicate if a client has voted or not
    variables_for_user_link.append([]) # for storing the threads that handles the clients
    thread = threading.Thread(target=host_accept_client, args=(server, variables_for_user_link, movie_database, user_votes))
    thread.start()
    return (server, thread)

# Function for a thread for the host to accept clients
# Starts a thread for each client
def host_accept_client(server, variables_for_user_link, movie_database, user_votes):
    clientID = 0
    while variables_for_user_link[0]:
        try:
            client, address = server.accept()
            user_votes.append([])
            variables_for_user_link[1].append(client)
            variables_for_user_link[2].append(True)
            variables_for_user_link[3].append("")
            variables_for_user_link[4].append(False)
            thread = threading.Thread(target=host_serve_client, args=((client, clientID, variables_for_user_link, movie_database, user_votes)))
            thread.start()
            variables_for_user_link[5].append(thread)
            clientID += 1
        except socket.timeout:
            pass
    server.settimeout(None)

# Function to be used by the host
# Function for the threads for each client to run
# For right now, it does nothing interesting
def host_serve_client(client, clientID, variables_for_user_link, movie_database, user_votes):
    client_filters = client.recv(1024).decode("ascii")[1:-1]
    if client_filters == "":
        """The client did not send any filters, so do nothing"""
    else:
        variables_for_user_link[3][clientID] = client_filters.split("\x09")
    variables_for_user_link[4][clientID] = True
    while movie_database[0] == "Wait":
        """Wait for the database to be generated"""
    #client.settimeout(0.2)
    client.send((movie_database[1].iat[0, 1] + "\x09" + str(movie_database[1].iat[0, 2]) + "\x09" + movie_database[1].iat[0, 6]).encode("ascii"))
    while variables_for_user_link[2][clientID]:
        try:
            vote = client.recv(1024).decode("ascii").split("\x09")
            # variables_for_user_link[0].testing_label.text = "Client #" + str(clientID+1) + " has " + vote[1] + "d " + vote[0]
            windex = -1

            if vote[1] == "upvote":
                user_votes[clientID+1].append(True)
                windex = check_win(user_votes, len(user_votes[clientID+1]) - 1)
            else:
                user_votes[clientID+1].append(False)


            #print(user_votes)
            # do stuff with winning movie
            if windex >= 0:
                #print(windex)
                movie_database[0] = movie_database[1].iat[windex, 1] + "\x09" + str(movie_database[1].iat[windex, 2]) + "\x09" + movie_database[1].iat[windex, 6]
                


            if movie_database[0] != "":
                client.send(("winner\x09" + movie_database[0]).encode("ascii"))
            else:
                movie_num = len(user_votes[clientID+1])
                client.send((movie_database[1].iat[movie_num, 1] + "\x09" + str(movie_database[1].iat[movie_num, 2]) + "\x09" + movie_database[1].iat[movie_num, 6]).encode("ascii"))
        except:
            return

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
    while variables_for_user_link[1] == "":
        """Wait for the client to select filters"""
    client.send(variables_for_user_link[1].encode("ascii"))
    variables_for_user_link[1] = ""
    #client.settimeout(0.2)
    while variables_for_user_link[0]:
        movie = client.recv(1024).decode("ascii")
        variables_for_user_link[1] = movie
        variables_for_user_link[2] = True
        while variables_for_user_link[2]:
            if not variables_for_user_link[0]:
                variables_for_user_link[1] = "voting\x09stoppe"
                variables_for_user_link[2] = False
        client.send(variables_for_user_link[1].encode("ascii"))
    variables_for_user_link[1] = "\x09shutdown"
    variables_for_user_link[2] = True

# Function for closing the socket the client is using
# Terminates the thread handling the connection to the host before closing the client's socket
def client_shutdown(variables_for_user_link):
    variables_for_user_link[0] = False
    variables_for_user_link[4].join()
    variables_for_user_link[3].close()

# Check if a movie has been decided upon
# TODO: impliment
def check_win(user_votes, index):
    for i in range(len(user_votes)):
        if (len(user_votes[i]) <= index):
            return -1
        if not user_votes[i][index]:
            return -1
    return index