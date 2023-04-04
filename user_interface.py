from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput

import user_link
variables_for_user_link = []

import database
movie_database = ["Wait"]
filter_services_list = []

data_structure_movies_list = []
seen_movies_list = []

class MovieMatcher(App):

    def build(self):

        global variables_for_user_link
        variables_for_user_link = []
        global movie_database
        movie_database = ["Wait"]
        global filter_services_list
        filter_services_list = []

        # Let Kivy handle spacing of widgets
        # Kivy will put everything in one column
        # New widgets will be added below old widgets
        self.window = GridLayout()
        self.window.cols = 1

        # Define buttons to voluteer to be the host or to join a host's group
        self.host_button = Button(text="host")
        self.host_button.bind(on_press=self.press_host_button)
        self.join_button = Button(text="join")
        self.join_button.bind(on_press=self.press_join_button)

        # The host and join buttons will be the first things to appear when the app is opened
        self.window.add_widget(self.host_button)
        self.window.add_widget(self.join_button)

        # When a user volunteers to be the host, they will have a label for their IP address and a start button
        self.IP_label = Label(text=user_link.get_IP())
        self.start_button = Button(text="start")
        self.start_button.bind(on_press=self.press_start_button)

        # When a user wants to join a host's group, they will need text input for the IP address and a join button
        self.input_IP = TextInput(multiline=False)
        self.connect_button = Button(text="connect")
        self.connect_button.bind(on_press=self.press_connect_button)

        # We might restrict filtering to the host
        # We can use buttons to select what to filter
        # For now we will just have buttons for streaming services
        self.netflix_button = Button(text="Netflix")
        self.netflix_button.bind(on_press=self.press_netflix_button)
        self.disney_plus_button = Button(text="Disney Plus")
        self.disney_plus_button.bind(on_press=self.press_disney_plus_button)
        self.amazon_prime_button = Button(text="Amazon Prime")
        self.amazon_prime_button.bind(on_press=self.press_amazon_prime_button)
        self.hulu_button = Button(text="Hulu")
        self.hulu_button.bind(on_press=self.press_hulu_button)
        # When the host has selected the streaming services to be used, We'll need to create a pandas dataframe
        self.next_button = Button(text="next")
        self.next_button.bind(on_press=self.press_next_button)

        #######################################################################################################################################################
        # A label for testing purposes
        # It can be removed after testing is complete
        self.testing_label = Label(text="")
        #######################################################################################################################################################

        #######################################################################################################################################################
        # A button to shutdown the socket for the host
        # This is for running tests and can be removed later
        self.host_shutdown_button = Button(text="shutdown")
        self.host_shutdown_button.bind(on_press=self.press_host_shutdown_button)
        #######################################################################################################################################################

        # Buttons for the client to vote on a movie
        # A label for displaying a movie name
        # This can be made more elaborate later by replacing buttons with swiping if possible and adding in something for a movie poster
        self.client_movie_label = Label(text="")
        self.client_upvote_button = Button(text="upvote")
        self.client_upvote_button.bind(on_press=self.press_client_upvote_button)
        self.client_downvote_button = Button(text="downvote")
        self.client_downvote_button.bind(on_press=self.press_client_downvote_button)
        #######################################################################################################################################################
        # A button to shutdown the socket for the client
        # This is for running tests and can be removed later
        self.client_shutdown_button = Button(text="shutdown")
        self.client_shutdown_button.bind(on_press=self.press_client_shutdown_button)
        #######################################################################################################################################################

        # Everything is done through self.window, so that is what we return
        return self.window


    # A user has voluteered to be the host
    # user_link.start_hosting will start a thread for accepting non-hosts
    # This thread will start a thread for communicating with each non-host
    # Replace the host and join buttons with the label for displaying the host's IP address and a start button
    def press_host_button(self, instance):
        self.window.remove_widget(self.host_button)
        self.window.remove_widget(self.join_button)
        variables_for_user_link.append(True) # boolean value to stop the host's accepting thread
        server, thread = user_link.start_hosting(variables_for_user_link, movie_database)
        variables_for_user_link.append(server) # storing the socket that the host is using so that it can be shut down later
        variables_for_user_link.append(thread) # storing the host's accepting thread for proper termination later
        self.window.add_widget(self.IP_label)
        self.window.add_widget(self.start_button)
        

    # A user wants to join a host's group
    # Replace the host and join buttons with text input for entering an IP address and a connect button
    def press_join_button(self, instance):
        self.window.remove_widget(self.host_button)
        self.window.remove_widget(self.join_button)
        self.window.add_widget(self.input_IP)
        self.window.add_widget(self.connect_button)


    # The host has determined that all non-hosts have connected and it is time to start the voting process
    # Terminate the thread accepting non-hosts
    # Remove the label for the host's IP address and the button to start the voting
    def press_start_button(self, instance):
        variables_for_user_link[0] = False
        variables_for_user_link[7].join()
        self.window.remove_widget(self.IP_label)
        self.window.remove_widget(self.start_button)
        self.window.add_widget(self.netflix_button)
        self.window.add_widget(self.disney_plus_button)
        self.window.add_widget(self.amazon_prime_button)
        self.window.add_widget(self.hulu_button)
        self.window.add_widget(self.next_button)


    # The non-host has entered the host's IP address into the text input and would like to connect to the host
    # user_link.client_join_server will start a thread for the connection to the host
    # Remove the text input for entering the host's IP address and the connect button
    def press_connect_button(self, instance):
        variables_for_user_link.append(True) # boolean for stopping the client's thread
        variables_for_user_link.append("") # string for passing movies from thread to UI and votes from UI to thread
        variables_for_user_link.append(False) # boolean for halting the client thread while a client is voting
        client, thread = user_link.client_join_server(self.input_IP.text, variables_for_user_link)
        variables_for_user_link.append(client) # storing the socket used by the client so that it can be shutdown later
        variables_for_user_link.append(thread) # storing the thread used by the client so that it can be properly terminated later
        #movie_database.append(database.generate_database(["netflix", "disney_plus", "amazon_prime", "hulu"]))
        self.window.remove_widget(self.input_IP)
        self.window.remove_widget(self.connect_button)
        self.window.add_widget(self.client_movie_label)
        while not variables_for_user_link[2]:
            """Wait for the first movie title to be sent before allowing the client to vote"""
        self.client_movie_label.text = variables_for_user_link[1]
        self.window.add_widget(self.client_upvote_button)
        self.window.add_widget(self.client_downvote_button)
        self.window.add_widget(self.client_shutdown_button)


    # Function to add or remove Netflix from filtering
    def press_netflix_button(self, instance):
        global filter_services_list
        if (self.netflix_button.text == "Netflix"):
            filter_services_list.append("netflix")
            self.netflix_button.text = "Netflix added"
        else:
            filter_services_list.remove("netflix")
            self.netflix_button.text = "Netflix"


    # Function to add or remove Disney Plus from filtering
    def press_disney_plus_button(self, instance):
        global filter_services_list
        if (self.disney_plus_button.text == "Disney Plus"):
            filter_services_list.append("disney_plus")
            self.disney_plus_button.text = "Disney Plus added"
        else:
            filter_services_list.remove("disney_plus")
            self.disney_plus_button.text = "Disney Plus"


    # Function to add or remove Amazon Prime from filtering
    def press_amazon_prime_button(self, instance):
        global filter_services_list
        if (self.amazon_prime_button.text == "Amazon Prime"):
            filter_services_list.append("amazon_prime")
            self.amazon_prime_button.text = "Amazon Prime added"
        else:
            filter_services_list.remove("amazon_prime")
            self.amazon_prime_button.text = "Amazon Prime"


    # Function to add or remove Hulu from filtering
    def press_hulu_button(self, instance):
        global filter_services_list
        if (self.hulu_button.text == "Hulu"):
            filter_services_list.append("hulu")
            self.hulu_button.text = "Hulu added"
        else:
            filter_services_list.remove("hulu")
            self.hulu_button.text = "Hulu"


    # Function to create the pandas dataframe when the host has selected the filters for the streaming services
    def press_next_button(self, instance):
        self.window.remove_widget(self.netflix_button)
        self.window.remove_widget(self.disney_plus_button)
        self.window.remove_widget(self.amazon_prime_button)
        self.window.remove_widget(self.hulu_button)
        self.window.remove_widget(self.next_button)
        #######################################################################################################################################################
        # The testing label is used for testing purposes
        # The code can be removed after testing is complete
        self.window.add_widget(self.testing_label)
        self.window.add_widget(self.host_shutdown_button)
        variables_for_user_link[0] = self
        #######################################################################################################################################################
        movie_database.append(database.generate_database(filter_services_list))
        movie_database[0] = ""


    # Function to allow the client to upvote a title
    def press_client_upvote_button(self, instance):
        if not variables_for_user_link[2]:
            return
        variables_for_user_link[1] += "\x09upvote"
        variables_for_user_link[2] = False
        while not variables_for_user_link[2]:
            """Wait for the next movie title to be sent"""
        self.client_movie_label.text = variables_for_user_link[1]
        if variables_for_user_link[1] == "\x09shutdown":
            self.window.remove_widget(self.client_upvote_button)
            self.window.remove_widget(self.client_downvote_button)


    # Function to allow the client to downvote a title
    def press_client_downvote_button(self, instance):
        if not variables_for_user_link[2]:
            return
        variables_for_user_link[1] += "\x09downvote"
        variables_for_user_link[2] = False
        while not variables_for_user_link[2]:
            """Wait for the next movie title to be sent"""
        self.client_movie_label.text = variables_for_user_link[1]
        if variables_for_user_link[1] == "\x09shutdown":
            self.window.remove_widget(self.client_upvote_button)
            self.window.remove_widget(self.client_downvote_button)


    #######################################################################################################################################################
    # Function to be bound to temporary host shutdown button
    def press_host_shutdown_button(self, instance):
        user_link.host_server_shutdown(variables_for_user_link)
        self.window.remove_widget(self.host_shutdown_button)
        self.testing_label.text = "shutdown"
    #######################################################################################################################################################

    #######################################################################################################################################################
    # Function to be bound to temporary client shutdown button
    def press_client_shutdown_button(self, instance):
        user_link.client_shutdown(variables_for_user_link)
        self.window.remove_widget(self.client_movie_label)
        self.window.remove_widget(self.client_upvote_button)
        self.window.remove_widget(self.client_downvote_button)
        self.window.remove_widget(self.client_shutdown_button)
        self.window.add_widget(self.testing_label)
        self.testing_label.text = "shutdown"
    #######################################################################################################################################################

MovieMatcher().run()