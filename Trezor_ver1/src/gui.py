##
# file: gui.py
# Brief: Grafical interface for Trezor
# autor: Michal Ľaš

from kivy.lang import Builder
from kivy.properties import StringProperty
from kivymd.app import MDApp
from kivymd.uix.relativelayout import MDRelativeLayout
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

            if (self.root.ids.password_field.ids.text_field.text == "") or (self.root.ids.email_field.text == ""):
                return

            key = SF.get_data(self.root.ids.email_field.text, self.root.ids.password_field.ids.text_field.text)

            if (key == "ERROR"):
                self.root.ids.consol_text.text = "No internet connection !"
                self.root.ids.consol_text.color = "red"
                return

            if (key == "Wrong email or password") or (key == "Access denied"):
                self.root.ids.consol_text.text = key
                self.root.ids.consol_text.color = "red"
            else:
                self.root.ids.consol_text.text = "Welcome, Do not forget to lock me !"
                self.root.ids.consol_text.color = "green"
                self.root.ids.submit_button.text = "Lock"

                # decrypt data
                SF.open_safe(key.encode())
             
        # lock safe
        else:
            msg = SF.lock_safe(self.root.ids.email_field.text, self.root.ids.password_field.ids.text_field.text)
            if (msg == "Success"):
                self.root.ids.consol_text.text = "Fill your E-mail and password"
                self.root.ids.consol_text.color = "yellow"
                self.root.ids.submit_button.text = "Submit"
            elif (msg == "ERROR"):
                self.root.ids.consol_text.text = "No internet connection ! You still have to lock me !"
                self.root.ids.consol_text.color = "red"
            elif (msg == "Wrong email or password") or (msg == "Access denied"):
                self.root.ids.consol_text.text = msg + " ! You still have to lock me !"
                self.root.ids.consol_text.color = "red"