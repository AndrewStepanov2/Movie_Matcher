from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput

import user_link

class MovieMatcher(App):

    def build(self):
        # Let Kivy handle spacing of widgets
        # Kivy will put everything in one column
        # New widgets will be added below old widgets
        self.window = GridLayout()
        self.window.cols = 1
        # Define buttons to voluteer to be the host or join a host's group
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
        self.join_button2 = Button(text="join")
        self.join_button2.bind(on_press=self.press_join_button2)
        # Everything is done through self.window, so that is what we return
        return self.window
    # A user has voluteered to be the host
    # Replace the host and join buttons with the IP label and a start button
    def press_host_button(self, instance):
        self.window.remove_widget(self.host_button)
        self.window.remove_widget(self.join_button)
        self.window.add_widget(self.IP_label)
        self.window.add_widget(self.start_button)
    # A user wants to join a host's group
    # Replace the host and join buttons with text input for entering an IP address and a second join button
    def press_join_button(self, instance):
        self.window.remove_widget(self.host_button)
        self.window.remove_widget(self.join_button)
        self.window.add_widget(self.input_IP)
        self.window.add_widget(self.join_button2)

    def press_start_button(self, instance):
        print('start')

    def press_join_button2(self, instance):
        host_IP = self.input_IP.text
        print(host_IP)

MovieMatcher().run()