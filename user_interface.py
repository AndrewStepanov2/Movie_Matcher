from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput

import user_link
import threading
variables_for_user_link = []

class MovieMatcher(App):

    def build(self):

        global variables_for_user_link
        variables_for_user_link = []

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

        #######################################################################################################################################################
        # A label for testing purposes
        # It can be removed after testing is complete
        self.testing_label = Label(text="Testing")
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
        variables_for_user_link.append(True) # for storing a boolean value to stop the accepting thread when voting is ready to begin
        server, thread = user_link.start_hosting(variables_for_user_link)
        variables_for_user_link.append(server) # for storing the socket used by the host for the server
        variables_for_user_link.append(thread) # for storing the accepting thread
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
        variables_for_user_link[0] = False # stops the accepting thread
        variables_for_user_link[5].join() # waits for the accepting thread to terminate
        self.window.remove_widget(self.IP_label)
        self.window.remove_widget(self.start_button)

        #######################################################################################################################################################
        # The testing label is used for testing purposes
        # The code can be removed after testing is complete
        self.window.add_widget(self.testing_label)
        #######################################################################################################################################################


    # The non-host has entered the host's IP address into the text input and would like to connect to the host
    # user_link.client_join_server will start a thread for the connection to the host
    # Remove the text input for entering the host's IP address and the connect button
    def press_connect_button(self, instance):
        variables_for_user_link.append(True) # for storing a boolean value that we can change to stop the client's thread that handles communication with the server
        client, thread = user_link.client_join_server(self.input_IP.text, variables_for_user_link)
        variables_for_user_link.append(client) # for storing the client's socket for communicating with the host
        variables_for_user_link.append(thread) # for storing the thread used by the client to handle communication with the host
        self.window.remove_widget(self.input_IP)
        self.window.remove_widget(self.connect_button)

        #######################################################################################################################################################
        # The testing label is used for testing purposes
        # The code can be removed after testing is complete
        self.window.add_widget(self.testing_label)
        #######################################################################################################################################################

MovieMatcher().run()