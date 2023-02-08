##
# file: backend.py
# Brief: classes and functions for Trezor
# autor: Michal Ľaš

from cryptography.fernet import Fernet
import os
from pathlib import Path
import pyrebase
import urllib
from urllib.request import urlopen



class SafeLock:

    def __init__(self):
        pass


    ##
    # Function try to log to Firebase database and get encryption key
    # email: email for log in
    # given_password: password for log in
    # key_name: name of key as default is set MYKEY  
    def get_data(self, email:str, given_password:str, key_name:str="MYKEY"):
        
        if SafeLock.is_internet():
            FB = FireBaseData()
            return FB.get_key(email, given_password, key_name)
        else:
            # no internet connection
            return "ERROR"
    

    ##
    # Function open Trezor (Safe)
    # key: key needed for decryption
    def open_safe(self, key):

        if SafeLock.is_lock():
            SF = SafeData()
            SF.open_safe(key)
            # set that Safe was opened
            SafeLock.set_lock("0")
        


    ##
    # Function lock Trezor (Safe), generets and push new encryption key to database
    # email: email for log in
    # given_password: password for log in
    # key_name: name of key as default is set MYKEY
    # return: error msg or Success
    def lock_safe(self, email:str, given_password:str, key_name:str="MYKEY"):

        # check internet connection
        if not SafeLock.is_internet():
            return "ERROR"
        
        SF = SafeData()
        new_key = SF.generate_key().decode()

        # PUSH KEY TO DATABASE
        FB = FireBaseData()
        msg = FB.push_new_key(new_key, email, given_password, key_name)

        if (msg == "Wrong email or password") or (msg == "Access denied"):
            return msg
        

        # Encrypt folder
        SF.lock_safe(new_key)
        SafeLock.set_lock("1")
        return "Success"
    

    ##
    # Function chceck if internet conncetion is available
    # return True if internet connection is available
    # return False if internet connection is not available
    def is_internet(self=None):
        try:
            urlopen("https://www.google.com", timeout=1)
            return True
        except urllib.error.URLError as Error:
            print(Error)
            return False
        
    
    ##
    # Function check if file trezor is locked
    # return True if trezor is lock
    # return False if trezor is not lock
    def is_lock(self=None):

        path = Path(__file__).parent / "../data/.open"

        with open(path, 'r') as f:
            data = f.read()
            if (data == "0"):
                msg = False
            else:
                msg = True

        return msg


    ##
    # Function set data in file for controling if Safe is close (1) or open (0)
    # set_to: "0" if Safe is open "1" if Safe is locked
    def set_lock(set_to, self=None):

        path = Path(__file__).parent / "../data/.open"

        with open(path, 'w') as f:
            if (set_to == "0"):                        
                f.write("0")
            else:
                f.write("1")


class FireBaseData:

    def __init__(self):
        self.firebaseConfig = {
            "apiKey": "yourApiKey",
            "authDomain": "yourAuthDomain",
            "databaseURL": "yourDatabaseURL",
            "projectId": "yourProjectID",
            "storageBucket": "yourStorageBucket",
            "messagingSenderId": "yourmessagingSenderID",
            "appId": "yourAPPID",
            "measurementId": "yourMeasurementId"
            }

    ##
    # Function get password hash from the FirebaseServer
    # @return: password hash
    # return: error msg or key
    def get_key(self, email:str, password:str, key_name:str="MYKEY"):
        
        firebase = pyrebase.initialize_app(self.firebaseConfig)

        # authenticate a user
        auth = firebase.auth()
        
        try:
            user = auth.sign_in_with_email_and_password(email, password)
        
        except:
            return "Wrong email or password"

        id_token = user["idToken"]

        try:
            db = firebase.database()

        except:
            return "Access denied"

        # Get the data from the database
        data = db.child("KEYS").get(id_token)
        return data.val()[key_name]
    

    ##
    # Function push new encryption key to database
    # email: email for log in
    # given_password: password for log in
    # key_name: name of key as default is set MYKEY 
    # return: error msg or Success
    def push_new_key(self, new_key, email:str, password:str, key_name:str="MYKEY"):

        firebase = pyrebase.initialize_app(self.firebaseConfig)

        # authenticate a user
        auth = firebase.auth()
        
        try:
            user = auth.sign_in_with_email_and_password(email, password)
        
        except:
            return "Wrong email or password"

        id_token = user["idToken"]

        try:
            db = firebase.database()

        except:
            return "Access denied"
        
        db.child("KEYS").child(key_name).set(new_key, id_token)
        return "Success"



        
            

class SafeData:

    def __init__(self):
        self.key = None
        self.hash = None


    ##
    # Function generate new encryption key
    # return: encryption key
    def generate_key(self):
        self.key = Fernet.generate_key()
        return self.key


    ##
    # Function encrypt every file in Safe directory
    def lock_safe(self, key):

        path = Path(__file__).parent / "../Safe"

        # Generate a Fernet key
        fernet = Fernet(key)

        for root, dirs, files in os.walk(path):
            for file in files:
                file_path = os.path.join(root, file)
                # Open the file in read binary mode
                with open(file_path, 'rb') as f:
                    # Read the file's content
                    file_data = f.read()
                    # Encrypt the file's content
                    encrypted_data = fernet.encrypt(file_data)
                    # Write the encrypted content back to the file
                    with open(file_path, 'wb') as f:
                        f.write(encrypted_data)

    
    ##
    # Function decrypt all data in Safe directory
    def open_safe(self, key):

        path = Path(__file__).parent / "../Safe"

        # Generate a Fernet key
        fernet = Fernet(key)

        # Iterate through all files in the folder
        for root, dirs, files in os.walk(path):
            for file in files:
                file_path = os.path.join(root, file)
                # Open the file in read binary mode
                with open(file_path, 'rb') as f:
                    # Read the file's content
                    encrypted_data = f.read()
                    # Decrypt the file's content
                    decrypted_data = fernet.decrypt(encrypted_data)
                    # Write the decrypted content back to the file
                    with open(file_path, 'wb') as f:
                        f.write(decrypted_data)                       