##
# file: gui.py
# Brief: Grafical interface for Trezor
# autor: Michal Ľaš

from kivy.lang import Builder
from kivy.properties import StringProperty
from kivymd.app import MDApp
from kivymd.uix.relativelayout import MDRelativeLayout
from plyer import filechooser
from backend import SafeLock


class ClickableTextFieldRound(MDRelativeLayout):
    text = StringProperty()
    hint_text = StringProperty()



class Safe(MDApp):

    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Red"
        return Builder.load_file("gui.kv")
    

    ##
    # function validate password and email, if they are correct, then decrypt data and update button to "lock"
    # if the button is pressed data become again encrypted and new encryption key is send to database
    def check_lock(self):

        SF = SafeLock()

        # open safe
        if (self.root.ids.submit_button.text == "Submit"):

            if (self.root.ids.password_field.ids.text_field.text == "") or (self.root.ids.selected_key.text == "Select key"):
                return


            key = SF.get_data(self.root.ids.selected_key.text)

            # Check key
            if (key == "ERROR"):
                self.root.ids.consol_text.text = "Wrong key file selected !"
                self.root.ids.consol_text.color = "red"
                return

            # Check password
            if (SF.check_pw(self.root.ids.password_field.ids.text_field.text)):
                self.root.ids.consol_text.text = "Welcome, Do not forget to lock me !"
                self.root.ids.consol_text.color = "green"
                self.root.ids.submit_button.text = "Lock"
                # decrypt data
                SF.open_safe(key)
            else:
                self.root.ids.consol_text.text = "Invalid password !"
                self.root.ids.consol_text.color = "red"
        
              
        # lock safe
        else:
            # Check password
            if (SF.check_pw(self.root.ids.password_field.ids.text_field.text)):

                msg = SF.lock_safe(self.root.ids.selected_key.text)
                if (msg == "Success"):
                    self.root.ids.consol_text.text = "Give me key and password"
                    self.root.ids.consol_text.color = "yellow"
                    self.root.ids.submit_button.text = "Submit"
                elif (msg == "ERROR"):
                    self.root.ids.consol_text.text = "Wrong key file selected ! You still have to lock me !"
                    self.root.ids.consol_text.color = "red"

            else:
                self.root.ids.consol_text.text = "Wrong password ! You still have to lock me !"
                self.root.ids.consol_text.color = "red"


    ##
    # Function open file chooser and call selected() function to show which file was selected
    def choose_file(self):
        filechooser.open_file(on_selection=self.selected)

    
    ##
    # Function show path to selected file
    # selection: file_path
    def selected(self, selection):
        if selection:
            self.root.ids.selected_key.text = selection[0]