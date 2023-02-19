##
# file: backend.py
# Brief: classes and functions for Trezor
# autor: Michal Ľaš

from cryptography.fernet import Fernet
import os
from pathlib import Path
from urllib.request import urlopen
import hashlib



class SafeLock:

    def __init__(self):
        # set password
        self.password = "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8" # password


    ##
    # Function try to log to Firebase database and get encryption key
    # email: email for log in
    # given_password: password for log in
    # key_name: name of key as default is set MYKEY  
    def get_data(self, key_path:str):
        return self.get_key(key_path)


    ##
    # Function open Trezor (Safe)
    # key: key needed for decryption
    def open_safe(self, key):

        if SafeLock.is_lock():
            open_safe(key)
            # set that Safe was opened
            SafeLock.set_lock("0")
        

    ##
    # Function lock Trezor (Safe), generets and save new encryption key to file_path
    # email: email for log in
    # given_password: password for log in
    # key_name: name of key as default is set MYKEY
    # return: error msg or Success
    def lock_safe(self, file_path):
        
        new_key = generate_key()

        # SAVE NEW KEY
        if not self.set_key(file_path, new_key):
            return "ERROR"
        
        # Encrypt folder
        lock_safe(new_key)
        SafeLock.set_lock("1")
        return "Success"
    

    ##
    # Function check if given password is valid
    # pw: password to be chacked
    # return True if password is valid
    # return False if password in not valid
    def check_pw(self, pw):
        pw_hash = hashlib.sha256(pw.encode()).hexdigest()
        return pw_hash == self.password
        
    
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


    ##
    # Function get encryptio key from given file path
    # file has to be .key format
    # file_path: file with encryption key
    # @return: password hash
    # return: error msg or key
    def get_key(self, file_path):
        if (file_path[-3:] == "key"):
            with open(file_path, "r") as f:
                key = f.read()
            return key
        else:
            return "ERROR"
        

    ##
    # Function wirite new encryption key to given file path
    # file has to be .key format
    # file_path: file where key will be stored
    # key: key that will be saved in file
    # return True if success
    # return False if not success
    def set_key(self, file_path, key):
        if (file_path[-3:] == "key"):
            with open(file_path, "wb") as f:
                f.write(key)
            return True
        else:
            return False

                


##
# Function generate new encryption key
# return: encryption key
def generate_key():
    return Fernet.generate_key()


##
# Function encrypt every file in Safe directory
def lock_safe(key):

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
def open_safe(key):

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